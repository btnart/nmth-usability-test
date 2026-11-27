# 原型連結與版本對照

## 第 2 輪測試版（交給館方的版本）

| 項目 | 內容 |
|---|---|
| Repo | https://github.com/btnart/nmth-usability-test |
| 對應 commit | `9fbb9db`（2026-11-25 23:00）：「展名拉線標籤固定在原位，不再因超出畫面或撞到樓層列而推移」 |
| 原始碼 | `src/app-b.html`（編輯源）→ `tools/build-b.py` → `b/index.html`（發布版） |
| **主連結（線上預覽）** | https://pure-jubilee-8hwd.here.now/#nmth |
| 備用連結（GitHub Pages） | https://btnart.github.io/nmth-usability-test/b/#nmth |
| 第 2 輪測試任務頁 | https://btnart.github.io/nmth-usability-test/r2/（原始碼在 repo 的 `r2/index.html`） |

2026-11-27 核對：主連結與備用連結的內容都與 `9fbb9db` 的 `b/index.html` 完全一致。

**兩個連結的關係**：同一個檔案放在兩個網站。主連結（here.now）由設計端手動發布，第 2 輪測試任務頁指向它；備用連結（GitHub Pages）在變更合併到 `main` 後自動更新。兩邊更新時間不同，之後若只更新其中一邊，內容會不一致，以主連結為準。原型為純前端，沒有任何後端請求。

### 第 2 輪測試任務頁的 QR Code

任務頁（`r2/index.html`）內所有 QR Code 與「打開導覽」按鈕，目標都是上表的主連結（`pure-jubilee-8hwd.here.now`），也就是目前最新版，沒有指向舊版原型。測試情境入口以網址參數進入，例如 `#nmth&go=ex:zj`（萬相天后展覽頁）、`#nmth&go=tour:perm:3`（常設展導覽第 3 則）、`#nmth&go=pt:806`（展品 806）。

## 第 1 輪測試版（歷史版本）

- B 版 Claude Artifact：https://claude.ai/artifact/CvwNtrgjMRfrF7Ri79VQ71#nmth（連結是否可開，取決於分享權限）
- 第 1 輪測試頁原始檔：`usability-tests/r1-nmth-usability-test.html`

## 未上傳的大型檔案（僅記錄位置）

下列檔案因含真人聲音或超過 GitHub 單檔建議上限（50 MB），不放進 repo。位置為設計端本機專案資料夾 `nmth-web-guide/` 之下：

| 檔案 | 大小 | 位置 |
|---|---|---|
| 訪談錄音 01_20261006_資深導覽員.m4a | 約 61 MB | `docs/02-需求訪談/錄音/` |
| 訪談錄音 02_20261016_展場服務督導.m4a | 約 32 MB | 同上 |
| 訪談錄音 03_20261022_數位創新中心.m4a | 約 27 MB | 同上 |
| 訪談錄音 04_20261030_公服組營運小組.m4a | 約 21 MB | 同上 |
| 訪談錄音 05_20261030_公服教育組_展場營運組.m4a | 約 49 MB | 同上 |
| 第 1 輪易用性測試錄音 2026-9-18 易用性測試.m4a | 約 23 MB | `docs/07-易用性測試/` |
