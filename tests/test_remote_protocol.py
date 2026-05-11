"""共享 remote 协议层测试。"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from nomi_protocol.remote import (
    PROTOCOL_VERSION,
    REMOTE_COMMAND_TYPES,
    REMOTE_EVENT_TYPES,
    ActiveProviderSelection,
    ProviderCatalog,
    ProviderCatalogItem,
    ProviderFieldError,
    ProviderStateItem,
    ProviderStateSnapshot,
    RemoteCommand,
    load_remote_protocol_spec,
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
    assert list(REMOTE_COMMAND_TYPES) == spec["remoteCommandTypes"]
    assert list(REMOTE_EVENT_TYPES) == spec["remoteEventTypes"]


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

    assert _read_typescript_const_array("REMOTE_COMMAND_TYPES") == spec["remoteCommandTypes"]
    assert _read_typescript_const_array("REMOTE_EVENT_TYPES") == spec["remoteEventTypes"]


def test_remote_command_accepts_all_known_command_types() -> None:
    """所有共享命令类型都应能通过 Python 命令模型校验。"""

    for command_type in REMOTE_COMMAND_TYPES:
        command = RemoteCommand(type=command_type)
        assert command.type == command_type


def test_remote_command_rejects_unknown_command_type() -> None:
    """未知命令类型不应通过 Python 命令模型校验。"""

    with pytest.raises(Exception):
        RemoteCommand(type="unknown-command")


def test_examples_use_known_protocol_event_types() -> None:
    """示例 payload 的事件类型应来自共享协议集合。"""

    examples_root = Path("examples/events")
    for path in examples_root.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["type"] in REMOTE_EVENT_TYPES or payload["type"] in REMOTE_COMMAND_TYPES


def test_provider_catalog_python_model_accepts_ready_payload_shape() -> None:
    """provider catalog 模型应能承接 ready 事件里的元数据形状。"""

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


def test_provider_state_python_models_accept_ready_payload_shape() -> None:
    """provider state 模型应能承接 ready 事件里的运行态配置形状。"""

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


def test_remote_command_accepts_update_provider_clear_api_key_shape() -> None:
    """update_provider 应支持 clear_api_key 字段。"""

    command = RemoteCommand(
        type="update_provider",
        provider="custom",
        clear_api_key=True,
    )

    assert command.type == "update_provider"
    assert command.clear_api_key is True


def test_provider_field_error_model_accepts_field_level_validation_shape() -> None:
    """字段级错误模型应能承接 provider 设置校验结果。"""

    payload = ProviderFieldError(
        field="api_base",
        code="not_editable",
        message="api_base is read-only for this provider",
    )

    assert payload.field == "api_base"
    assert payload.code == "not_editable"
