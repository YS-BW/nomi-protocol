import { PROTOCOL_VERSION, REMOTE_COMMAND_TYPES, REMOTE_EVENT_TYPES } from "./spec.js";
export { PROTOCOL_VERSION, REMOTE_COMMAND_TYPES, REMOTE_EVENT_TYPES };
export type RemoteCommandType = (typeof REMOTE_COMMAND_TYPES)[number];
export type RemoteEventType = (typeof REMOTE_EVENT_TYPES)[number];
export type MessageKind = "user" | "assistant" | "progress" | "task" | "system";
export type MessageStatus = "history" | "sent" | "streaming" | "completed" | "interrupted" | "task_delivered" | "error";
export type ThemePreference = "system" | "light" | "dark";
export type ConnectionReason = "idle" | "owner_unavailable" | "transport_error" | "auth_error" | "command_before_ready" | "closed" | "unknown";
export interface RemoteClientError {
    kind: Exclude<ConnectionReason, "idle" | "owner_unavailable" | "command_before_ready">;
    message: string;
}
export interface ConnectionProfile {
    host: string;
    port: string;
    token: string;
    clientId: string;
    defaultSessionId: string;
    lastBoundSessionId: string;
    themePreference: ThemePreference;
}
export interface ProviderCatalogItem {
    name: string;
    display_name: string;
    backend: string;
    default_api_base?: string | null;
    api_base_editable: boolean;
    is_gateway: boolean;
    is_local: boolean;
    is_direct: boolean;
    strip_model_prefix: boolean;
    supports_prompt_caching: boolean;
}
export interface ProviderCatalog {
    providers: ProviderCatalogItem[];
}
export interface MessageItem {
    id: string;
    kind: MessageKind;
    role: string;
    content: string;
    sessionId: string;
    status: MessageStatus;
}
export interface ActiveTurn {
    sessionId: string;
    draftText: string;
    hasStream: boolean;
    completed: boolean;
    stopReason: string | null;
    messageId: string | null;
}
export interface DesktopSessionState {
    sessionId: string;
    messages: MessageItem[];
    activeTurn: ActiveTurn | null;
    lastStatus: Record<string, unknown> | null;
    isBound: boolean;
}
export interface SidebarTaskItem {
    id: string;
    title: string;
    instruction: string;
    enabled: boolean;
    scheduleKind: "at" | "every" | "cron" | string;
    scheduleAtMs: number | null;
    scheduleEveryMs: number | null;
    scheduleExpr: string | null;
    scheduleTz: string | null;
    nextRunAtMs: number | null;
    runCount: number;
    status: string;
}
export interface SidebarSkillItem {
    name: string;
    path: string;
}
export interface SidebarMcpItem {
    name: string;
    enabled: boolean;
    transport: string;
    command: string;
    args: string[];
    url: string;
    enabledTools: string[];
    env?: Record<string, string>;
    headers?: Record<string, string>;
}
export interface DesktopSidebarData {
    tasks: SidebarTaskItem[];
    skills: SidebarSkillItem[];
    mcpServers: SidebarMcpItem[];
}
export interface SessionSummary {
    key: string;
    session_id: string;
    title?: string | null;
    created_at_ms?: number | null;
    updated_at_ms?: number | null;
    message_count?: number | null;
    archived?: boolean | null;
    source?: string | null;
    created_at?: string;
    updated_at?: string;
    path?: string;
}
export interface RemoteCommand {
    type: RemoteCommandType;
    session_id?: string;
    content?: string;
    client_id?: string;
    metadata?: Record<string, unknown>;
    limit?: number;
    cursor?: number | null;
    page_token?: string | null;
    page_size?: number | null;
    include_archived?: boolean | null;
    title?: string | null;
    instruction?: string;
    after_seconds?: number;
    at?: string;
    daily_time?: string;
    every_seconds?: number;
    task_id?: string;
    source?: string;
    upload_token?: string;
    skill_name?: string;
    mcp_name?: string;
    mcp?: Record<string, unknown>;
}
export interface RemoteEvent {
    type: RemoteEventType;
    session_id?: string;
    content?: string;
    host?: string;
    port?: number;
    provider_catalog?: ProviderCatalog;
    tool_hint?: boolean;
    resuming?: boolean;
    stop_reason?: string;
    result?: Record<string, unknown>;
    snapshot?: Record<string, unknown>;
    messages?: Array<Record<string, unknown>>;
    sessions?: SessionSummary[];
    task_id?: string;
    message?: string;
    code?: string;
    command?: string;
    metadata?: Record<string, unknown>;
    title?: string | null;
    created_at_ms?: number | null;
    updated_at_ms?: number | null;
    message_count?: number | null;
    archived?: boolean | null;
    source?: string | null;
    deleted?: boolean;
    total_messages?: number;
    total_count?: number | null;
    cursor?: number;
    next_cursor?: number | null;
    next_page_token?: string | null;
    sidebar?: DesktopSidebarData;
    resource?: string;
    action?: string;
    ok?: boolean;
    skill_name?: string;
    mcp_name?: string;
}
export interface DesktopActions {
    connect(): void;
    disconnect(): void;
    interruptCurrentTurn(): Promise<void>;
    clearRuntimeState(): Promise<void>;
    createNewSession(): Promise<void>;
    refreshSidebar(): Promise<void>;
    sendResourceCommand(command: RemoteCommand): Promise<boolean>;
    uploadSkillZip(file: File): Promise<string | null>;
    sendMainMessage(): Promise<void>;
    setDraftInput(value: string): void;
}
