export interface ApiErrorBody {
  code: string;
  message: string;
  details: Record<string, unknown>;
}

export interface ApiErrorResponse {
  error: ApiErrorBody;
}

export interface PageInfo {
  next_page_token?: string | null;
  total_count?: number | null;
}

export interface SessionSummary {
  key: string;
  session_id: string;
  title?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  created_at_ms?: number | null;
  updated_at_ms?: number | null;
  message_count?: number | null;
  archived?: boolean | null;
  source?: string | null;
  path?: string | null;
}

export interface SessionMessage {
  role: string;
  content?: unknown;
  timestamp?: string | null;
  tool_calls?: Array<Record<string, unknown>> | null;
  tool_call_id?: string | null;
  name?: string | null;
  reasoning_content?: string | null;
  reasoning_items?: unknown[] | null;
  thinking_blocks?: unknown[] | null;
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

export interface ProviderFieldError {
  field: string;
  code: string;
  message: string;
}

export interface ProviderStateItem {
  provider: string;
  display_name?: string | null;
  backend?: string | null;
  builtin?: boolean | null;
  editable?: boolean | null;
  deletable?: boolean | null;
  api_key_set: boolean;
  api_key_preview?: string | null;
  saved_model?: string | null;
  api_base?: string | null;
  api_base_editable?: boolean | null;
  default_api_base?: string | null;
  source?: string | null;
}

export interface ActiveProviderSelection {
  provider: string;
  model: string;
}

export interface ProviderStateSnapshot {
  providers: ProviderStateItem[];
  active: ActiveProviderSelection;
  apply_mode: "reload_runtime";
}

export type ProviderListSnapshot = ProviderStateSnapshot;

export interface SidebarTaskItem {
  id: string;
  title: string;
  instruction: string;
  enabled: boolean;
  scheduleKind: string;
  scheduleAtMs?: number | null;
  scheduleEveryMs?: number | null;
  scheduleExpr?: string | null;
  scheduleTz?: string | null;
  nextRunAtMs?: number | null;
  runCount: number;
  status: string;
  targetChannels: string[];
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

export interface TaskSchedule {
  kind: "at" | "every" | "cron";
  at_ms?: number | null;
  every_ms?: number | null;
  expr?: string | null;
  tz?: string | null;
}

export interface TaskItem {
  id: string;
  title: string;
  instruction: string;
  enabled: boolean;
  schedule: TaskSchedule;
  next_run_at_ms?: number | null;
  run_count: number;
  status: string;
  target_channels: string[];
}

export interface McpServerItem {
  name: string;
  enabled: boolean;
  type?: string | null;
  command: string;
  args: string[];
  url: string;
  enabled_tools: string[];
  env: Record<string, string>;
  headers: Record<string, string>;
}

export interface SkillItem {
  name: string;
  key?: string | null;
  path: string;
  description: string;
}
