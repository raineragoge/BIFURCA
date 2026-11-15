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
    assert not errors, errors
    context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for reduced, mobile in [(False, False), (True, False), (False, True)]:
        run_check(browser, reduced=reduced, mobile=mobile)
    browser.close()

print('PASS: ramas, SVG, datos locales, motion reducido, escritorio y móvil')
