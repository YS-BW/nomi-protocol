# Nomi Protocol

共享 remote wire contract 仓库。

当前范围只包含：

- `remote_protocol.json`
- Python 导出：`nomi_protocol`
- TypeScript 导出：`nomi-protocol`
- 协议示例 payload

当前额外约定：

- `ready` 事件会携带 `provider_catalog`
- desktop 应使用这份 catalog 决定 provider 设置页的只读/可编辑状态

当前不包含：

- runtime
- remote server
- desktop UI
- reducer / transport

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

## GitHub 依赖

Python：

```bash
pip install "nomi-protocol @ git+https://github.com/YS-BW/nomi-protocol.git@v0.3.0"
```

Node.js：

```bash
npm install github:YS-BW/nomi-protocol#v0.3.0
```

## 发布约定

- PyPI 包名：`nomi-protocol`
- npm 包名：`nomi-protocol`
- 版本统一走 SemVer
- GitHub 依赖阶段，`dist/` 也纳入 Git 提交
