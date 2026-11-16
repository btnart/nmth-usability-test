#!/usr/bin/env python3
"""把 src/app-b.html 包進 src/shell-b.html，產生 GitHub Pages 用的 b/index.html。

編輯源是 src/app-b.html（等同發布成 Artifact 的那份內容，不含 <html>/<head>）。
b/index.html 是產出物，不要手動編輯——改了也會被下一次 build 蓋掉。

用法：python3 tools/build-b.py [--check]
  --check  只比對、不寫入；產出物與現有檔案不符時以結束碼 1 離開。
"""
import io, os, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(ROOT, 'src', 'shell-b.html')
APP   = os.path.join(ROOT, 'src', 'app-b.html')
OUT   = os.path.join(ROOT, 'b', 'index.html')
MARK  = '<!--APP-->'

def read(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()

def main():
    shell = read(SHELL)
    if MARK not in shell:
        sys.exit(f'外殼 {SHELL} 裡找不到佔位標記 {MARK}')
    out = shell.replace(MARK, read(APP))

    if '--check' in sys.argv:
        cur = read(OUT) if os.path.exists(OUT) else None
        if cur == out:
            print('b/index.html 與 src/ 一致')
            return
        sys.exit('b/index.html 與 src/ 不一致，請執行：python3 tools/build-b.py')

    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'已產生 {os.path.relpath(OUT, ROOT)}（{len(out)} 字元）')

if __name__ == '__main__':
    main()
