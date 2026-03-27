# 開發者指南

## 環境設定

```sh
uv sync
```

## 常用指令

| 指令 | 說明 |
|------|------|
| `make test` | 執行測試 |
| `make lint` | ruff 檢查 |
| `make fmt` | ruff 格式化 |
| `make check` | lint + test |

## 更新版號

請勿直接編輯 `pyproject.toml` 的版號，否則會與 `uv.lock` 產生不符，導致鎖定檔失效。應使用：

```sh
uv version --bump patch   # 0.1.1 → 0.1.2
uv version --bump minor   # 0.1.1 → 0.2.0
uv version --bump major   # 0.1.1 → 1.0.0
```
