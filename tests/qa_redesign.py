"""Playwright QA on a fresh, isolated browser profile; never opens a personal profile."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = 'http://127.0.0.1:8012/'
OUT = Path(__file__).resolve().parent / 'captures'
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    assert page.goto(BASE, wait_until='domcontentloaded').status == 200
    expect(page.locator('.node')).to_have_count(8)
    expect(page.locator('#mapHeadingCount')).to_contain_text('46 conceptos · 8 visibles')
    initial_storage = page.evaluate("Object.keys(localStorage).sort()")
    assert 'bifurca_v3_app' in initial_storage
    page.screenshot(path=str(OUT / '01-escritorio.png'))

    page.locator('#moreTools summary').click()
    expect(page.locator('#exportBtn')).to_be_visible()
    expect(page.locator('#themeBtn')).to_be_visible()
    expect(page.locator('#soundBtn')).to_be_visible()
    page.locator('#moreTools summary').click()

    page.locator('.node').nth(1).click()
    expect(page.locator('#conceptPanel')).to_be_visible()
    expect(page.locator('#conceptTitle')).to_have_text('Inteligencia Artificial')
    expect(page.locator('#conceptDescription')).to_contain_text('formas de razonar')
    expect(page.locator('.node')).to_have_count(13)
    page.wait_for_timeout(750)
    page.screenshot(path=str(OUT / '02-concepto.png'))
    page.locator('#conceptCenter').click()
    page.locator('#conceptPanelClose').click()
    expect(page.locator('#conceptPanel')).to_be_hidden()

    page.locator('.node').first.focus()
    page.keyboard.press('ArrowDown')
    assert page.evaluate('document.activeElement?.dataset?.id') == page.locator('.node').nth(1).get_attribute('data-id')
    page.keyboard.press('ArrowLeft')
    expect(page.locator('.node')).to_have_count(8)
    page.keyboard.press('F2')
    expect(page.locator('#editDialog')).to_be_visible()
    page.locator('#editDialog .x').click()

    page.keyboard.press('Control+k')
    expect(page.locator('#conceptSearch')).to_be_focused()
    page.locator('#conceptSearch').fill('regresion')
    assert page.locator('#searchResults button').count() > 0
    page.locator('#searchResults button').first.click()
    assert page.locator('#projectName').inner_text()

    page.locator('#filterColorsBtn').click()
    expect(page.locator('#colorFilterPanel')).to_be_visible()
    page.locator('#colorFilterOptions button').first.click()
    expect(page.locator('#filterColorsBtn')).to_have_attribute('data-active', 'true')
    page.locator('#filterColorsBtn').click()
    page.locator('#clearColorFilter').click()
    expect(page.locator('#filterColorsBtn')).to_have_attribute('data-active', 'false')

    page.locator('#newBtn').click()
    expect(page.locator('#newDocDialog')).to_be_visible()
    page.locator('#newDocName').fill('Árbol de prueba aislado')
    page.locator('#newDocKind').select_option('knowledge')
    page.locator('#outlineInput').fill('Aprendizaje\n  Concepto A | Primera explicación | Ejemplo A\n  Concepto B | Segunda explicación | Ejemplo B')
    page.locator('#newDocForm button[type=submit]').click()
    expect(page.locator('#projectName')).to_have_text('Árbol de prueba aislado')
    expect(page.locator('.node')).to_have_count(3)
    page.screenshot(path=str(OUT / '03-arbol-prueba.png'))
    page.locator('.node').nth(1).locator('.node-chain').click()
    page.locator('.node').nth(2).click()
    assert len(page.evaluate('window.BIFURCA_DEBUG.links()')) == 1
    page.locator('.node').nth(1).locator('.node-edit').click()
    expect(page.locator('#editDialog')).to_be_visible()
    page.locator('#editTitle').fill('Concepto A editado')
    page.locator('#editForm button[type=submit]').click()
    expect(page.locator('.node-title').filter(has_text='Concepto A editado')).to_have_count(1)
    page.keyboard.press('Control+z')
    expect(page.locator('.node-title').filter(has_text='Concepto A editado')).to_have_count(0)
    page.keyboard.press('Control+Shift+z')
    expect(page.locator('.node-title').filter(has_text='Concepto A editado')).to_have_count(1)

    page.locator('#moreTools summary').click()
    page.locator('#exportBtn').click()
    with page.expect_download() as export:
        page.locator('#jsonExportBtn').click()
    exported = json.loads(Path(export.value.path()).read_text(encoding='utf-8'))
    assert exported['format'] == 'bifurca-v4'
    assert exported['tree']['children'][0]['title'] == 'Concepto A editado'
    assert len(exported['links']) == 1
    with page.expect_download() as backup:
        page.locator('#sidebarBackupBtn').click()
    assert backup.value.suggested_filename.endswith('.json')

    page.reload(wait_until='domcontentloaded')
    expect(page.locator('#projectName')).to_have_text('Árbol de prueba aislado')
    expect(page.locator('.node-title').filter(has_text='Concepto A editado')).to_have_count(1)
    assert 'bifurca_v3_app' in page.evaluate('Object.keys(localStorage)')
    page.locator('#quickImportBtn').click()
    page.locator('#fileInput').set_input_files({'name': 'test-import.json', 'mimeType': 'application/json', 'buffer': json.dumps(exported).encode()})
    expect(page.locator('#projectName')).to_have_text('Árbol de prueba aislado')
    assert len(page.evaluate('window.BIFURCA_DEBUG.state().docs')) >= 2
    if not page.locator('#treeSidebar').is_visible():
        page.locator('#treesToggle').click()
    page.locator('#courseTreeList .tree-choice').nth(2).click()
    expect(page.locator('#projectName')).to_contain_text('Machine Learning')
    page.locator('.node').nth(1).click()
    assert page.locator('.node').count() > 6
    page.wait_for_timeout(750)
    page.screenshot(path=str(OUT / '04-arbol-grande.png'))
    page.locator('#layoutBtn').click()
    expect(page.locator('body')).to_have_attribute('data-tree-layout', 'horizontal')
    page.locator('#fitBtn').click()
    page.locator('#layoutBtn').click()
    expect(page.locator('body')).to_have_attribute('data-tree-layout', 'compact')
    page.locator('#aiBtn').click()
    expect(page.locator('#aiDialog')).to_be_visible()
    page.locator('#aiDialog [data-close]').click()
    page.locator('#moreTools summary').click()
    page.locator('#legendBtn').click()
    expect(page.locator('#legendDialog')).to_be_visible()
    expect(page.locator('#legendEntries input')).to_have_count(5)
    page.locator('#legendDialog .x').click()
    page.locator('#moreTools summary').click()
    page.locator('#soundBtn').click()
    expect(page.locator('#soundBtn')).to_have_attribute('aria-pressed', 'false')
    assert 'bifurca_audio_v1' in page.evaluate('Object.keys(localStorage)')
    page.locator('#moreTools summary').click()
    page.locator('#soundBtn').click()
    expect(page.locator('#soundBtn')).to_have_attribute('aria-pressed', 'true')
    page.locator('#moreTools summary').click()
    page.locator('#themeBtn').click()
    expect(page.locator('#themeDialog')).to_be_visible()
    page.locator('[data-theme-value="salvia"]').click()
    expect(page.locator('body')).to_have_attribute('data-theme', 'salvia')
    page.locator('#themeDialog .x').click()
    assert not errors, errors
    context.close()

    mobile = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    page = mobile.new_page()
    mobile_errors = []
    page.on('pageerror', lambda error: mobile_errors.append(str(error)))
    page.goto(BASE, wait_until='domcontentloaded')
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
    page.screenshot(path=str(OUT / '05-movil.png'))
    page.locator('#treesToggle').click()
    expect(page.locator('#treeSidebar')).to_be_visible()
    page.locator('#courseTreeList .tree-choice').nth(1).click()
    expect(page.locator('#projectName')).to_contain_text('Inteligencia Artificial')
    page.locator('.node').nth(1).click()
    expect(page.locator('#conceptPanel')).to_be_visible()
    page.wait_for_timeout(900)
    page.screenshot(path=str(OUT / '06-movil-concepto.png'))
    page.locator('#conceptPanelClose').click()
    page.locator('#moreTools summary').click()
    expect(page.locator('#legendBtn')).to_be_visible()
    assert not mobile_errors, mobile_errors
    mobile.close()

    reduced = browser.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
    page = reduced.new_page()
    page.goto(BASE, wait_until='domcontentloaded')
    assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
    page.locator('.node').nth(1).click()
    expect(page.locator('#conceptPanel')).to_be_visible()
    assert page.locator('#conceptPanel').evaluate('(el) => getComputedStyle(el).animationDuration') in ('0.01ms', '1e-05s', '0s')
    reduced.close()
    browser.close()

print('PASS: árbol, panel, teclado, búsqueda, filtro, creación, edición, exportación, respaldo, importación, persistencia, IA, móvil y movimiento reducido')
