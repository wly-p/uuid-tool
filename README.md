# uuid-tool

UUID 產生與驗證的命令列工具，支援 v1 / v3 / v4 / v5。

## 安裝

```sh
uv tool install uuid-tool
```

## 使用

### 產生 UUID

```sh
# 預設產生 1 個 v4
uuid-tool generate

# 指定版本與數量
uuid-tool generate --type v1 --count 5
uuid-tool gen -t v4 -n 3
```

| 旗標 | 簡寫 | 說明 | 預設 |
|------|------|------|------|
| `--type` | `-t` | UUID 版本：`v1` `v3` `v4` `v5` | `v4` |
| `--count` | `-n` | 產生數量 | `1` |

### 驗證 UUID

```sh
# 直接傳入
uuid-tool validate 550e8400-e29b-41d4-a716-446655440000

# 多個
uuid-tool val <uuid1> <uuid2> ...

# 從 stdin pipe
cat uuids.txt | uuid-tool validate
uuid-tool gen -n 5 | uuid-tool val
```

結果：`✓` 表示有效，`✗` 表示無效。若有任何無效 UUID，exit code 為 `1`。

### GUI

提供圖形介面操作，功能與 CLI 相同（產生、驗證）。

```sh
uuid-tool --gui
uuid-tool -g
```

> **macOS + Homebrew**：需要額外安裝 tkinter
> ```sh
> brew install python-tk@3.13
> ```

## 開發

詳見 [DEVELOPMENT.md](DEVELOPMENT.md)。
