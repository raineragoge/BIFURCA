"""BIFURCA · QA aislado de lectura ampliada y eliminación de nodos.
Ejecutar con servidor local en el puerto 8012:
    python tests/qa_node_actions.py
No usa datos del navegador habitual ni modifica la web pública.
"""
import os
from playwright.sync_api import sync_playwright, expect

BASE = os.getenv("BIFURCA_TEST_URL", "http://127.0.0.1:8012/")
NAME = "QA – Árbol temporal de acciones"

def node_id(page, title):
    return page.evaluate("""title => {
      let found = null;
      function walk(n) { if(n.title === title) { found = n.id; return; }
        for(const child of n.children) { if(!found) walk(child); }
      }
      walk(window.BIFURCA_DEBUG.tree());
      return found;
    }""", title)

def get_tree(page):
    return page.evaluate("window.BIFURCA_DEBUG.tree()")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    missing = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("response", lambda res: missing.append(res.url) if res.status >= 400 else None)
    page.goto(BASE, wait_until="domcontentloaded")
    page.locator("#newBtn").click()
    page.locator("#newDocName").fill(NAME)
    page.locator("#newDocKind").select_option("knowledge")
    page.locator("#outlineInput").fill(
        "Raíz de prueba\n"
        "  Concepto A | Explicación amplia para leer en una ventana independiente. | Ejemplo útil\n"
        "    Concepto B | Definición B | Ejemplo B\n"
        "    Concepto C | Definición C | Ejemplo C\n"
        "  Concepto D | Definición D | Ejemplo D"
    )
    page.locator('#newDocForm button[type="submit"]').click()
    root_id, a_id = node_id(page, "Raíz de prueba"), node_id(page, "Concepto A")
    b_id, c_id = node_id(page, "Concepto B"), node_id(page, "Concepto C")
    assert all((root_id, a_id, b_id, c_id))

    # La raíz se protege; la lectura funciona sin alterar las ramas.
    expect(page.locator(f'.node[data-id="{root_id}"] .node-delete')).to_be_hidden()
    page.locator(f'.node[data-id="{root_id}"] .node-read').click()
    expect(page.locator("#nodeReadDialog")).to_be_visible()
    expect(page.locator("#nodeReadTitle")).to_have_text("Raíz de prueba")
    page.get_by_role("button", name="Volver al mapa").click()

    # Si la rama está plegada, la desplegamos antes de leer su contenido.
    if page.locator(f'.node[data-id="{a_id}"]').count() == 0:
        page.locator(f'.node[data-id="{root_id}"] .node-fold').click()
    page.locator(f'.node[data-id="{a_id}"] .node-read').click()
    expect(page.locator("#nodeReadTitle")).to_have_text("Concepto A")
    expect(page.locator("#nodeReadDescription .node-read-value")).to_contain_text("Explicación amplia")
    expect(page.locator("#nodeReadExample .node-read-value")).to_have_text("Ejemplo útil")
    expect(page.locator("#nodeReadChildren li")).to_have_count(2)
    page.locator("#nodeReadEdit").click()
    expect(page.locator("#editDialog")).to_be_visible()
    expect(page.locator("#editTitle")).to_have_value("Concepto A")
    page.locator('#editDialog [data-close="editDialog"]').first.click()

    # Cancelar la eliminación no debe modificar el árbol.
    page.locator(f'.node[data-id="{a_id}"] .node-delete').click()
    expect(page.locator("#deleteNodeDialog")).to_be_visible()
    expect(page.locator("#deleteNodeModes")).to_be_visible()
    page.locator('#deleteNodeDialog [data-close="deleteNodeDialog"]').click()
    assert node_id(page, "Concepto A") == a_id

    # Eliminar únicamente el padre y promover a sus dos hijos.
    page.locator(f'.node[data-id="{a_id}"] .node-delete').click()
    page.locator('#deleteNodeModes [value="node"]').check()
    page.locator("#confirmNodeDeletion").click()
    tree = get_tree(page)
    assert [n["title"] for n in tree["children"]] == ["Concepto B", "Concepto C", "Concepto D"]
    assert node_id(page, "Concepto A") is None
    assert node_id(page, "Concepto B") == b_id
    assert node_id(page, "Concepto C") == c_id

    # Deshacer y rehacer utilizan el historial original.
    page.locator("#undoBtn").click()
    assert node_id(page, "Concepto A") == a_id
    assert [x["title"] for x in get_tree(page)["children"][0]["children"]] == ["Concepto B", "Concepto C"]
    page.locator("#redoBtn").click()
    assert node_id(page, "Concepto A") is None
    page.locator("#undoBtn").click()

    # Eliminar toda la rama elimina también descendientes y se puede deshacer.
    page.locator(f'.node[data-id="{a_id}"] .node-delete').click()
    page.locator('#deleteNodeModes [value="branch"]').check()
    page.locator("#confirmNodeDeletion").click()
    assert node_id(page, "Concepto A") is None
    assert node_id(page, "Concepto B") is None
    assert node_id(page, "Concepto C") is None
    assert [n["title"] for n in get_tree(page)["children"]] == ["Concepto D"]
    page.locator("#undoBtn").click()
    assert node_id(page, "Concepto B") == b_id

    # Persistencia en el perfil temporal.
    page.reload(wait_until="domcontentloaded")
    assert node_id(page, "Concepto A") == a_id
    assert "bifurca_v3_app" in page.evaluate("Object.keys(localStorage)")

    # Móvil: botones disponibles sin hover y ventana dentro del viewport.
    mobile = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    mobile.on("pageerror", lambda error: errors.append(str(error)))
    mobile.goto(BASE, wait_until="domcontentloaded")
    first = mobile.locator('.node').first
    first.locator('.node-read').tap()
    expect(mobile.locator("#nodeReadDialog")).to_be_visible()
    assert mobile.locator("#nodeReadDialog").evaluate("el=>el.getBoundingClientRect().width <= innerWidth")
    mobile.locator('#nodeReadDialog [data-close="nodeReadDialog"]').first.tap()

    assert not errors, errors
    assert not missing, missing
    browser.close()
print("PASS: lectura ampliada, confirmación, hijos conservados, borrado de rama, deshacer, rehacer, persistencia y móvil")
