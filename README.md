# Nomi Protocol

共享 remote wire contract 仓库。

## 单一事实源

从现在开始，`nomi-protocol` 是 remote 协议的唯一事实源。

允许存在的协议产物只有：

- `remote_protocol.json`
- Python 导出：`nomi_protocol`
- TypeScript 导出：`nomi-protocol`

不应该再长期维护这些额外副本：

- `core` 仓里的第二份协议镜像
- `desktop` 仓里的手写 `src/protocol/*` 镜像
- “先改 core，再手抄到 desktop”的流程

正确方向固定为：

- 先改 `nomi-protocol`
- `core` 和 `desktop` 都直接消费它
- 联调通过后发正式版本
- 再升级 `core` / `desktop` 的依赖版本

当前范围只包含：

- `remote_protocol.json`
- Python 导出：`nomi_protocol`
- TypeScript 导出：`nomi-protocol`
- 协议示例 payload

## Remote vNext: HTTP + SSE

Remote vNext 全量切换为：

- HTTP API：查询、创建、更新、删除、管理动作
- SSE Event Stream：实时输出、会话变化、任务投递、运行态变化

后端实现固定使用 `aiohttp`。协议事实源仍然是本仓导出的 Python / TypeScript 类型。

### HTTP API

基础：

```text
GET /v1/health
GET /v1/bootstrap
GET /v1/status
GET /v1/sidebar
```

Sessions / Turns：

```text
GET    /v1/sessions
POST   /v1/sessions
GET    /v1/sessions/{session_id}
DELETE /v1/sessions/{session_id}
GET    /v1/sessions/{session_id}/messages
POST   /v1/sessions/{session_id}/turns
POST   /v1/sessions/{session_id}/interrupt
POST   /v1/sessions/{session_id}/reset
```

Tasks：

```text
GET    /v1/tasks
POST   /v1/tasks
GET    /v1/tasks/{task_id}
PATCH  /v1/tasks/{task_id}
DELETE /v1/tasks/{task_id}
POST   /v1/tasks/{task_id}/enable
POST   /v1/tasks/{task_id}/disable
POST   /v1/tasks/{task_id}/reschedule
```

Providers / Runtime：

```text
GET   /v1/providers
GET   /v1/providers/state
PATCH /v1/providers/{provider}
PUT   /v1/providers/active
POST  /v1/runtime/reload
POST  /v1/runtime/clear-remote-state
```

Skills：

```text
GET    /v1/skills
POST   /v1/skills/uploads
POST   /v1/skills
DELETE /v1/skills/{skill_name}
```

MCP：

```text
GET    /v1/mcp
POST   /v1/mcp
PATCH  /v1/mcp/{name}
DELETE /v1/mcp/{name}
POST   /v1/mcp/{name}/enable
POST   /v1/mcp/{name}/disable
```

### SSE

```text
GET /v1/events
```

事件统一 envelope：

```json
{
  "id": "evt_xxx",
  "type": "session.message_appended",
  "created_at_ms": 1780000000000,
  "data": {}
}
```

SSE 必须覆盖：

```text
runtime.connected
runtime.status_changed
runtime.reloaded
runtime.resync_required
session.created
session.updated
session.deleted
session.message_appended
turn.started
turn.progress
turn.delta
turn.stream_end
turn.completed
turn.failed
turn.interrupted
task.created
task.updated
task.deleted
task.delivered
provider.state_changed
provider.list_changed
provider.settings_updated
provider.active_changed
sidebar.invalidated
sidebar.snapshot
skill.installed
skill.uninstalled
mcp.created
mcp.updated
mcp.deleted
mcp.enabled
mcp.disabled
```

### 任务投递语义

`CreateTaskRequest.target_channels` 是可选字段：

- 省略或空数组：全局提醒
- `["weixin"]`：只投递微信
- `["cli"]`：只投递 CLI
- `["remote"]`：只投递 remote / desktop

当前额外约定：

- `GET /v1/bootstrap` 会携带 `provider_catalog` 和 `provider_state`。
- `GET /v1/providers` 返回完整 provider 管理列表。
- `PATCH /v1/providers/{provider}` 是 provider 配置写回入口。
- desktop 应使用 `provider_catalog` 决定 provider 设置页的只读/可编辑状态。
- provider 设置页的当前值和 active provider/model 由 core 通过 `provider_state` 提供。

当前不包含：

- runtime
- remote server
- desktop UI
- reducer / transport

## 依赖获取规则

### 开发联调

开发阶段允许使用本地路径依赖，但只允许直接指向 `nomi-protocol` 仓库，不允许复制代码。

Python：

```bash
uv add --editable /absolute/path/to/nomi-protocol
```

Node.js：

```bash
npm install file:/absolute/path/to/nomi-protocol
```

### 正式集成

正式环境不应长期依赖 GitHub tag URL。

规范做法固定为：

- Python 侧从 PyPI 获取 `nomi-protocol`
- Node.js 侧从 npm 获取 `nomi-protocol`
- `core` 和 `desktop` 都只 pin 发布版号

GitHub tag 只允许作为“注册表尚未可用时的短期过渡手段”，不能当长期依赖方案。

## 发布流程

每次协议变更后的正确顺序固定为：

1. 先在 `nomi-protocol` 仓库改协议
2. 本地执行 Python 测试和 TypeScript 构建
3. `core` 和 `desktop` 都切到本地路径依赖联调
4. 联调通过后，提升 `nomi-protocol` 版本号
5. 发布到 PyPI 和 npm
6. 再把 `core` / `desktop` 切到正式发布版

## 当前阶段说明

当前仓库已经具备：

- Python 包元数据
- npm 包元数据
- GitHub CI

但如果注册表发布流程还没接通，那么当前推荐顺序是：

- 开发联调：本地路径依赖
- 对外共享：临时 GitHub tag
- 最终目标：PyPI + npm 正式发版

## 本地开发

Python：

```bash
uv sync --extra dev
uv run pytest -q
```

TypeScript：

```bash
npm install
npm run build
```

## 临时 GitHub 依赖

只有在注册表发布尚未接通时才使用这组方式。

Python：

```bash
pip install "nomi-protocol @ git+https://github.com/YS-BW/nomi-protocol.git@v0.6.0"
```

Node.js：

```bash
npm install github:YS-BW/nomi-protocol#v0.6.0
```

## 发布约定

- PyPI 包名：`nomi-protocol`
- npm 包名：`nomi-protocol`
- 版本统一走 SemVer
- GitHub 依赖阶段，`dist/` 也纳入 Git 提交
- 发版后，`core` / `desktop` 只升级版本号，不再手动同步协议副本
