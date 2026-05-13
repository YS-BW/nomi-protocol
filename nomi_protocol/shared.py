"""Nomi remote vNext 共享模型。"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictBase(BaseModel):
    """协议层基础模型。"""

    model_config = ConfigDict(extra="forbid")


class ApiErrorBody(StrictBase):
    """描述 HTTP API 的统一错误正文。"""

    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ApiErrorResponse(StrictBase):
    """描述 HTTP API 的统一错误响应。"""

    error: ApiErrorBody


class PageInfo(StrictBase):
    """描述分页响应元信息。"""

    next_page_token: str | None = None
    total_count: int | None = None


class SessionSummary(StrictBase):
    """描述远端可见的会话摘要。"""

    key: str
    session_id: str
    title: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_at_ms: int | None = None
    updated_at_ms: int | None = None
    message_count: int | None = None
    archived: bool | None = None
    source: str | None = None
    path: str | None = None


class SessionMessage(StrictBase):
    """描述远端历史与事件中使用的会话消息。"""

    role: str
    content: Any = ""
    timestamp: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None
    name: str | None = None
    reasoning_content: str | None = None
    reasoning_items: list[Any] | None = None
    thinking_blocks: list[Any] | None = None


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


class ProviderFieldError(StrictBase):
    """描述 provider 设置相关的字段级错误。"""

    field: str
    code: str
    message: str


class ProviderStateItem(StrictBase):
    """描述单个 provider 的当前持久化状态。"""

    provider: str
    display_name: str | None = None
    backend: str | None = None
    builtin: bool | None = None
    editable: bool | None = None
    deletable: bool | None = None
    api_key_set: bool = False
    api_key_preview: str | None = None
    saved_model: str | None = None
    api_base: str | None = None
    api_base_editable: bool | None = None
    default_api_base: str | None = None
    source: str | None = None


class ActiveProviderSelection(StrictBase):
    """描述当前 remote 默认生效的 provider/model 选择。"""

    provider: str
    model: str


class ProviderStateSnapshot(StrictBase):
    """描述远端 provider 设置页的完整状态快照。"""

    providers: list[ProviderStateItem] = Field(default_factory=list)
    active: ActiveProviderSelection
    apply_mode: Literal["reload_runtime"] = "reload_runtime"


ProviderListSnapshot = ProviderStateSnapshot


class SidebarTaskItem(StrictBase):
    """描述资源侧栏里的任务项。"""

    id: str
    title: str
    instruction: str
    enabled: bool
    scheduleKind: str
    scheduleAtMs: int | None = None
    scheduleEveryMs: int | None = None
    scheduleExpr: str | None = None
    scheduleTz: str | None = None
    nextRunAtMs: int | None = None
    runCount: int
    status: str
    targetChannels: list[str] = Field(default_factory=list)


class SidebarSkillItem(StrictBase):
    """描述资源侧栏里的 skill 项。"""

    name: str
    path: str


class SidebarMcpItem(StrictBase):
    """描述资源侧栏里的 MCP server 项。"""

    name: str
    enabled: bool = False
    transport: str = ""
    command: str = ""
    args: list[str] = Field(default_factory=list)
    url: str = ""
    enabledTools: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)


class DesktopSidebarData(StrictBase):
    """描述远端资源侧栏快照。"""

    tasks: list[SidebarTaskItem] = Field(default_factory=list)
    skills: list[SidebarSkillItem] = Field(default_factory=list)
    mcpServers: list[SidebarMcpItem] = Field(default_factory=list)


class TaskSchedule(StrictBase):
    """描述自动任务调度规则。"""

    kind: Literal["at", "every", "cron"]
    at_ms: int | None = None
    every_ms: int | None = None
    expr: str | None = None
    tz: str | None = None


class TaskItem(StrictBase):
    """描述远端可见的自动任务。"""

    id: str
    title: str
    instruction: str
    enabled: bool
    schedule: TaskSchedule
    next_run_at_ms: int | None = None
    run_count: int = 0
    status: str = "idle"
    target_channels: list[str] = Field(default_factory=list)


class McpServerItem(StrictBase):
    """描述一个 MCP server 配置。"""

    name: str
    enabled: bool = False
    type: str | None = None
    command: str = ""
    args: list[str] = Field(default_factory=list)
    url: str = ""
    enabled_tools: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)


class SkillItem(StrictBase):
    """描述一个已安装 skill。"""

    name: str
    key: str | None = None
    path: str
    description: str = ""
