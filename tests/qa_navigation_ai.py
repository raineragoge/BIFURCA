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
---
CONCEPTO: Cabeza
PADRE: Anatomía
RUTA_PADRE: Anatomía
ID_PADRE: r
EXPLICACION: Concepto duplicado para corregir.
EJEMPLO:
NOTAS:
---
CONCEPTO: Detalle descartado
PADRE: Encéfalo
RUTA_PADRE: Anatomía → Cuerpo → Encéfalo
ID_PADRE: y
EXPLICACION: No se incorporará.
EJEMPLO:
NOTAS:
---'''
    page.locator('#completeResponse').fill(response)
    original=tree(page)
    page.locator('#completeReviewBtn').click()
    expect(page.locator('#aiReviewDialog')).to_be_visible()
    expect(page.locator('.review-rail-item')).to_have_count(6)
    expect(page.locator('#aiGhostLayer .ai-ghost-card')).to_have_count(0)
    assert tree(page)==original
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'02-revision-expandida.png'))
    page.locator('#reviewDescription').fill('Coordina con precisión el movimiento y el equilibrio.')
    page.locator('#reviewExample').fill('Caminar por una línea manteniendo el equilibrio.')
    page.locator('#reviewNotes').fill('Dos hemisferios y vermis.')
    page.locator('#reviewColor').select_option('positive')
    page.locator('#reviewNext').click()
    page.locator('#reviewParentSearch').fill('Cabeza → Encéfalo')
    page.locator('#reviewParent').select_option('x')
    page.locator('#reviewColor').select_option('warning')
    page.locator('.review-rail-item').nth(2).click()
    page.locator('#reviewParent').select_option('proposal:p0')
    page.locator('.review-rail-item').nth(3).click()
    assert 'Elige un nodo padre' in page.locator('#reviewError').inner_text()
    page.locator('#reviewToggle').click()
    page.locator('.review-rail-item').nth(4).click()
    assert 'Ya existe un concepto' in page.locator('#reviewError').inner_text()
    page.locator('#reviewTitle').fill('Huesos craneales')
    page.locator('#reviewParent').select_option('a')
    expect(page.locator('#reviewError')).to_be_hidden()
    page.locator('.review-rail-item').nth(5).click();page.locator('#reviewToggle').click()
    expect(page.locator('#aiReviewCount')).to_have_text('4 seleccionadas de 6')
    page.locator('.review-rail-item').first.click()
    assert page.locator('#reviewDescription').input_value()=='Coordina con precisión el movimiento y el equilibrio.'
    assert page.locator('#reviewColor').input_value()=='positive'
    page.locator('#aiReviewClose').click()
    expect(page.locator('#aiReviewDialog')).to_be_hidden()
    assert tree(page)==original and page.locator('#aiResumeFloating').is_visible()
    page.locator('#aiResumeFloating').click()
    assert page.locator('#reviewDescription').input_value()=='Coordina con precisión el movimiento y el equilibrio.'
    page.locator('#aiReviewTreePreview').click()
    expect(page.locator('#aiReviewDialog')).to_be_hidden()
    expect(page.locator('#aiGhostLayer .ai-ghost-card')).to_have_count(1)
    assert page.locator('#aiTreePreviewBar').is_visible()
    page.wait_for_timeout(550)
    page.screenshot(path=str(OUT/'03-ubicacion-en-arbol.png'))
    page.locator('#aiTreePreviewReturn').click()
    expect(page.locator('#aiReviewDialog')).to_be_visible()
    page.locator('.review-rail-item').nth(2).click();page.locator('#aiReviewTreePreview').click()
    ghosts=page.locator('#aiGhostLayer .ai-ghost-card')
    expect(ghosts).to_have_count(2)
    boxes=[ghosts.nth(i).bounding_box() for i in range(2)]
    assert boxes[0]['x']+boxes[0]['width']<=boxes[1]['x']
    page.locator('#aiTreePreviewReturn').click()
    page.locator('#aiReviewSource').click()
    expect(page.locator('#completeDialog')).to_be_visible()
    assert page.locator('#completeResponse').input_value()==response
    assert 'Instrucción adicional propia.' in page.locator('#completePrompt').input_value()
    page.locator('#completeResumeBtn').click()
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'03-ubicaciones-corregidas.png'))
    page.locator('#aiReviewContinue').click()
    expect(page.locator('#aiConfirmDialog')).to_be_visible()
    expect(page.locator('.confirm-row')).to_have_count(4)
    assert tree(page)==original
    page.locator('#aiConfirmBack').click()
    page.locator('.review-rail-item').first.click();page.locator('#reviewNotes').fill('Dos hemisferios, vermis y núcleos profundos.')
    page.locator('#aiReviewContinue').click()
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'04-confirmacion.png'))
    page.locator('#aiConfirmApply').click()
    root=tree(page);head=child(root,'Cabeza');body=child(root,'Cuerpo')
    cerebellum=child(child(head,'Encéfalo'),'Cerebelo')
    assert cerebellum['status']=='positive' and cerebellum['description']=='Coordina con precisión el movimiento y el equilibrio.'
    assert cerebellum['example']=='Caminar por una línea manteniendo el equilibrio.' and cerebellum['notes']=='Dos hemisferios, vermis y núcleos profundos.'
    assert child(cerebellum,'Circuitos cerebelosos')['example']=='Aprendizaje motor.'
    assert child(child(head,'Encéfalo'),'Tronco encefálico')['status']=='warning'
    assert child(head,'Huesos craneales')['description']=='Concepto duplicado para corregir.'
    assert 'Concepto ambiguo' not in str(root) and 'Detalle descartado' not in str(root)
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
    page.locator('#completeReviewBtn').click()
    expect(page.locator('#aiReviewContinue')).to_be_disabled()
    assert 'Ya existe un concepto' in page.locator('#reviewError').inner_text()
    page.locator('.review-rail-item').nth(1).click()
    page.locator('#reviewParent').select_option('proposal:p2')
    page.locator('.review-rail-item').nth(2).click()
    page.locator('#reviewParent').select_option('proposal:p1')
    assert 'circular' in page.locator('#reviewError').inner_text().lower()
    page.locator('.review-rail-item').nth(1).click();page.locator('#reviewToggle').click()
    page.locator('.review-rail-item').nth(2).click()
    assert 'padre está rechazada' in page.locator('#reviewError').inner_text()
    assert tree(page)==before_invalid
    page.locator('#aiReviewDiscard').click()
    assert tree(page)==before_invalid
    page.locator('#aiBtn').click()
    expect(page.locator('#aiDialog')).to_be_visible()
    page.locator('#aiResponse').fill('CONCEPTO: Nueva prueba\nEXPLICACION: Campo\nEJEMPLO: Caso\nNOTAS: Nota\n---')
    page.locator('#addSuggestions').click()
    expect(page.locator('#aiReviewDialog')).to_be_visible()
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT/'05-ideas-ia.png'))
    page.locator('#aiReviewSource').click()
    assert 'Nueva prueba' in page.locator('#aiResponse').input_value()
    page.locator('#aiResumeBtn').click()
    page.locator('#aiReviewDiscard').click()
    assert 'Nueva prueba' not in str(tree(page))
    page.locator('#aiBtn').click()
    page.locator('#aiProposalFileInput').set_input_files({'name':'propuestas.json','mimeType':'application/json','buffer':json.dumps({'propuestas':[{'concepto':'Importado externo','explicacion':'Conserva el parser anterior.'}]}).encode('utf-8')})
    expect(page.locator('#aiReviewDialog')).to_be_visible()
    expect(page.locator('#reviewTitle')).to_have_value('Importado externo')
    page.locator('#aiReviewDiscard').click()
    page.locator('#aiBtn').click()
    many='\n'.join(f'CONCEPTO: Idea {i:02d}\nEXPLICACION: Una explicación editable.\n---' for i in range(1,31))
    page.locator('#aiResponse').fill(many);page.locator('#addSuggestions').click()
    expect(page.locator('.review-rail-item')).to_have_count(30)
    page.locator('.review-rail-item').last.click()
    expect(page.locator('#reviewPosition')).to_have_text('PROPUESTA 30 / 30')
    page.locator('#reviewExample').fill('Caso treinta.')
    page.locator('.review-rail-item').first.click();page.locator('.review-rail-item').last.click()
    assert page.locator('#reviewExample').input_value()=='Caso treinta.'
    assert page.locator('#aiReviewList').evaluate('(x)=>x.scrollHeight>x.clientHeight')
    assert page.locator('#aiReviewDialog').bounding_box()['width']<=1440
    page.wait_for_timeout(350);page.screenshot(path=str(OUT/'10-treinta-propuestas.png'))
    page.locator('#aiReviewDiscard').click()
    assert not errors,errors
    ctx.close()
    mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    mp=mobile.new_page();mobile_errors=[];mp.on('pageerror',lambda e:mobile_errors.append(str(e)));mp.goto(BASE,wait_until='domcontentloaded');seed(mp)
    mp.locator('#libraryOpenBtn').click();expect(mp.locator('#libraryDialog')).to_be_visible()
    assert mp.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
    mp.wait_for_timeout(350)
    mp.screenshot(path=str(OUT/'06-biblioteca-movil.png'))
    mp.locator('.library-return').click()
    mp.screenshot(path=str(OUT/'07-arbol-movil.png'))
    mp.locator('#aiBtn').click()
    mp.locator('#aiResponse').fill('CONCEPTO: Prueba móvil\nEXPLICACION: Texto legible.\nEJEMPLO: Un ejemplo.\nNOTAS: Una nota.\n---')
    mp.locator('#addSuggestions').click()
    expect(mp.locator('#aiReviewDialog')).to_be_visible()
    assert mp.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
    mp.wait_for_timeout(350);mp.screenshot(path=str(OUT/'08-revision-movil.png'))
    mp.locator('#aiReviewDiscard').click()
    mp.locator('#moreTools summary').click();mp.locator('#completeTreeBtn').click()
    mp.locator('#completeResponse').fill(response);mobile_original=tree(mp)
    mp.locator('#completeReviewBtn').click();expect(mp.locator('.review-rail-item')).to_have_count(6)
    mp.locator('#reviewDescription').fill('Explicación revisada desde móvil.')
    mp.locator('#reviewColor').select_option('positive')
    mp.locator('.review-rail-item').nth(2).click();mp.locator('#reviewParent').select_option('proposal:p0')
    mp.locator('.review-rail-item').nth(3).click();mp.locator('#reviewToggle').click()
    mp.locator('.review-rail-item').nth(4).click();mp.locator('#reviewTitle').fill('Huesos móviles');mp.locator('#reviewParent').select_option('a')
    mp.locator('.review-rail-item').nth(5).click();mp.locator('#reviewToggle').click()
    expect(mp.locator('#aiReviewCount')).to_have_text('4 seleccionadas de 6')
    assert mp.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
    mp.wait_for_timeout(350);mp.screenshot(path=str(OUT/'09-seis-propuestas-movil.png'))
    mp.locator('#aiReviewContinue').click();expect(mp.locator('.confirm-row')).to_have_count(4)
    assert tree(mp)==mobile_original
    mp.locator('#aiConfirmApply').click();assert child(child(child(tree(mp),'Cabeza'),'Encéfalo'),'Cerebelo')['status']=='positive'
    assert child(tree(mp),'Cabeza')['children'][-1]['title']=='Huesos móviles'
    mp.locator('#undoBtn').click();assert tree(mp)==mobile_original
    assert not mobile_errors,mobile_errors
    mobile.close();browser.close()
print('PASS: biblioteca, título, IA, padres por ID/ruta, dependencias, colores, confirmación, deshacer, persistencia y móvil')
