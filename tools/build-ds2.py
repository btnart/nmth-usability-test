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
html.ds2 body #hero .plaque h1{
  line-height:.98 !important;
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
   2026-11-18：拱被否決後，柱列的意象改由「動作」承載。
   照館徽的節奏把落地頁背景切成 7 條（4 柱 + 3 隙，隙:柱 = 1:1，見設計系統 R1／R2）：
     第 1 段　3 道「隙」落下消失 → 照片裡浮出館徽的柱列
     第 2 段　4 根「柱」向中央合攏 → 收成一個整體，再交給首頁
   整段約 850ms（隙落 60–400ms ／ 柱列定格 400–500ms ／ 合攏 500–840ms），只在進站時發生一次。prefers-reduced-motion 開啟時直接走現況。 */
(function(){
  var R = document.documentElement;
  var N = 7, PILLARS = [0,2,4,6], GAPS = [1,3,5];
  var EZ = 'cubic-bezier(.2,.8,.2,1)';

  function run(landing, done){
    var img = landing.querySelector('.lbg');
    if(!img || !img.naturalWidth) return done();

    var r = landing.getBoundingClientRect(), W = r.width, H = r.height;
    /* 複製 object-fit:cover 的結果，讓 7 條接起來仍是同一張連續的照片 */
    var k = Math.max(W / img.naturalWidth, H / img.naturalHeight);
    var bw = img.naturalWidth * k, bh = img.naturalHeight * k;
    var ox = (W - bw) / 2, oy = (H - bh) / 2;
    var sw = W / N;

    var layer = document.createElement('div');
    layer.className = 'ds2cols';
    layer.style.cssText = 'position:absolute;inset:0;overflow:hidden;background:#0f212b;z-index:1';

    var strips = [];
    for(var i = 0; i < N; i++){
      var d = document.createElement('div');
      d.style.cssText = 'position:absolute;top:0;bottom:0;left:' + (i * sw) + 'px;width:' + (sw + 0.6) + 'px;'
        + 'background-image:url(' + img.currentSrc + ');'
        + 'background-size:' + bw + 'px ' + bh + 'px;'
        + 'background-position:' + (ox - i * sw) + 'px ' + oy + 'px;'
        + 'will-change:transform,opacity';
      layer.appendChild(d);
      strips.push(d);
    }
    img.style.visibility = 'hidden';
    landing.insertBefore(layer, img.nextSibling);

    /* 第 1 段：隙落下。由中間往兩側，讓柱列「長出來」而不是整排一起消失 */
    var order = [3, 1, 5];
    order.forEach(function(gi, n){
      strips[gi].animate(
        [{transform:'translateY(0)', opacity:1}, {transform:'translateY(18px)', opacity:0}],
        {duration:240, delay:60 + n * 50, easing:'cubic-bezier(.4,0,1,1)', fill:'forwards'});
    });

    /* 第 2 段：柱合攏。4 根收成連續的一塊，位置對稱 */
    var closedLeft = (W - PILLARS.length * sw) / 2;
    PILLARS.forEach(function(pi, n){
      var dx = (closedLeft + n * sw) - pi * sw;
      /* 位移的同時把背景位置一起推回去：合攏後 4 根柱接成的是一張完整連續的照片，
         不是四片拼貼。少了這一段，收起來會看到接縫錯開。 */
      var bx0 = ox - pi * sw;
      var bx1 = ox - closedLeft - n * sw;
      strips[pi].animate(
        [{transform:'translateX(0)',               backgroundPositionX: bx0 + 'px'},
         {transform:'translateX(' + dx + 'px)',    backgroundPositionX: bx1 + 'px'}],
        {duration:340, delay:500, easing:EZ, fill:'forwards'});
    });

    setTimeout(function(){ done(); }, 850);
  }

  /* 包住原本的 leaveLanding：提案版走柱列轉場，現況版原封不動 */
  var orig = window.leaveLanding;
  if(typeof orig !== 'function') return;
  window.leaveLanding = function(){
    var landing = document.querySelector('#app > .scr.landing');
    var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(!R.classList.contains('ds2') || !landing || reduced) return orig.apply(this, arguments);
    landing.classList.add('leaving', 'ds2leave');
    run(landing, function(){ setLang(S.lang); });
  };

  /* 轉場只在進站發生一次，看完要能重看 */
  var again = document.createElement('button');
  again.id = 'ds2again';
  again.type = 'button';
  again.textContent = '重看轉場';
  again.onclick = function(){ location.reload(); };
  document.body.appendChild(again);
  function showAgain(){
    var onLanding = !!document.querySelector('#app > .scr.landing');
    again.style.display = onLanding ? 'none' : 'flex';
  }
  showAgain();
  new MutationObserver(showAgain).observe(document.body, {childList:true, subtree:true});
})();
</script>
<style>
/* 提案版自己接管背景，原本的放大打亮不要同時跑 */
html.ds2 .landing.ds2leave .lbg{ animation:none !important }
#ds2again{
  position:fixed; left:122px; bottom:calc(12px + env(safe-area-inset-bottom,0px)); z-index:99999;
  display:none; align-items:center; min-height:36px; padding:0 13px; border:0; border-radius:18px;
  background:rgba(20,28,32,.84); color:#fff; font:500 13px/1 system-ui,-apple-system,"Noto Sans TC",sans-serif;
  -webkit-backdrop-filter:blur(8px); backdrop-filter:blur(8px);
  box-shadow:0 4px 14px rgba(0,0,0,.3); cursor:pointer;
}
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
