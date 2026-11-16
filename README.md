# 臺史博手機導覽原型

可用性測試用的前臺原型，兩個版本並陳：

| | 網址 | 說明 |
|---|---|---|
| 入口 | https://btnart.github.io/nmth-usability-test/ | 版本選擇 |
| A 版 | https://btnart.github.io/nmth-usability-test/a/ | |
| B 版 | https://btnart.github.io/nmth-usability-test/b/ | 目前主要維護的版本 |

## B 版怎麼改

**編輯源是 `src/app-b.html`，不是 `b/index.html`。**

`b/index.html` 是產出物，由 build 腳本把 `src/app-b.html` 包進 `src/shell-b.html`
（`<!doctype>`、`<head>`、meta 那一層外殼）產生。直接改 `b/index.html` 會在下一次
build 被蓋掉。

```bash
# 1. 改 src/app-b.html
# 2. 產生 b/index.html
python3 tools/build-b.py
# 3. 兩個檔案一起 commit
git add src/app-b.html b/index.html && git commit && git push
```

推上 `main` 後 GitHub Pages 會自動重建，約一兩分鐘。

檢查產出物有沒有跟源檔脫節（commit 前跑一次，或接到 CI）：

```bash
python3 tools/build-b.py --check
```

### 為什麼要分成兩個檔案

`src/app-b.html` 同時服務兩個發布管道：

- **Adobe/Claude Artifact**：平台自己會包上 `<!doctype>`、`<html>`、`<head>`，
  所以直接發布 `src/app-b.html` 的內容即可
- **GitHub Pages**：當靜態檔直接送，必須是完整 HTML 文件，所以要補上 `src/shell-b.html`
  那 263 個字元的外殼

兩者差別只有那層外殼，之後一字不差都是 `src/app-b.html`。

### 歷史

2026-11 以前，`app-b.html` 只存在於本機的暫存目錄、沒有進版控，只有產出物
`b/index.html` 會 push。結果是在另一台機器上改了產出物之後，本機只要再同步一次
就會整個蓋掉。把源檔納入 repo 就是為了消除這個問題——現在不管在哪台機器，
改的都是同一個 `src/app-b.html`，衝突由 git 處理。

## A 版

`a/index.html` 仍是單一檔案、沒有拆出源檔，維持原狀直接編輯。
