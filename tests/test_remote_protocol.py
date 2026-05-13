"""共享 remote vNext 协议层测试。"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from nomi_protocol import HTTP_ROUTES, PROTOCOL_VERSION, SSE_EVENT_TYPES
from nomi_protocol.events import SseEventEnvelope
from nomi_protocol.http import CreateTaskRequest, CreateTurnRequest
from nomi_protocol.remote import load_remote_protocol_spec
from nomi_protocol.shared import (
    ActiveProviderSelection,
    ApiErrorResponse,
    ProviderCatalog,
    ProviderCatalogItem,
    ProviderFieldError,
    ProviderStateItem,
    ProviderStateSnapshot,
    TaskSchedule,
)


def _read_typescript_const_array(name: str) -> list[str]:
    """从 TypeScript 协议 spec 文件里读取常量数组。"""

    source = Path("src/spec.ts").read_text(encoding="utf-8")
    pattern = re.compile(rf"export const {name} = \[(.*?)\] as const;", re.S)
    match = pattern.search(source)
    assert match is not None
    return re.findall(r'"([^"]+)"', match.group(1))


def test_remote_protocol_spec_matches_python_contract() -> None:
    """共享协议 spec 应与 Python 薄封装保持一致。"""

    spec = load_remote_protocol_spec()

    assert PROTOCOL_VERSION == spec["version"]
    assert list(HTTP_ROUTES) == spec["httpRoutes"]
    assert list(SSE_EVENT_TYPES) == spec["sseEventTypes"]


def test_repo_root_and_python_package_spec_stay_in_sync() -> None:
    """仓库根协议文件和 Python 包内协议文件应保持一致。"""

    root_spec = json.loads(Path("remote_protocol.json").read_text(encoding="utf-8"))
    package_spec = json.loads(
        Path("nomi_protocol/remote_protocol.json").read_text(encoding="utf-8")
    )

    assert root_spec == package_spec


def test_remote_protocol_spec_matches_typescript_contract() -> None:
    """TypeScript 侧协议常量应与共享 spec 保持一致。"""

    spec = load_remote_protocol_spec()

    assert _read_typescript_const_array("HTTP_ROUTES") == spec["httpRoutes"]
    assert _read_typescript_const_array("SSE_EVENT_TYPES") == spec["sseEventTypes"]


def test_http_routes_cover_required_v1_surface() -> None:
    """vNext HTTP 路由应覆盖当前 remote 管理面。"""

    required = {
        "GET /v1/bootstrap",
        "POST /v1/sessions/{session_id}/turns",
        "POST /v1/tasks",
        "PUT /v1/providers/active",
        "POST /v1/runtime/reload",
        "GET /v1/events",
    }

    assert required.issubset(set(HTTP_ROUTES))


def test_sse_event_types_cover_session_and_turn_stream() -> None:
    """SSE 事件应覆盖跨 channel session 和 turn 实时更新。"""

    required = {
        "session.message_appended",
        "session.updated",
        "turn.started",
        "turn.delta",
        "turn.completed",
        "task.delivered",
    }

    assert required.issubset(set(SSE_EVENT_TYPES))


def test_create_task_request_accepts_global_target_channels_default() -> None:
    """target_channels 省略时应按全局提醒处理。"""

    request = CreateTaskRequest(
        instruction="明早提醒我量体重",
        schedule=TaskSchedule(kind="cron", expr="0 9 * * *", tz="Asia/Shanghai"),
        source_session_key="desktop:test",
    )

    assert request.target_channels == []


def test_create_turn_request_rejects_unknown_fields() -> None:
    """HTTP schema 应保持严格字段校验。"""

    with pytest.raises(Exception):
        CreateTurnRequest.model_validate({"content": "hello", "unexpected": True})


def test_legacy_remote_command_models_are_not_exported() -> None:
    """vNext 不应继续导出旧 command/event 模型。"""

    import nomi_protocol.remote as remote

    assert not hasattr(remote, "RemoteCommand")
    assert not hasattr(remote, "RemoteEvent")


def test_sse_event_envelope_accepts_known_event_type() -> None:
    """SSE envelope 应能校验已知事件类型。"""

    event = SseEventEnvelope(
        id="evt_test",
        type="session.message_appended",
        created_at_ms=1,
        data={"session_id": "weixin:test"},
    )

    assert event.type == "session.message_appended"


def test_api_error_response_shape() -> None:
    """统一错误模型应保持稳定。"""

    error = ApiErrorResponse(
        error={
            "code": "session_not_found",
            "message": "session not found",
            "details": {"session_id": "desktop:test"},
        }
    )

    assert error.error.code == "session_not_found"


def test_provider_catalog_python_model_accepts_bootstrap_payload_shape() -> None:
    """provider catalog 模型应能承接 bootstrap 里的元数据形状。"""

    catalog = ProviderCatalog(
        providers=[
            ProviderCatalogItem(
                name="custom",
                display_name="Custom",
                backend="openai_compat",
                default_api_base=None,
                api_base_editable=True,
                is_gateway=False,
                is_local=False,
                is_direct=True,
                strip_model_prefix=False,
                supports_prompt_caching=False,
            )
        ]
    )

    assert catalog.providers[0].name == "custom"
    assert catalog.providers[0].api_base_editable is True


def test_provider_state_python_models_accept_bootstrap_payload_shape() -> None:
    """provider state 模型应能承接 bootstrap 里的运行态配置形状。"""

    snapshot = ProviderStateSnapshot(
        providers=[
            ProviderStateItem(
                provider="deepseek",
                display_name="DeepSeek",
                backend="deepseek",
                builtin=True,
                editable=True,
                deletable=False,
                api_key_set=True,
                api_key_preview="…3688",
                saved_model="deepseek-chat",
                api_base="https://api.deepseek.com",
                api_base_editable=False,
                default_api_base="https://api.deepseek.com",
                source="config",
            )
        ],
        active=ActiveProviderSelection(
            provider="deepseek",
            model="deepseek-chat",
        ),
        apply_mode="reload_runtime",
    )

    assert snapshot.providers[0].provider == "deepseek"
    assert snapshot.active.model == "deepseek-chat"


def test_provider_field_error_model_accepts_field_level_validation_shape() -> None:
    """字段级错误模型应能承接 provider 设置校验结果。"""

    payload = ProviderFieldError(
        field="api_base",
        code="not_editable",
        message="api_base is read-only for this provider",
    )

    assert payload.field == "api_base"
    assert payload.code == "not_editable"
