"""共享 remote 协议定义。"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


@lru_cache(maxsize=1)
def load_remote_protocol_spec() -> dict[str, Any]:
    """加载共享 remote 协议 spec。"""

    spec_path = Path(__file__).with_name("remote_protocol.json")
    return json.loads(spec_path.read_text(encoding="utf-8"))


_REMOTE_PROTOCOL_SPEC = load_remote_protocol_spec()
PROTOCOL_VERSION = str(_REMOTE_PROTOCOL_SPEC["version"])
REMOTE_COMMAND_TYPES = tuple(str(item) for item in _REMOTE_PROTOCOL_SPEC["remoteCommandTypes"])
REMOTE_EVENT_TYPES = tuple(str(item) for item in _REMOTE_PROTOCOL_SPEC["remoteEventTypes"])

RemoteCommandType = Literal[*REMOTE_COMMAND_TYPES]
RemoteEventType = Literal[*REMOTE_EVENT_TYPES]


class StrictBase(BaseModel):
    """协议层基础模型。"""

    model_config = ConfigDict(extra="forbid")


class RemoteCommand(StrictBase):
    """描述一条远程客户端命令。"""

    type: RemoteCommandType
    session_id: str | None = None
    content: str | None = None
    client_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    limit: int | None = None
    cursor: int | None = None
    page_token: str | None = None
    page_size: int | None = None
    include_archived: bool | None = None
    title: str | None = None
    instruction: str | None = None
    after_seconds: int | None = None
    at: str | None = None
    daily_time: str | None = None
    every_seconds: int | None = None
    task_id: str | None = None
    source: str | None = None
    upload_token: str | None = None
    skill_name: str | None = None
    mcp_name: str | None = None
    mcp: dict[str, Any] = Field(default_factory=dict)


class ProviderCatalogItem(StrictBase):
    """描述一个可供远端 UI 使用的 provider 元数据条目。"""

    name: str
    display_name: str
    backend: str
    default_api_base: str | None = None
    api_base_editable: bool = False
    is_gateway: bool = False
    is_local: bool = False
    is_direct: bool = False
    strip_model_prefix: bool = False
    supports_prompt_caching: bool = False


class ProviderCatalog(StrictBase):
    """描述远端 UI 可见的 provider 元数据目录。"""

    providers: list[ProviderCatalogItem] = Field(default_factory=list)
