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
<!-- ===== DS2 對照層｜字即建築 ===== -->
<!-- 2026-11-18：原本還有「拱」，使用者否決整條語言，已移除。見設計系統 §2.2。 -->
<style id="ds2css">
/* 兩段狀態：（無 class）現況　｜　.ds2 提案。拿掉 class 就完全是現況。 */

/* ---------- 語言：字即建築（設計系統 §2.3）----------
   堆疊式英文大標。只改行高與字距，不換字體（選項 A，零成本）。 */
/* 2026-11-19：行距改回原本（使用者指定）。只收字距，不壓行高。 */
html.ds2 body #hero .plaque h1{
  letter-spacing:-.015em !important;
}
/* 左側金柱高度改為綁定文字塊，不再寫死 236px（四語系下文字塊高度不同） */
html.ds2 body .hline{ height:var(--hline-h,236px) !important; }
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
html.ds2 #ds2btn i{ background:#C9A961 }
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

  /* 只在數值真的變了才寫。寫入本身會再觸發下面的 MutationObserver，
     不擋就是無限迴圈，整頁會卡死（2026-11-18 實測踩到）。 */
  function setVar(el, name, val){
    if(el.style.getPropertyValue(name) !== val) el.style.setProperty(name, val);
  }

  function sync(){
    var h = 0;
    Array.prototype.forEach.call(document.querySelectorAll('#hero .plaque'), function(p){
      var ph = p.getBoundingClientRect().height;
      if(!ph) return;
      h = Math.round(ph - 24);
      setVar(p.parentElement, '--hline-h', h + 'px');
    });
    var on = R.classList.contains('ds2');
    var txt = (on && h) ? '金柱 ' + h + 'px' : (h ? '金柱 236px（寫死）' : '');
    if(num.textContent !== txt) num.textContent = txt;
  }

  /* 整頁靠 JS 重繪，要跟著重算；用 rAF 併批，一次重繪只跑一次 */
  var pend = false;
  function schedule(){
    if(pend) return;
    pend = true;
    requestAnimationFrame(function(){ pend = false; sync(); });
  }

  function paint(){
    var on = R.classList.contains('ds2');
    lab.textContent = on ? '提案・字即建築' : '現況';
    btn.setAttribute('aria-label', (on ? '目前是提案版' : '目前是現況版') + '，按一下切換');
    try{ sessionStorage.setItem('ds2', on ? '1' : '0'); }catch(e){}
    sync();
  }

  btn.addEventListener('click', function(){ R.classList.toggle('ds2'); paint(); });

  /* 起始狀態：網址帶 ds=0／ds=1 就以網址為準（兩邊都要能強制指定，
     否則 sessionStorage 的記憶會蓋掉 ?ds=0，切不回現況）；沒帶才沿用這個分頁上次看的 */
  var q = (location.search + location.hash).match(/ds=([01])/), mem = null;
  try{ mem = sessionStorage.getItem('ds2'); }catch(e){}
  var on = q ? q[1] === '1' : mem === '1';
  R.classList.toggle('ds2', on);
  paint();

  addEventListener('resize', schedule);
  addEventListener('orientationchange', schedule);
  new MutationObserver(schedule).observe(document.body, {childList:true, subtree:true});
})();
</script>

<script>
/* ===== 柱列轉場（landing → 首頁）=====
   2026-11-19：動態從 logo 本身開始。
   logo 裡本來就是 4 柱 + 3 隙（實測 logo-sprite.png 第一格 97x100：
   柱各寬 11、隙各寬 10、隙/柱 = 0.909、柱列帶 x9–82 y25–71、色 rgb(171,142,70)），
   所以不是「把照片切成柱狀」，是「把 logo 的柱列撐開成整個畫面」：

     0–400ms   落地頁的 logo 原地放大，柱列帶撐滿全螢幕；
               金色柱子裡換成照片，隙的位置沉成深色，柱子長出稜線
     400–600   定格（絕對靜止，長度可用 ?hold= 調）
     600–930   4 根柱向中央合攏（外層窗口 +dx／內層影像 −dx，影像在螢幕上其實沒動）
     850       交棒給首頁，刻意疊在合攏最後 80ms
     930–1030  整層淡出移除

   prefers-reduced-motion 開啟時整段跳過，走原本的淡入。 */
(function(){
  var R = document.documentElement;
  var N = 7, PILLARS = [0,2,4,6], GAPS = [1,3,5];
  var EZ_OUT = 'cubic-bezier(.4,0,1,1)';
  var EZ_MERGE = 'cubic-bezier(.65,0,.3,1)';
  var EZ_FORM = 'cubic-bezier(.2,.7,.3,1)';
  var FORM_END = 400, MERGE_DUR = 330;
  var LOGO = 'assets-b/logo-sprite.png';
  var GOLD = '#AB8E46';
  /* 柱列帶在 logo 格子裡的位置，用 logo-sprite.png 實測（格寬 504/5.2466 = 96.06） */
  var BAND = { x:9/96.06, w:74/96.06, y:25/100, h:47/100 };

  var DROP = '0 0 28px 6px rgba(0,0,0,.42)';
  function edgeShadow(sw){
    /* 1px 亮邊（邊緣接到光）＋ 內縮暗邊（內側自己有陰影）。
       暗邊尺寸要跟著柱寬算，固定值在窄柱上會從兩側蓋滿整條，把照片壓成濾鏡感。 */
    var o = Math.max(4, Math.round(sw * 0.10)), b = Math.round(sw * 0.30);
    return 'inset 1px 0 0 rgba(255,255,255,.18), inset -1px 0 0 rgba(255,255,255,.18),'
         + 'inset ' + o + 'px 0 ' + b + 'px ' + (-o) + 'px rgba(0,0,0,.42),'
         + 'inset ' + (-o) + 'px 0 ' + b + 'px ' + (-o) + 'px rgba(0,0,0,.42)';
  }

  function hold(){
    var m = (location.search + location.hash).match(/hold=([0-9]{1,3})/);
    return Math.max(0, Math.min(800, m ? +m[1] : 200));
  }

  /* 落地頁本來沒有 logo。只在提案版補上去，現況完全不動。 */
  function mountLogo(){
    var landing = document.querySelector('#app > .scr.landing');
    if(!landing) return null;
    var col = landing.lastElementChild;
    if(!col) return null;
    var el = col.querySelector('.ds2logo');
    if(!R.classList.contains('ds2')){ if(el) el.remove(); return null; }
    if(!el){
      el = document.createElement('span');
      el.className = 'ds2logo';
      el.style.cssText = 'width:56px;height:58.3px;overflow:hidden;position:relative;display:block;flex:0 0 auto';
      el.innerHTML = '<img src="' + LOGO + '" alt="" style="position:absolute;left:0;top:0;'
                   + 'height:100%;width:524.66%;max-width:none">';
      col.insertBefore(el, col.firstChild);
    }
    return el;
  }

  function run(landing, done){
    var img = landing.querySelector('.lbg');
    if(!img || !img.naturalWidth) return done();
    var logoEl = mountLogo();

    var r = landing.getBoundingClientRect(), W = r.width, H = r.height;
    var k = Math.max(W / img.naturalWidth, H / img.naturalHeight);
    var bw = img.naturalWidth * k, bh = img.naturalHeight * k;
    var ox = (W - bw) / 2, oy = (H - bh) / 2;
    var sw = W / N, EDGE = edgeShadow(sw);

    /* 圖層掛在 body：交棒時 landing 會被重繪掉，但合攏的最後 80ms 要疊在首頁淡入上 */
    var layer = document.createElement('div');
    layer.className = 'ds2cols';
    layer.style.cssText = 'position:fixed;inset:0;overflow:hidden;z-index:9998;pointer-events:none';

    /* 底：撐開的過程中要讓落地頁照片透出來（才像 logo 在長大），
       撐滿之後才沉成深色，當作「隙」的底。 */
    var back = document.createElement('div');
    back.style.cssText = 'position:absolute;inset:0;background:#0f212b;opacity:0;will-change:opacity';
    layer.appendChild(back);

    /* 柱列網格：整組一起做「從 logo 撐開」的縮放 */
    var grid = document.createElement('div');
    grid.style.cssText = 'position:absolute;inset:0;transform-origin:0 0;will-change:transform';
    layer.appendChild(grid);

    var cols = [], imgs = [];
    for(var i = 0; i < N; i++){
      var L = Math.round(i * sw), isP = PILLARS.indexOf(i) >= 0;
      var col = document.createElement('div');
      col.style.cssText = 'position:absolute;top:0;bottom:0;left:' + L + 'px;'
        + 'width:' + (Math.round(sw) + 1) + 'px;overflow:hidden;will-change:transform;'
        + (isP ? 'background:' + GOLD : 'background:transparent');
      if(isP){
        var im = document.createElement('div');
        im.style.cssText = 'position:absolute;top:0;bottom:0;left:' + (-L) + 'px;width:' + W + 'px;opacity:0;'
          + 'background-image:url(' + img.currentSrc + ');'
          + 'background-size:' + bw + 'px ' + bh + 'px;'
          + 'background-position:' + ox + 'px ' + oy + 'px;will-change:transform,opacity';
        col.appendChild(im);
        imgs[i] = im;
      }
      grid.appendChild(col);
      cols.push(col);
    }
    document.body.appendChild(layer);

    /* 第 1 拍：從 logo 的柱列帶撐開到全螢幕 */
    if(logoEl){
      var lr = logoEl.getBoundingClientRect();
      var sx = (BAND.w * lr.width) / W, sy = (BAND.h * lr.height) / H;
      var tx = lr.left + BAND.x * lr.width, ty = lr.top + BAND.y * lr.height;
      grid.animate([
        {transform:'translate(' + tx + 'px,' + ty + 'px) scale(' + sx + ',' + sy + ')'},
        {transform:'translate(0px,0px) scale(1,1)'}
      ], {duration:340, delay:60, easing:EZ_FORM, fill:'both'});
      logoEl.style.visibility = 'hidden';   /* 由撐開的柱列接手 */
    }

    back.animate([{opacity:0},{opacity:1}],
      {duration:140, delay:260, easing:EZ_FORM, fill:'forwards'});
    PILLARS.forEach(function(pi){
      /* 金色換成照片：等縮放快結束才換，否則照片會被拉變形 */
      imgs[pi].animate([{opacity:0},{opacity:1}],
        {duration:100, delay:300, easing:'linear', fill:'forwards'});
      cols[pi].animate([{boxShadow:'none'}, {boxShadow:EDGE}],
        {duration:220, delay:180, easing:EZ_FORM, fill:'forwards'});
    });

    var H0 = hold(), mStart = FORM_END + H0, mEnd = mStart + MERGE_DUR;

    /* 第 2 拍：合攏。外層窗口 +dx、內層影像 −dx，影像在螢幕座標上完全沒動 */
    var closedLeft = (W - PILLARS.length * sw) / 2;
    PILLARS.forEach(function(pi, n){
      var dx = (closedLeft + n * sw) - pi * sw;
      var o = {duration:MERGE_DUR, delay:mStart, easing:EZ_MERGE, fill:'forwards'};
      cols[pi].animate([{transform:'translateX(0)'}, {transform:'translateX(' + dx + 'px)'}], o);
      imgs[pi].animate([{transform:'translateX(0)'}, {transform:'translateX(' + (-dx) + 'px)'}], o);
    });

    setTimeout(function(){
      PILLARS.forEach(function(pi){ cols[pi].style.boxShadow = EDGE + ',' + DROP; });
    }, mStart);
    setTimeout(function(){
      PILLARS.forEach(function(pi){
        cols[pi].animate([{boxShadow:EDGE + ',' + DROP}, {boxShadow:EDGE}],
          {duration:80, easing:'ease-in', fill:'forwards'});
      });
    }, mEnd - 80);

    setTimeout(done, mEnd - 80);
    setTimeout(function(){
      layer.animate([{opacity:1},{opacity:0}], {duration:100, easing:'linear', fill:'forwards'})
        .onfinish = function(){ layer.remove(); };
    }, mEnd);
  }

  var orig = window.leaveLanding;
  if(typeof orig !== 'function') return;
  window.leaveLanding = function(){
    var landing = document.querySelector('#app > .scr.landing');
    var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(!R.classList.contains('ds2') || !landing || reduced) return orig.apply(this, arguments);
    landing.classList.add('leaving', 'ds2leave');
    run(landing, function(){ setLang(S.lang); });
  };

  var again = document.createElement('button');
  again.id = 'ds2again';
  again.type = 'button';
  again.textContent = '重看轉場';
  again.onclick = function(){ location.reload(); };
  document.body.appendChild(again);

  function sync(){
    mountLogo();
    again.style.display = document.querySelector('#app > .scr.landing') ? 'none' : 'flex';
  }
  sync();
  document.getElementById('ds2btn').addEventListener('click', function(){ setTimeout(sync, 0); });
  new MutationObserver(sync).observe(document.body, {childList:true, subtree:true});
})();
</script>
<style>
/* 提案版自己接管背景，原本的放大打亮不要同時跑 */
html.ds2 .landing.ds2leave .lbg{ animation:none !important }
/* 2026-11-19：落地頁在提案版多了一顆 logo（插在內容欄最前面），
   所以進場／離場的 nth-child 延遲全部往後移一位，logo 自己另外處理。
   原本的 lout 是 .4s + 6 個元素各差 .04s，最後一個結束在 600ms，
   整個「定格」期間文字都還在往上飛——定格等於不存在。壓縮成 310ms 結束，
   位移從 −24px 收到 −16px，曲線跟轉場的離場統一。 */
/* 進場也往後移一位 */
html.ds2 .landing.enter>div:last-child>.ds2logo{ animation-delay:.05s !important }
html.ds2 .landing.enter>div:last-child>:nth-child(2){ animation-delay:.15s !important }
html.ds2 .landing.enter>div:last-child>:nth-child(3){ animation-delay:.3s !important }
html.ds2 .landing.enter>div:last-child>:nth-child(4){ animation-delay:.5s !important }
html.ds2 .landing.enter>div:last-child>:nth-child(5){ animation-delay:.65s !important }
html.ds2 .landing.enter>div:last-child>:nth-child(6){ animation-delay:.8s !important }
html.ds2 .landing.enter>div:last-child>:nth-child(7){ animation-delay:.95s !important }

@keyframes ds2out{ to{ opacity:0; transform:translateY(-16px) } }
html.ds2 .landing.ds2leave>div:last-child>*{
  animation:ds2out .22s cubic-bezier(.4,0,1,1) both !important }
html.ds2 .landing.ds2leave>div:last-child>:nth-child(2){ animation-delay:0s !important }
html.ds2 .landing.ds2leave>div:last-child>:nth-child(3){ animation-delay:.018s !important }
html.ds2 .landing.ds2leave>div:last-child>:nth-child(4){ animation-delay:.036s !important }
html.ds2 .landing.ds2leave>div:last-child>:nth-child(5){ animation-delay:.054s !important }
html.ds2 .landing.ds2leave>div:last-child>:nth-child(6){ animation-delay:.072s !important }
html.ds2 .landing.ds2leave>div:last-child>:nth-child(7){ animation-delay:.09s !important }
/* logo 不跟著文字飛走——它是被撐開的那個，由 JS 接手 */
html.ds2 .landing.ds2leave>div:last-child>.ds2logo{ animation:none !important }

</style>
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
