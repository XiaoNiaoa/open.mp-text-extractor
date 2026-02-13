# -*- coding: gbk -*-

import json
from collections import defaultdict

def replace_lines(translated_file='translate.json'):
    with open(translated_file, 'r', encoding='gbk', errors='ignore') as f:
        translated = json.load(f)
    
    file_groups = defaultdict(list)
    for entry in translated:
        file_groups[entry['file']].append(entry)
    
    for filepath, entries in file_groups.items():
        with open(filepath, 'r', encoding='gbk', errors='ignore') as f:
            lines = f.readlines()
        
        entries.sort(key=lambda e: e['line'], reverse=True)
        
        for entry in entries:
            line_num = entry['line'] - 1 
            original_line_content = lines[line_num]
            
            stripped = original_line_content.rstrip('\r\n')
            original_newline = original_line_content[len(stripped):]
            
            translated_content = entry['original_line']
            
            lines[line_num] = translated_content + original_newline
        
        with open(filepath, 'w', encoding='gbk', newline='') as f:
            f.writelines(lines)
    
    print("翻译替换已完成.")

if __name__ == "__main__":
    replace_lines('translate.json')
