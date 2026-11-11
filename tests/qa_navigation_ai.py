"""Isolated Playwright coverage for library and both AI review flows."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

BASE = 'http://127.0.0.1:8012/'
OUT = Path(__file__).resolve().parent / 'captures-navigation-ai'
OUT.mkdir(exist_ok=True)

def seed(page):
    page.evaluate("""() => {
      const key='bifurca_v3_app', s=JSON.parse(localStorage.getItem(key));
      const n=(id,title,children=[],description='')=>({id,title,description,example:'',notes:'',status:'neutral',collapsed:false,expanded:false,children});
      s.docs.push({id:'qa-map',name:'Atlas de anatomía',kind:'knowledge',root:n('r','Anatomía',[
        n('a','Cabeza',[n('x','Encéfalo',[],'Sistema nervioso central')]),
        n('b','Cuerpo',[n('y','Encéfalo',[],'Un nombre repetido a propósito')])
      ],'Mapa corporal de prueba'),links:[],auxNodes:[],legend:{neutral:'Sin clasificar',positive:'Clave clínica',warning:'Repasar',negative:'Error frecuente',info:'Referencia visual'},updatedAt:Date.now()});
      s.activeId='qa-map';localStorage.setItem(key,JSON.stringify(s));
    }""")
    page.reload(wait_until='domcontentloaded')

def tree(page):
    return page.evaluate('window.BIFURCA_DEBUG.tree()')

def child(parent, title):
    return next(x for x in parent['children'] if x['title']==title)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    ctx=browser.new_context(viewport={'width':1440,'height':900},accept_downloads=True)
    page=ctx.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    assert page.goto(BASE,wait_until='domcontentloaded').status==200
    seed(page)
    expect(page.locator('#projectBtn')).to_have_count(1)
    assert page.locator('#projectBtn').evaluate('(x)=>x.tagName')=='DIV'
    expect(page.locator('#projectName')).to_have_text('Atlas de anatomía')
    page.locator('#libraryOpenBtn').click()
    expect(page.locator('#libraryDialog')).to_be_visible()
    assert page.locator('#libraryDialog').bounding_box()['width']>=1400
    page.screenshot(path=str(OUT/'01-biblioteca-escritorio.png'))
    with page.expect_download() as transfer:
        page.locator('.library-card').filter(has_text='Atlas de anatomía').get_by_role('button',name='Exportar').click()
    archive=json.loads(Path(transfer.value.path()).read_text(encoding='utf-8'))
    assert archive['format']=='bifurca-v4' and archive['tree']['id']=='r' and archive['legend']['positive']=='Clave clínica'
    page.locator('#librarySearch').fill('Sistema nervioso central')
    expect(page.locator('.library-card')).to_have_count(1)
    page.locator('#librarySearch').fill('')
    page.locator('[data-library-filter="personal"]').click()
    assert page.locator('.library-card').count()>=1
    page.locator('#librarySort').select_option('name')
    page.locator('[data-library-filter="all"]').click()
    preset=page.locator('.library-card').filter(has_text='MongoDB · Bases de datos documentales')
    preset.get_by_role('button',name='Abrir árbol').click()
    expect(page.locator('#projectName')).to_have_text('MongoDB · Bases de datos documentales')
    page.locator('#libraryOpenBtn').click()
    page.locator('.library-card').filter(has_text='Atlas de anatomía').get_by_role('button',name='Abrir árbol').click()
    expect(page.locator('#libraryDialog')).to_be_hidden()
    expect(page.locator('#projectName')).to_have_text('Atlas de anatomía')
    current_view=page.evaluate('window.BIFURCA_DEBUG.view()')
    page.locator('#libraryOpenBtn').click();page.locator('.library-return').click()
    assert page.evaluate('window.BIFURCA_DEBUG.view()')==current_view
    page.locator('#libraryOpenBtn').focus();page.keyboard.press('Enter');expect(page.locator('#libraryDialog')).to_be_visible()
    page.keyboard.press('Escape');expect(page.locator('#libraryDialog')).to_be_hidden()
    page.locator('#moreTools summary').click()
    page.locator('#completeTreeBtn').click()
    expect(page.locator('#completeDialog')).to_be_visible()
    prompt=page.locator('#completePrompt').input_value()
    assert all(x in prompt for x in ['RUTA_PADRE','ID_PADRE','[ID x]','[ID y]'])
    page.locator('#completePrompt').fill(prompt+'\nInstrucción adicional propia.')
    response='''CONCEPTO: Cerebelo
PADRE: Encéfalo
RUTA_PADRE: Anatomía → Cuerpo → Encéfalo
ID_PADRE: x
EXPLICACION: Coordina el movimiento.
EJEMPLO: Mantener el equilibrio.
NOTAS: Situado detrás del tronco.
---
CONCEPTO: Tronco encefálico
PADRE: Encéfalo
RUTA_PADRE: Anatomía → Cuerpo → Encéfalo
ID_PADRE: id-inexistente
EXPLICACION: Conecta estructuras.
EJEMPLO: Control respiratorio.
NOTAS: Función vital.
---
CONCEPTO: Circuitos cerebelosos
PADRE: Cerebelo
RUTA_PADRE: Anatomía → Cabeza → Encéfalo → Cerebelo
ID_PADRE:
EXPLICACION: Redes neuronales locales.
EJEMPLO: Aprendizaje motor.
NOTAS: Varios núcleos.
---
CONCEPTO: Concepto ambiguo
PADRE: Encéfalo
RUTA_PADRE:
ID_PADRE:
EXPLICACION: Requiere elección manual.
EJEMPLO:
NOTAS:
---'''
    page.locator('#completeResponse').fill(response)
    original=tree(page)
    page.locator('#completeReviewBtn').click()
    expect(page.locator('#aiPreviewPanel')).to_be_visible()
    assert tree(page)==original
    page.locator('#aiPreviewExpand').click()
    expect(page.locator('#aiReviewDialog')).to_be_visible()
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'02-revision-expandida.png'))
    cards=page.locator('.review-card')
    expect(cards).to_have_count(4)
    assert 'Elige un nodo padre' in cards.nth(3).inner_text()
    cards.nth(2).locator('select[aria-label^="Nodo padre"]').select_option('proposal:p0')
    cards.nth(3).locator('select[aria-label^="Nodo padre"]').select_option('y')
    cards.nth(0).locator('select[aria-label^="Color"]').select_option('positive')
    cards.nth(1).locator('select[aria-label^="Color"]').select_option('warning')
    cards.nth(3).get_by_role('button',name='Rechazar Concepto ambiguo').click()
    page.locator('#aiReviewBack').click()
    expect(page.locator('#aiReviewDialog')).to_be_hidden()
    page.locator('#aiPreviewExpand').click()
    assert page.locator('.review-card').nth(0).locator('select[aria-label^="Color"]').input_value()=='positive'
    page.locator('#aiReviewSource').click()
    expect(page.locator('#completeDialog')).to_be_visible()
    assert page.locator('#completeResponse').input_value()==response
    assert 'Instrucción adicional propia.' in page.locator('#completePrompt').input_value()
    page.locator('#completeResumeBtn').click()
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'03-ubicaciones-corregidas.png'))
    page.locator('#aiReviewContinue').click()
    expect(page.locator('#aiConfirmDialog')).to_be_visible()
    assert tree(page)==original
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'04-confirmacion.png'))
    page.locator('#aiConfirmApply').click()
    root=tree(page);head=child(root,'Cabeza');body=child(root,'Cuerpo')
    cerebellum=child(child(head,'Encéfalo'),'Cerebelo')
    assert cerebellum['status']=='positive' and cerebellum['description']=='Coordina el movimiento.'
    assert child(cerebellum,'Circuitos cerebelosos')['example']=='Aprendizaje motor.'
    assert child(child(body,'Encéfalo'),'Tronco encefálico')['status']=='warning'
    assert 'Concepto ambiguo' not in str(root)
    page.locator('#undoBtn').click();assert tree(page)==original
    page.locator('#redoBtn').click();assert 'Cerebelo' in str(tree(page))
    page.reload(wait_until='domcontentloaded');assert 'Cerebelo' in str(tree(page))
    page.locator('#moreTools summary').click()
    page.locator('#completeTreeBtn').click()
    page.locator('#completeResponse').fill('''CONCEPTO: Cabeza
PADRE: Anatomía
RUTA_PADRE: Anatomía
ID_PADRE: r
EXPLICACION: Duplicado.
---
CONCEPTO: Ciclo A
PADRE:
RUTA_PADRE:
ID_PADRE:
EXPLICACION: Primero.
---
CONCEPTO: Ciclo B
PADRE:
RUTA_PADRE:
ID_PADRE:
EXPLICACION: Segundo.
---''')
    before_invalid=tree(page)
    page.locator('#completeReviewBtn').click();page.locator('#aiPreviewExpand').click()
    expect(page.locator('#aiReviewContinue')).to_be_disabled()
    assert 'Ya existe un concepto' in page.locator('.review-card').nth(0).inner_text()
    cards=page.locator('.review-card')
    cards.nth(1).locator('select[aria-label^="Nodo padre"]').select_option('proposal:p2')
    cards.nth(2).locator('select[aria-label^="Nodo padre"]').select_option('proposal:p1')
    assert any('circular' in x.lower() for x in page.locator('.review-error').all_inner_texts())
    cards.nth(1).get_by_role('button',name='Rechazar Ciclo A').click()
    assert 'padre está rechazada' in page.locator('.review-card').nth(2).inner_text()
    assert tree(page)==before_invalid
    page.locator('#aiReviewDiscard').click()
    assert tree(page)==before_invalid
    page.locator('#aiBtn').click()
    expect(page.locator('#aiDialog')).to_be_visible()
    page.locator('#aiResponse').fill('CONCEPTO: Nueva prueba\nEXPLICACION: Campo\nEJEMPLO: Caso\nNOTAS: Nota\n---')
    page.locator('#addSuggestions').click()
    page.locator('#aiPreviewExpand').click()
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'05-ideas-ia.png'))
    page.locator('#aiReviewSource').click()
    assert 'Nueva prueba' in page.locator('#aiResponse').input_value()
    page.locator('#aiResumeBtn').click()
    page.locator('#aiReviewDiscard').click()
    assert 'Nueva prueba' not in str(tree(page))
    assert not errors,errors
    ctx.close()
    mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    mp=mobile.new_page();mp.goto(BASE,wait_until='domcontentloaded');seed(mp)
    mp.locator('#libraryOpenBtn').click();expect(mp.locator('#libraryDialog')).to_be_visible()
    assert mp.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
    mp.wait_for_timeout(350)
    mp.screenshot(path=str(OUT/'06-biblioteca-movil.png'))
    mp.locator('.library-return').click()
    mp.screenshot(path=str(OUT/'07-arbol-movil.png'))
    mp.locator('#aiBtn').click()
    mp.locator('#aiResponse').fill('CONCEPTO: Prueba móvil\nEXPLICACION: Texto legible.\nEJEMPLO: Un ejemplo.\nNOTAS: Una nota.\n---')
    mp.locator('#addSuggestions').click();mp.locator('#aiPreviewExpand').click()
    expect(mp.locator('#aiReviewDialog')).to_be_visible()
    assert mp.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
    mp.wait_for_timeout(350);mp.screenshot(path=str(OUT/'08-revision-movil.png'))
    mobile.close();browser.close()
print('PASS: biblioteca, título, IA, padres por ID/ruta, dependencias, colores, confirmación, deshacer, persistencia y móvil')
