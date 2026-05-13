import { SSE_EVENT_TYPES } from "./spec.js";
import type {
  ActiveProviderSelection,
  DesktopSidebarData,
  ProviderStateItem,
  ProviderStateSnapshot,
  SessionMessage,
  SessionSummary,
  TaskItem,
} from "./shared.js";

export { SSE_EVENT_TYPES };
export type SseEventType = (typeof SSE_EVENT_TYPES)[number];

export interface SseEventEnvelope<TData extends Record<string, unknown> = Record<string, unknown>> {
  id: string;
  type: SseEventType;
  created_at_ms: number;
  data: TData;
}

export interface RuntimeConnectedData {
  version: string;
  provider_state: ProviderStateSnapshot;
}

export interface RuntimeStatusChangedData {
  status: Record<string, unknown>;
}

export interface RuntimeReloadedData {
  active: ActiveProviderSelection;
  provider_state: ProviderStateSnapshot;
}

export interface SessionData {
  session: SessionSummary;
}

export interface SessionMessageAppendedData {
  session_id: string;
  message: SessionMessage;
  index?: number | null;
}

export interface TurnStartedData {
  turn_id: string;
  session_id: string;
}

export interface TurnTextData {
  turn_id?: string | null;
  session_id: string;
  content: string;
  tool_hint: boolean;
}

export interface TurnStreamEndData {
  turn_id?: string | null;
  session_id: string;
  resuming: boolean;
}

export interface TurnCompletedData {
  turn_id?: string | null;
  session_id: string;
  stop_reason: string;
  error?: string | null;
}

export interface TaskEventData {
  task?: TaskItem | null;
  task_id?: string | null;
  content?: string | null;
  session_id?: string | null;
}

export interface ProviderStateChangedData {
  provider_state: ProviderStateSnapshot;
}

export interface ProviderSettingsUpdatedData {
  provider: string;
  settings: ProviderStateItem;
  requires_runtime_reload: boolean;
}

export interface ProviderActiveChangedData {
  active: ActiveProviderSelection;
  requires_runtime_reload: boolean;
}

export interface SidebarSnapshotData {
  sidebar: DesktopSidebarData;
}

export interface ResourceEventData {
  resource: string;
  action: string;
  name?: string | null;
  item?: Record<string, unknown> | null;
}
