"""Nomi remote vNext HTTP API 模型。"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from nomi_protocol.remote import HTTP_ROUTES
from nomi_protocol.shared import (
    ActiveProviderSelection,
    DesktopSidebarData,
    McpServerItem,
    PageInfo,
    ProviderCatalog,
    ProviderStateItem,
    ProviderStateSnapshot,
    SessionMessage,
    SessionSummary,
    SkillItem,
    StrictBase,
    TaskItem,
    TaskSchedule,
)

HttpRoute = Literal[*HTTP_ROUTES]


class HealthResponse(StrictBase):
    """健康检查响应。"""

    ok: bool = True
    version: str


class BootstrapResponse(StrictBase):
    """远端首屏启动快照。"""

    status: dict[str, Any] = Field(default_factory=dict)
    sessions: list[SessionSummary] = Field(default_factory=list)
    provider_catalog: ProviderCatalog
    provider_state: ProviderStateSnapshot
    tasks: list[TaskItem] = Field(default_factory=list)
    sidebar: DesktopSidebarData


class SessionListResponse(StrictBase):
    """会话列表响应。"""

    sessions: list[SessionSummary] = Field(default_factory=list)
    page: PageInfo = Field(default_factory=PageInfo)


class CreateSessionRequest(StrictBase):
    """创建会话请求。"""

    session_id: str | None = None
    title: str | None = None


class SessionResponse(StrictBase):
    """单个会话响应。"""

    session: SessionSummary


class DeleteSessionResponse(StrictBase):
    """删除会话响应。"""

    session_id: str
    deleted: bool


class SessionMessagesResponse(StrictBase):
    """会话消息列表响应。"""

    session_id: str
    messages: list[SessionMessage] = Field(default_factory=list)
    cursor: int = 0
    next_cursor: int | None = None
    total_messages: int = 0


class CreateTurnRequest(StrictBase):
    """创建一轮对话请求。"""

    content: str
    client_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CreateTurnResponse(StrictBase):
    """创建一轮对话响应。"""

    turn_id: str
    session_id: str
    status: Literal["queued"] = "queued"


class InterruptSessionResponse(StrictBase):
    """中断会话响应。"""

    session_id: str
    result: dict[str, Any]


class ResetSessionResponse(StrictBase):
    """重置会话响应。"""

    session_id: str
    reset: bool = True


class TaskListResponse(StrictBase):
    """任务列表响应。"""

    tasks: list[TaskItem] = Field(default_factory=list)


class CreateTaskRequest(StrictBase):
    """创建自动任务请求。"""

    instruction: str
    schedule: TaskSchedule
    source_session_key: str
    target_channels: list[str] = Field(default_factory=list)


class UpdateTaskRequest(StrictBase):
    """更新自动任务请求。"""

    instruction: str | None = None
    schedule: TaskSchedule | None = None
    target_channels: list[str] | None = None


class RescheduleTaskRequest(StrictBase):
    """重排自动任务请求。"""

    schedule: TaskSchedule


class TaskResponse(StrictBase):
    """单个任务响应。"""

    task: TaskItem


class DeleteTaskResponse(StrictBase):
    """删除任务响应。"""

    task_id: str
    deleted: bool


class ProviderListResponse(StrictBase):
    """provider 列表响应。"""

    provider_list: ProviderStateSnapshot


class ProviderStateResponse(StrictBase):
    """provider 状态响应。"""

    provider_state: ProviderStateSnapshot


class UpdateProviderRequest(StrictBase):
    """更新 provider 配置请求。"""

    api_key: str | None = None
    api_base: str | None = None
    model: str | None = None
    clear_api_key: bool | None = None


class UpdateProviderResponse(StrictBase):
    """更新 provider 配置响应。"""

    provider: str
    settings: ProviderStateItem
    requires_runtime_reload: bool


class SetActiveProviderRequest(StrictBase):
    """切换 active provider 请求。"""

    provider: str
    model: str | None = None


class SetActiveProviderResponse(StrictBase):
    """切换 active provider 响应。"""

    active: ActiveProviderSelection
    requires_runtime_reload: bool


class RuntimeReloadResponse(StrictBase):
    """runtime reload 响应。"""

    active: ActiveProviderSelection
    provider_state: ProviderStateSnapshot


class SkillListResponse(StrictBase):
    """skill 列表响应。"""

    skills: list[SkillItem] = Field(default_factory=list)


class SkillUploadResponse(StrictBase):
    """skill 上传响应。"""

    ok: bool
    upload_token: str
    filename: str


class InstallSkillRequest(StrictBase):
    """安装 skill 请求。"""

    source: str | None = None
    upload_token: str | None = None


class ResourceActionResponse(StrictBase):
    """资源动作响应。"""

    ok: bool
    message: str
    resource: str
    action: str
    id: str | None = None


class McpListResponse(StrictBase):
    """MCP server 列表响应。"""

    mcp_servers: list[McpServerItem] = Field(default_factory=list)


class UpsertMcpRequest(StrictBase):
    """创建或更新 MCP server 请求。"""

    mcp: dict[str, Any] = Field(default_factory=dict)


class McpResponse(StrictBase):
    """单个 MCP server 响应。"""

    mcp: McpServerItem


class DeleteMcpResponse(StrictBase):
    """删除 MCP server 响应。"""

    name: str
    deleted: bool
