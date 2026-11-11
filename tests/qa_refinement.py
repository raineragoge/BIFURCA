"""Focused UX regression checks in temporary Playwright browser contexts."""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = 'http://127.0.0.1:8012/'
OUT = Path(__file__).resolve().parent / 'captures-refinement'
OUT.mkdir(exist_ok=True)
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lQAAAABJRU5ErkJggg==')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width':1440,'height':900}, accept_downloads=True)
    page = context.new_page()
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    assert page.goto(BASE,wait_until='domcontentloaded').status==200
    assert 'bifurca_v3_app' in page.evaluate('Object.keys(localStorage)')
    assert page.locator('#treeSidebar').bounding_box()['width'] <= 260
    expect(page.locator('#courseTreeList .tree-choice')).to_have_count(8)
    page.screenshot(path=str(OUT/'01-biblioteca.png'))
    initial_root_id=page.evaluate('window.BIFURCA_DEBUG.tree().id')

    page.locator('#guideToggle').focus()
    page.keyboard.press('Space')
    expect(page.locator('#guideToggle')).to_have_attribute('aria-expanded','false')
    expect(page.locator('#guideContent')).to_be_hidden()
    assert page.evaluate("localStorage.getItem('bifurca_guide_collapsed_v1')")=='1'
    page.screenshot(path=str(OUT/'02-ayuda-minima.png'))
    page.locator('#courseTreeList .tree-choice').nth(1).click()
    expect(page.locator('#guideToggle')).to_have_attribute('aria-expanded','false')
    page.reload(wait_until='domcontentloaded')
    expect(page.locator('#guideToggle')).to_have_attribute('aria-expanded','false')
    page.locator('#guideToggle').click()
    expect(page.locator('#guideContent')).to_be_visible()

    page.locator('#closeSidebarBtn').click()
    expect(page.locator('#treesToggle')).to_have_attribute('aria-expanded','false')
    assert page.locator('#stage').bounding_box()['width'] > 1300
    page.locator('#treesToggle').click()
    expect(page.locator('#treesToggle')).to_have_attribute('aria-expanded','true')
    page.locator('#conceptSearch').fill('bayes')
    assert page.locator('#searchResults button').count()>0
    page.locator('#searchResults button').first.click()
    assert page.locator('#projectName').inner_text()
    page.locator('#conceptSearch').fill('')

    page.locator('#courseTreeList .tree-choice').first.click()
    assert page.evaluate('window.BIFURCA_DEBUG.tree().id')==initial_root_id
    page.locator('#fitBtn').click()
    page.wait_for_timeout(550)
    page.locator('.node').nth(1).locator('.node-edit').click()
    expect(page.locator('#editDialog')).to_be_visible()
    expect(page.locator('#knowledgeFields')).to_be_visible()
    expect(page.locator('#editForm button[type=submit]')).to_be_in_viewport()
    expect(page.locator('#notesDisclosure')).not_to_have_attribute('open','')
    page.screenshot(path=str(OUT/'03-editor.png'))
    page.locator('#editDescription').fill('Explicación de prueba sin datos personales.')
    page.locator('#editExample').fill('Ejemplo local de prueba.')
    page.locator('#notesDisclosure summary').click()
    page.locator('#editNote').fill('Nota temporal que debe persistir.')
    page.locator('#notesDisclosure summary').click()
    expect(page.locator('#notesDisclosure')).not_to_have_attribute('open','')
    assert page.locator('#editNote').input_value()=='Nota temporal que debe persistir.'
    page.locator('#mediaDisclosure summary').click()
    page.locator('#editImageFile').set_input_files({'name':'tiny.png','mimeType':'image/png','buffer':PNG})
    page.wait_for_function("!document.querySelector('#editImagePreview').hidden")
    page.screenshot(path=str(OUT/'04-editor-imagen.png'))
    for key in ('neutral','positive','warning','negative','info'):
        page.locator(f'#statusChoices [data-status="{key}"]').click()
        expect(page.locator(f'#statusChoices [data-status="{key}"]')).to_have_attribute('aria-pressed','true')
    page.locator('#editForm button[type=submit]').click()
    edited=page.evaluate('window.BIFURCA_DEBUG.tree().children[0]')
    assert edited['status']=='info'
    assert edited['description']=='Explicación de prueba sin datos personales.'
    assert edited['example']=='Ejemplo local de prueba.'
    assert edited['notes']=='Nota temporal que debe persistir.'
    assert edited['image'].startswith('data:image/')
    page.reload(wait_until='domcontentloaded')
    assert page.evaluate('window.BIFURCA_DEBUG.tree().children[0].status')=='info'
    page.locator('.node').nth(1).locator('.node-edit').click()
    expect(page.locator('#notesDisclosure')).to_have_attribute('open','')
    expect(page.locator('#mediaDisclosure')).to_have_attribute('open','')
    page.locator('#editTitle').fill('CAMBIO DESCARTADO')
    page.locator('.editor-footer [data-close="editDialog"]').click()
    assert page.evaluate('window.BIFURCA_DEBUG.tree().children[0].title')!='CAMBIO DESCARTADO'
    page.locator('.node').nth(1).locator('.node-edit').click()
    page.locator('#clearImageBtn').click()
    expect(page.locator('#editImagePreview')).to_be_hidden()
    page.locator('#editForm button[type=submit]').click()
    assert page.evaluate('window.BIFURCA_DEBUG.tree().children[0].image')==''
    page.locator('.node').nth(1).locator('.node-edit').click()
    page.locator('#mediaDisclosure summary').click()
    page.locator('#editImageUrl').fill('https://example.invalid/editorial.png')
    expect(page.locator('#editImagePreview')).to_be_visible()
    page.locator('#editForm button[type=submit]').click()
    assert page.evaluate('window.BIFURCA_DEBUG.tree().children[0].image')=='https://example.invalid/editorial.png'
    page.locator('#moreTools summary').click()
    page.locator('#legendBtn').click()
    page.locator('#legendEntries input').nth(1).fill('Esencial')
    page.locator('#saveLegendBtn').click()
    page.locator('.node').nth(1).locator('.node-edit').click()
    expect(page.locator('#statusChoices [data-status="positive"]')).to_contain_text('Esencial')
    page.locator('.editor-footer [data-close="editDialog"]').click()

    page.locator('#newBtn').click()
    page.locator('#newDocName').fill('Árbol de eliminación aislado')
    page.locator('#newDocKind').select_option('knowledge')
    page.locator('#outlineInput').fill('Raíz\n  Rama de prueba')
    page.locator('#newDocForm button[type=submit]').click()
    expect(page.locator('.node')).to_have_count(2)
    page.locator('.node').nth(1).locator('.node-edit').click()
    page.locator('#editAdvanced summary').click()
    page.once('dialog',lambda dialog:dialog.dismiss())
    page.locator('#deleteNode').click()
    expect(page.locator('#editDialog')).to_be_visible()
    assert len(page.evaluate('window.BIFURCA_DEBUG.tree().children'))==1
    page.once('dialog',lambda dialog:dialog.accept())
    page.locator('#deleteNode').click()
    page.wait_for_function('window.BIFURCA_DEBUG.tree().children.length===0')
    assert not errors,errors
    context.close()

    for width in (390,320):
        mobile=browser.new_context(viewport={'width':width,'height':844},is_mobile=True,has_touch=True)
        page=mobile.new_page()
        mobile_errors=[]
        page.on('pageerror',lambda error:mobile_errors.append(str(error)))
        page.goto(BASE,wait_until='domcontentloaded')
        expect(page.locator('#guideToggle')).to_have_attribute('aria-expanded','false')
        page.locator('#guideToggle').click()
        expect(page.locator('#guideContent')).to_be_visible()
        page.locator('#guideToggle').click()
        page.locator('#treesToggle').click()
        expect(page.locator('#treesToggle')).to_have_attribute('aria-expanded','true')
        page.locator('#courseTreeList .tree-choice').nth(1).click()
        expect(page.locator('#projectName')).to_contain_text('Inteligencia Artificial')
        page.locator('.node').nth(1).locator('.node-edit').click()
        expect(page.locator('#editDialog')).to_be_visible()
        page.wait_for_timeout(300)
        assert round(page.locator('#editDialog').bounding_box()['width'])==width
        expect(page.locator('#editForm button[type=submit]')).to_be_in_viewport()
        page.locator('#notesDisclosure summary').focus()
        page.keyboard.press('Enter')
        expect(page.locator('#notesDisclosure')).to_have_attribute('open','')
        page.locator('#editNote').fill('Borrador móvil')
        page.locator('#notesDisclosure summary').click()
        assert page.locator('#editNote').input_value()=='Borrador móvil'
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
        page.screenshot(path=str(OUT/f'05-editor-movil-{width}.png'))
        assert not mobile_errors,mobile_errors
        mobile.close()

    many=browser.new_context(viewport={'width':1280,'height':760})
    page=many.new_page()
    page.goto(BASE,wait_until='domcontentloaded')
    page.evaluate("""() => {
      const state=window.BIFURCA_DEBUG.state(),sample=state.docs.find(d=>!d.id.startsWith('preset-'));
      for(let i=1;i<=30;i++)state.docs.push({...structuredClone(sample),id:'test-many-'+i,name:'Mapa de prueba '+String(i).padStart(2,'0')});
      localStorage.setItem('bifurca_v3_app',JSON.stringify(state));
    }""")
    page.reload(wait_until='domcontentloaded')
    expect(page.locator('#personalTreeList .tree-choice')).to_have_count(31)
    assert page.locator('#sidebarBrowse').evaluate('(e)=>e.scrollHeight>e.clientHeight')
    page.locator('#personalTreeList .tree-choice').last.scroll_into_view_if_needed()
    page.screenshot(path=str(OUT/'06-biblioteca-larga.png'))
    page.locator('#personalTreeList .tree-choice').last.click()
    expect(page.locator('#projectName')).to_have_text('Mapa de prueba 30')
    many.close()
    browser.close()

print('PASS: biblioteca amplia, búsqueda, ayuda persistente, editor, cinco colores, imagen, cancelar, eliminación protegida y móvil')
