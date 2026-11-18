# -*- coding: utf-8 -*-
"""
產生 b/ds2.html：B 類第一關（拱／字即建築）的 A/B 對照頁。

做法：讀已建置好的 b/index.html，在 </body> 前塞一層 overlay（CSS + 小段 JS + 切換鈕）。
原始的 b/index.html 一個 byte 都不動——12/1 易用性測試的標的是它，不能碰。
ds2.html 與 index.html 同資料夾，共用 assets-b/，不需要再上傳 135MB 資產。

用法：python3 tools/build-ds2.py [--check]
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, 'b', 'index.html')
# --head：改用 git HEAD 版的 b/index.html 當底。對照頁要跟線上已發布的版本同底，
# 工作目錄裡可能混著別的 session 正在進行的修改，拿來過稿會對到還沒定案的東西。
if '--head' in sys.argv:
    import subprocess
    SRC = None
OUT  = os.path.join(ROOT, 'b', 'ds2.html')

OVERLAY = u'''
<!-- ===== DS2 對照層｜B 類第一關：拱＋字即建築 ===== -->
<style id="ds2css">
/* 三段狀態，由 <html> 的 class 控制：
   （無 class）現況　｜　.ds2a 提案 A：拱在下緣　｜　.ds2b 提案 B：拱在頂緣
   拿掉 class 就完全是現況，這一層不覆寫任何現況樣式。                        */

/* ---------- 語言二：拱 ----------
   矢高 = 跨距 × 0.23（館徽實測：拱頂 279×64）
   用 border-radius 的橢圓語法：水平半徑 50%（＝跨距一半），垂直半徑由 JS 依實際寬度算成 px。
   兩個角各佔一半寬，接起來就是一條完整橢圓弧，矢高精準等於 0.23 × 寬。
   （JS 設 inline style 的地方要 !important：展覽頁 hero 捲動收合時會寫 borderRadius）  */

/* A：拱在下緣——影像底邊拱形，下方內容由拱底升起（設計系統 §2.2 原寫法） */
html.ds2a body #hero,
html.ds2a body .exhero.ins{
  border-radius:20px 20px 50% 50% / 20px 20px var(--arch-r,80px) var(--arch-r,80px) !important;
}

/* B：拱在頂緣——影像頂邊成屋頂，文字在拱下。內容要讓出矢高，否則會被切到 */
html.ds2b body #hero,
html.ds2b body .exhero.ins{
  border-radius:50% 50% 20px 20px / var(--arch-r,80px) var(--arch-r,80px) 20px 20px !important;
}
html.ds2b body #hero .plaque{ margin-top:calc(var(--arch-r,80px) * .62) !important; }
html.ds2b body .hline{ top:calc(24px + var(--arch-r,80px) * .62) !important; }

/* 底部面板頂緣：兩案都一樣，取代 border-radius:24px 24px 0 0 */
html.ds2a body .sheet,
html.ds2b body .sheet{
  border-radius:50% 50% 0 0 / var(--arch-r,80px) var(--arch-r,80px) 0 0 !important;
}

/* ---------- 語言三：字即建築 ----------
   堆疊式英文大標。只改行高與字距，不換字體（§2.3 選項 A，零成本）。 */
html.ds2a body #hero .plaque h1,
html.ds2b body #hero .plaque h1{
  line-height:.98 !important;
  letter-spacing:-.015em !important;
}
/* 左側金柱高度改為綁定文字塊，不再寫死 236px */
html.ds2a body .hline,
html.ds2b body .hline{ height:var(--hline-h,236px) !important; }
</style>

<style id="ds2ui">
#ds2btn{
  position:fixed; left:12px; bottom:calc(12px + env(safe-area-inset-bottom,0px)); z-index:99999;
  display:flex; align-items:center; gap:7px;
  min-height:36px; padding:0 13px 0 10px; border:0; border-radius:18px;
  background:rgba(20,28,32,.84); color:#fff; font:500 13px/1 system-ui,-apple-system,"Noto Sans TC",sans-serif;
  -webkit-backdrop-filter:blur(8px); backdrop-filter:blur(8px);
  box-shadow:0 4px 14px rgba(0,0,0,.3); cursor:pointer; user-select:none;
}
#ds2btn i{ width:8px; height:8px; border-radius:4px; background:#8A8F92; display:block }
html.ds2a #ds2btn i{ background:#C9A961 }
html.ds2b #ds2btn i{ background:#6FA8BC }
#ds2btn b{ font-weight:500; white-space:nowrap }
#ds2btn small{ font-weight:400; font-size:11px; opacity:.62; font-variant-numeric:tabular-nums; white-space:nowrap }
</style>

<button id="ds2btn" type="button" aria-live="polite">
  <i aria-hidden="true"></i><b>現況</b><small></small>
</button>

<script>
(function(){
  var R = document.documentElement, btn = document.getElementById('ds2btn');
  var lab = btn.querySelector('b'), num = btn.querySelector('small');
  var STATES = ['', 'ds2a', 'ds2b'];
  var NAMES  = { '': '現況', 'ds2a': '提案 A・拱在下緣', 'ds2b': '提案 B・拱在頂緣' };
  var cur = 0;

  /* 只在數值真的變了才寫。寫入本身會再觸發下面的 MutationObserver，
     不擋就是無限迴圈，整頁會卡死（2026-11-18 實測踩到）。 */
  function setVar(el, name, val){
    if(el.style.getPropertyValue(name) !== val) el.style.setProperty(name, val);
  }

  function archSync(){
    var w = 0;
    ['#hero', '.exhero.ins', '.sheet'].forEach(function(sel){
      Array.prototype.forEach.call(document.querySelectorAll(sel), function(el){
        var bw = el.getBoundingClientRect().width;
        if(!bw) return;
        setVar(el, '--arch-r', (bw * 0.23).toFixed(1) + 'px');
        if(sel === '#hero') w = bw;
      });
    });
    /* 金柱高度 = 說明牌文字塊實際高度 */
    Array.prototype.forEach.call(document.querySelectorAll('#hero .plaque'), function(p){
      var h = p.getBoundingClientRect().height;
      if(h) setVar(p.parentElement, '--hline-h', Math.round(h - 24) + 'px');
    });
    var txt = (cur && w) ? Math.round(w) + '×0.23=' + Math.round(w * 0.23) : '';
    if(num.textContent !== txt) num.textContent = txt;
  }

  /* 整頁靠 JS 重繪，要跟著重算；用 rAF 併批，一次重繪只跑一次 */
  var pend = false;
  function schedule(){
    if(pend) return;
    pend = true;
    requestAnimationFrame(function(){ pend = false; archSync(); });
  }

  function paint(){
    STATES.forEach(function(c){ if(c) R.classList.remove(c); });
    if(STATES[cur]) R.classList.add(STATES[cur]);
    lab.textContent = NAMES[STATES[cur]];
    btn.setAttribute('aria-label', '目前是「' + NAMES[STATES[cur]] + '」，按一下換下一版');
    try{ sessionStorage.setItem('ds2', String(cur)); }catch(e){}
    archSync();
  }

  btn.addEventListener('click', function(){ cur = (cur + 1) % STATES.length; paint(); });

  /* 起始狀態：網址帶 ds=1／ds=2 直接指定；否則沿用這個分頁上次看的 */
  var q = (location.search + location.hash).match(/ds=([012])/), mem = null;
  try{ mem = sessionStorage.getItem('ds2'); }catch(e){}
  cur = q ? +q[1] : (mem !== null ? +mem : 0);
  if(!(cur >= 0 && cur < STATES.length)) cur = 0;
  paint();

  addEventListener('resize', schedule);
  addEventListener('orientationchange', schedule);
  new MutationObserver(schedule).observe(document.body, {childList:true, subtree:true});
})();
</script>
<!-- ===== /DS2 對照層 ===== -->
'''

def build():
    if SRC is None:
        import subprocess
        html = subprocess.check_output(
            ['git', 'show', 'HEAD:b/index.html'], cwd=ROOT).decode('utf-8')
    else:
        with io.open(SRC, encoding='utf-8') as f:
            html = f.read()
    if '</body>' in html:
        out = html.replace('</body>', OVERLAY + '\n</body>', 1)
    else:
        out = html + OVERLAY
    out = out.replace('<title>', '<title>[對照] ', 1)
    return out

if __name__ == '__main__':
    built = build()
    if '--check' in sys.argv:
        cur = io.open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
        print('b/ds2.html 與 b/index.html 一致' if cur == built else 'b/ds2.html 已過期，請重跑 build-ds2.py')
        sys.exit(0 if cur == built else 1)
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(built)
    print('b/ds2.html 已產生（%d bytes）' % len(built.encode('utf-8')))
