"""Regresión de motion en BIFURCA: ramas, SVG, persistencia y accesibilidad.

Ejecutar desde la raíz del proyecto:
    python -m http.server 8013
    python tests/qa_motion.py

Requiere: pip install playwright && python -m playwright install chromium
"""
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8013/"


def seeded_tree(page):
    page.evaluate("""() => {
      const key = 'bifurca_v3_app';
      const state = JSON.parse(localStorage.getItem(key));
      if (!state) throw new Error('BIFURCA debe inicializar localStorage antes de la prueba');
      const n = (id, title, children = []) => ({
        id, title, children, notes: '', description: '', example: '',
        status: 'neutral', collapsed: false, expanded: false
      });
      state.docs.push({
        id: 'motion-qa-map', kind: 'knowledge', name: 'QA Motion',
        root: n('motion-r', 'Raíz', [
          n('motion-a', 'Primera rama', [
            n('motion-c', 'Concepto C'), n('motion-d', 'Concepto D')
          ]),
          n('motion-b', 'Segunda rama', [n('motion-e', 'Concepto E')])
        ]),
        links: [], auxNodes: [], legend: {neutral:'Sin clasificar', positive:'Importante', warning:'Pendiente', negative:'Problema', info:'Referencia'}, updatedAt: Date.now()
      });
      state.activeId = 'motion-qa-map';
      localStorage.setItem(key, JSON.stringify(state));
    }""")
    page.reload(wait_until="domcontentloaded")
    page.locator(".node[data-id='motion-r']").wait_for()


def run_check(browser, reduced=False, mobile=False):
    context = browser.new_context(
        viewport={'width': 390 if mobile else 1400, 'height': 800},
        is_mobile=mobile, has_touch=mobile,
        reduced_motion='reduce' if reduced else 'no-preference'
    )
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    assert page.goto(URL, wait_until='domcontentloaded').status == 200
    seeded_tree(page)
    assert page.evaluate("typeof window.BIFURCA_MOTION?.enterNode") == "function"
    before = page.evaluate("window.BIFURCA_DEBUG.tree()")
    assert page.locator(".node:not([aria-hidden=\"true\"])").count() == 6
    assert page.locator(".connector").count() == 5

    page.locator(".node[data-id='motion-a'] .node-fold").click()
    assert page.evaluate("window.BIFURCA_DEBUG.tree().children[0].collapsed") is True
    assert page.locator(".node:not([aria-hidden=\"true\"])").count() == 4
    page.wait_for_timeout(350)
    assert page.locator(".connector").count() == 3

    page.locator(".node[data-id='motion-a'] .node-fold").click()
    assert page.evaluate("window.BIFURCA_DEBUG.tree().children[0].collapsed") is False
    assert page.locator(".node:not([aria-hidden=\"true\"])").count() == 6
    page.wait_for_timeout(700)
    after = page.evaluate("window.BIFURCA_DEBUG.tree()")
    assert before == after, 'Los datos no deben cambiar tras plegar y desplegar'
    assert page.locator(".connector").count() == 5
    assert page.evaluate("JSON.parse(localStorage.getItem('bifurca_v3_app')).activeId") == 'motion-qa-map'

    # Cambio de tamaño y render no deben perder las conexiones.
    page.set_viewport_size({'width': 900 if not mobile else 390, 'height': 750})
    page.wait_for_timeout(550)
    assert page.locator(".connector").count() == 5
    # A real cross-link survives rapid interruption, navigation, and reload.
    page.locator("[data-id='motion-c'] .node-chain").dispatch_event('click')
    page.locator("[data-id='motion-e']").dispatch_event('click')
    links = page.evaluate("BIFURCA_DEBUG.links()")
    assert len(links) == 1
    root = page.locator("[data-id='motion-r']")
    root.focus()
    page.keyboard.press('ArrowRight')
    assert page.evaluate("document.activeElement.dataset.id") == 'motion-a'
    fold = page.locator("[data-id='motion-a'] .node-fold")
    for _ in range(8):
        fold.dispatch_event('click')
        page.wait_for_timeout(36)
    page.wait_for_timeout(600)
    assert page.locator(".node[aria-hidden=true]").count() == 0
    assert page.locator('.cross-connector').count() == 1

    def camera():
        return page.locator('#scene').evaluate("e=>new DOMMatrix(getComputedStyle(e).transform).toFloat64Array().join(',')")
    previous = camera()
    page.locator('#zoomIn').dispatch_event('click')
    page.wait_for_timeout(380)
    assert camera() != previous
    previous = camera()
    stage = page.locator('#stage').bounding_box()
    # Choose unobstructed canvas so a toolbar or card cannot consume the drag.
    x, y = page.evaluate("""box=>{
      for(let y=box.y+15;y<box.y+box.height-30;y+=21)
        for(let x=box.x+15;x<box.x+box.width-30;x+=21){
          if(['stage','scene','nodeLayer'].includes(document.elementFromPoint(x,y)?.id)) return [x,y];
        }
      throw Error('No free canvas');
    }""", stage)
    page.mouse.move(x,y); page.mouse.down(); page.mouse.move(x+26,y+24,steps=4); page.mouse.up()
    assert camera() != previous
    page.reload(wait_until='load')
    assert page.evaluate("BIFURCA_DEBUG.tree()") == before
    assert page.evaluate("BIFURCA_DEBUG.links()") == links
    assert page.locator('.cross-connector').count() == 1
    # Dense fixture in this context only; test both the animation budget and
    # the SVG endpoint while a visible child moves away from its parent.
    page.evaluate("""() => {
      const state=BIFURCA_DEBUG.state(), doc=state.docs.find(d=>d.id===state.activeId);
      const branch=doc.root.children[0], sample=branch.children[0];
      for(let i=0;i<120;i++) doc.root.children[i%2].children.push({...sample,id:'dense-'+i,title:'Concepto '+i});
      state.settings.treeLayout='horizontal';
      localStorage.setItem('bifurca_v3_app',JSON.stringify(state));
    }""")
    page.reload(wait_until='load')
    assert page.locator('.node').count() == 126
    fold.dispatch_event('click')
    page.wait_for_timeout(250)
    samples = page.evaluate("""async () => {
      document.querySelector('[data-id="motion-a"] .node-fold').click();
      const card=document.querySelector('[data-id="motion-c"]');
      const path=document.querySelector('.connector[data-child="motion-c"]');
      // Seek actual WAAPI flights to reproducible frames, even on a busy CI host.
      const flights=document.getAnimations().filter(a=>a.effect.getKeyframes().some(k=>'translate' in k));
      for(const flight of flights)flight.pause();
      const result=[];
      for(const time of [80,160,240]){
        for(const flight of flights)flight.currentTime=time;
        await new Promise(requestAnimationFrame);
        await new Promise(requestAnimationFrame);
        const translate=getComputedStyle(card).translate;
        const [dx=0,dy=0]=translate==='none'?[]:translate.split(' ').map(parseFloat);
        const end=path.getPointAtLength(path.getTotalLength());
        const error=Math.hypot(end.x-card.offsetLeft-card.offsetWidth/2-dx,end.y-card.offsetTop-dy);
        result.push([error,translate]);
      }
      for(const flight of flights)flight.play();
      return result;
    }""")
    assert max(d for d,_ in samples)<3, (mobile,reduced,samples)
    assert any(v!='none' for _,v in samples) != reduced, (mobile,reduced,samples)
    page.wait_for_timeout(500)
    assert page.locator('.connector').count() == 125
    if reduced:
        assert page.locator('.node').evaluate_all("els=>els.every(e=>!e.getAnimations().some(a=>a.effect.getKeyframes().some(k=>'translate' in k)))")
    assert not errors, errors
    context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for reduced, mobile in [(False, False), (True, False), (False, True)]:
        run_check(browser, reduced=reduced, mobile=mobile)
    browser.close()

print('PASS: ramas, SVG, datos locales, motion reducido, escritorio y móvil')
