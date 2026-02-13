# -*- coding: gbk -*-
import os
import json

class PawnStatementFinalExtractor:
    def __init__(self, root_dir, tab_size=4):
        self.root_dir = root_dir
        self.tab_size = tab_size
        self.ignore_keys = ['sscanf', 'mysql']
        self.target_keys = [
            'format', 'strcat', 'Msg', 'Error', 'Log', 'Message', 'Show',
            'Warning', 'print', '3DText', 'GameText', 'TextDraw',
            'Dialog', 'ProxDetector', 'SCM', 'Debug',
        ]
        self.results = []

    def process_line(self, line, in_string):
        code_chars = []
        has_quote = False
        i = 0
        n = len(line)
        escaped = False
        while i < n:
            ch = line[i]
            if not in_string:
                if ch == '"' and not escaped:
                    in_string = True
                    has_quote = True
                else:
                    code_chars.append(ch)
                if ch == '\\' and not escaped:
                    escaped = True
                else:
                    escaped = False
                i += 1
            else:
                if ch == '"' and not escaped:
                    in_string = False
                    has_quote = True
                else:
                    pass
                if ch == '\\' and not escaped:
                    escaped = True
                else:
                    escaped = False
                i += 1
        return in_string, ''.join(code_chars), has_quote

    def preprocess_file(self, lines):
        info_list = []
        in_string = False
        for idx, line in enumerate(lines):
            raw = line.expandtabs(self.tab_size).rstrip('\n').rstrip('\r')
            in_string, code, has_quote = self.process_line(raw, in_string)
            info_list.append({
                'raw': raw,
                'line_num': idx + 1,
                'code': code,
                'has_quote': has_quote
            })
        return info_list

    def process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return

        info_list = self.preprocess_file(lines)
        i = 0
        while i < len(info_list):
            info = info_list[i]
            code = info['code']

            if any(ignore in code for ignore in self.ignore_keys):
                i += 1
                continue

            if not any(target in code for target in self.target_keys):
                i += 1
                continue

            if '{' in code:
                i += 1
                continue

            if i + 1 < len(info_list):
                next_code = info_list[i+1]['code']
                if '{' in next_code:
                    i += 1
                    continue

            if ';' in code:
                if info['has_quote']:
                    self.results.append({
                        "file": os.path.abspath(file_path),
                        "line": info['line_num'],
                        "original_line": info['raw']
                    })
                i += 1
            else:
                statement = []
                has_quote_in_stmt = info['has_quote']
                statement.append({
                    "file": os.path.abspath(file_path),
                    "line": info['line_num'],
                    "original_line": info['raw']
                })
                j = i + 1
                capturing = True
                while j < len(info_list) and capturing:
                    cur_info = info_list[j]
                    cur_code = cur_info['code']

                    if any(ignore in cur_code for ignore in self.ignore_keys):
                        statement = []
                        capturing = False
                        j += 1
                        break

                    statement.append({
                        "file": os.path.abspath(file_path),
                        "line": cur_info['line_num'],
                        "original_line": cur_info['raw']
                    })
                    if cur_info['has_quote']:
                        has_quote_in_stmt = True

                    if ';' in cur_code:
                        if has_quote_in_stmt:
                            self.results.extend(statement)
                        capturing = False
                        j += 1
                        break

                    j += 1

                i = j

    def run(self):
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.lower().endswith(('.pwn', '.inc')):
                    self.process_file(os.path.join(root, file))
        self.save_json()

    def save_json(self):
        try:
            with open('translate.json', 'w', encoding='gbk') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=4)
            print(f"提取完成！共找到 {len(self.results)} 条记录")
        except Exception as e:
            print(f"保存失败: {e}")

if __name__ == "__main__":
    scanner = PawnStatementFinalExtractor(r'E:\samp\files\gamemodes\SP-RP-main\gamemodes')
    scanner.run()
