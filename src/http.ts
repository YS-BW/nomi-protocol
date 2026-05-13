import { HTTP_ROUTES } from "./spec.js";
import type {
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
  TaskItem,
  TaskSchedule,
} from "./shared.js";

export { HTTP_ROUTES };
export type HttpRoute = (typeof HTTP_ROUTES)[number];

export interface HealthResponse {
  ok: boolean;
  version: string;
}

export interface BootstrapResponse {
  status: Record<string, unknown>;
  sessions: SessionSummary[];
  provider_catalog: ProviderCatalog;
  provider_state: ProviderStateSnapshot;
  tasks: TaskItem[];
  sidebar: DesktopSidebarData;
}

export interface SessionListResponse {
  sessions: SessionSummary[];
  page: PageInfo;
}

export interface CreateSessionRequest {
  session_id?: string | null;
  title?: string | null;
}

export interface SessionResponse {
  session: SessionSummary;
}

export interface DeleteSessionResponse {
  session_id: string;
  deleted: boolean;
}

export interface SessionMessagesResponse {
  session_id: string;
  messages: SessionMessage[];
  cursor: number;
  next_cursor?: number | null;
  total_messages: number;
}

export interface CreateTurnRequest {
  content: string;
  client_id?: string | null;
  metadata?: Record<string, unknown>;
}

export interface CreateTurnResponse {
  turn_id: string;
  session_id: string;
  status: "queued";
}

export interface InterruptSessionResponse {
  session_id: string;
  result: Record<string, unknown>;
}

export interface ResetSessionResponse {
  session_id: string;
  reset: boolean;
}

export interface TaskListResponse {
  tasks: TaskItem[];
}

export interface CreateTaskRequest {
  instruction: string;
  schedule: TaskSchedule;
  source_session_key: string;
  target_channels?: string[];
}

export interface UpdateTaskRequest {
  instruction?: string | null;
  schedule?: TaskSchedule | null;
  target_channels?: string[] | null;
}

export interface RescheduleTaskRequest {
  schedule: TaskSchedule;
}

export interface TaskResponse {
  task: TaskItem;
}

export interface DeleteTaskResponse {
  task_id: string;
  deleted: boolean;
}

export interface ProviderListResponse {
  provider_list: ProviderStateSnapshot;
}

export interface ProviderStateResponse {
  provider_state: ProviderStateSnapshot;
}

export interface UpdateProviderRequest {
  api_key?: string | null;
  api_base?: string | null;
  model?: string | null;
  clear_api_key?: boolean | null;
}

export interface UpdateProviderResponse {
  provider: string;
  settings: ProviderStateItem;
  requires_runtime_reload: boolean;
}

export interface SetActiveProviderRequest {
  provider: string;
  model?: string | null;
}

export interface SetActiveProviderResponse {
  active: ActiveProviderSelection;
  requires_runtime_reload: boolean;
}

export interface RuntimeReloadResponse {
  active: ActiveProviderSelection;
  provider_state: ProviderStateSnapshot;
}

export interface SkillListResponse {
  skills: SkillItem[];
}

export interface SkillUploadResponse {
  ok: boolean;
  upload_token: string;
  filename: string;
}

export interface InstallSkillRequest {
  source?: string | null;
  upload_token?: string | null;
}

export interface ResourceActionResponse {
  ok: boolean;
  message: string;
  resource: string;
  action: string;
  id?: string | null;
}

export interface McpListResponse {
  mcp_servers: McpServerItem[];
}

export interface UpsertMcpRequest {
  mcp: Record<string, unknown>;
}

export interface McpResponse {
  mcp: McpServerItem;
}

export interface DeleteMcpResponse {
  name: string;
  deleted: boolean;
}
