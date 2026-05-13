"""Nomi remote vNext SSE event 模型。"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from nomi_protocol.remote import SSE_EVENT_TYPES
from nomi_protocol.shared import (
    ActiveProviderSelection,
    DesktopSidebarData,
    ProviderStateItem,
    ProviderStateSnapshot,
    SessionMessage,
    SessionSummary,
    StrictBase,
    TaskItem,
)

SseEventType = Literal[*SSE_EVENT_TYPES]


class SseEventEnvelope(StrictBase):
    """SSE 事件统一 envelope。"""

    id: str
    type: SseEventType
    created_at_ms: int
    data: dict[str, Any] = Field(default_factory=dict)


class RuntimeConnectedData(StrictBase):
    """runtime.connected 数据。"""

    version: str
    provider_state: ProviderStateSnapshot


class RuntimeStatusChangedData(StrictBase):
    """runtime.status_changed 数据。"""

    status: dict[str, Any] = Field(default_factory=dict)


class RuntimeReloadedData(StrictBase):
    """runtime.reloaded 数据。"""

    active: ActiveProviderSelection
    provider_state: ProviderStateSnapshot


class SessionData(StrictBase):
    """session created/updated/deleted 数据。"""

    session: SessionSummary


class SessionMessageAppendedData(StrictBase):
    """session.message_appended 数据。"""

    session_id: str
    message: SessionMessage
    index: int | None = None


class TurnStartedData(StrictBase):
    """turn.started 数据。"""

    turn_id: str
    session_id: str


class TurnTextData(StrictBase):
    """turn progress/delta 数据。"""

    turn_id: str | None = None
    session_id: str
    content: str
    tool_hint: bool = False


class TurnStreamEndData(StrictBase):
    """turn.stream_end 数据。"""

    turn_id: str | None = None
    session_id: str
    resuming: bool = False


class TurnCompletedData(StrictBase):
    """turn completed/failed/interrupted 数据。"""

    turn_id: str | None = None
    session_id: str
    stop_reason: str
    error: str | None = None


class TaskEventData(StrictBase):
    """task 事件数据。"""

    task: TaskItem | None = None
    task_id: str | None = None
    content: str | None = None
    session_id: str | None = None


class ProviderStateChangedData(StrictBase):
    """provider 状态事件数据。"""

    provider_state: ProviderStateSnapshot


class ProviderSettingsUpdatedData(StrictBase):
    """provider 设置事件数据。"""

    provider: str
    settings: ProviderStateItem
    requires_runtime_reload: bool


class ProviderActiveChangedData(StrictBase):
    """active provider 事件数据。"""

    active: ActiveProviderSelection
    requires_runtime_reload: bool


class SidebarSnapshotData(StrictBase):
    """sidebar.snapshot 数据。"""

    sidebar: DesktopSidebarData


class ResourceEventData(StrictBase):
    """skill/mcp 资源事件数据。"""

    resource: str
    action: str
    name: str | None = None
    item: dict[str, Any] | None = None
