# open.mp/sa-mp 服务器文本提取与替换工具

一套用于 SA-MP/open.mp 服务器脚本（Pawn 语言）的源码文本提取与回写工具。
目标：快速定位需要翻译文本代码，无需手动翻阅源文件, 统一集中修改之后，一键自动替换原来的内容

**好处**：  
- 不用手动翻阅成百上千个文件去找要翻译的句子。  
- 翻译内容有误或需要更新时，直接在 `translate.json` 中查找修改即可，无需反复打开源码文件。  
- 可以轻松配合 AI 进行翻译：将 JSON 中的文本批量喂给 AI，**极大降低 token 消耗**，翻译后轻松自动替换回源码中。

## 使用方法

### 1. 下载脚本
将 `export.py` 和 `replace.py` 保存到你的电脑上的同一路径下

### 2. 修改配置
- 打开脚本，找到 `__main__` 部分的路径，改为你的脚本目录（例如 `E:\samp\gamemodes`）。

### 3. 运行
```bash
python export.py
```

### 4. 查看结果
运行结束后，会在当前目录生成 `translate.json` 文件，结构如下：
```json
[
    {
        "file": "E:/samp/gamemodes/mymode.pwn",
        "line": 123,
        "original_line": "    SendClientMessage(playerid, COLOR, \"欢迎来到服务器！\");"
    },
    {
        "file": "E:/samp/gamemodes/mymode.pwn",
        "line": 456,
        "original_line": "    format(string, sizeof(string), \"你的等级：%d\", level);"
    }
]
```


### 5. 配合 AI 翻译示例

假设你希望用 ChatGPT/DeepSeek 等 AI 批量翻译这些文本：

1. 从 `translate.json` 中提取所有 `original_line` 的内容。
2. 将纯文本列表发送给 AI
3. AI 返回翻译后的文本替换回原 JSON 中（注意保留占位符 `%d` 等）。

### 6. 回写源码

```bash
python replace.py
```

脚本会读取 translate.json，根据文件路径和行号，将修改后的内容写回原文件

## 配置说明

### `export.py`

- `ignore_keys`：列表，包含关键词的行将被忽略（高优先级）
- `target_keys`：列表，触发提取的关键词
