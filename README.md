# BIFURCA

**Un árbol para pensar y aprender.** Aplicación web estática de exploración visual que crece de arriba hacia abajo. Permite árboles de **decisiones e ideas** y mapas de **conocimientos y temarios**, usando el mismo lienzo y las mismas conexiones.

## Refinamiento de biblioteca, orientación y editor

La biblioteca lateral ahora ocupa menos espacio y agrupa con claridad los temarios incluidos, los árboles personales, la búsqueda y las acciones. La ayuda «Explorar el mapa» puede reducirse a un botón discreto; el estado se guarda en la nueva clave de interfaz `bifurca_guide_collapsed_v1` y permanece al cambiar de árbol y recargar. En móvil aparece reducida por defecto.

El editor separa identidad, explicación y ejemplo, clasificación, notas, imagen y gestión de rama. Notas e imagen son secciones desplegables que conservan el texto al cerrarse. Las acciones de eliminación están apartadas; el encabezado y «Guardar cambios» permanecen visibles mientras se desplaza el contenido, también en móvil. Se conservaron los cinco colores configurables, imágenes por URL o archivo, conexiones, IA, cancelar y las confirmaciones de borrado.

La [comparación visual y las decisiones de diseño](docs/REFINAMIENTO-BIBLIOTECA-EDITOR.md) incluyen capturas del antes y el después. `python tests/qa_refinement.py`, servido desde la raíz en `127.0.0.1:8012`, prueba biblioteca, ayuda persistente, edición, imágenes, colores, glosario, cancelación, eliminación protegida, teclado y tamaños móviles. La rama `archive/redesign-ux-ui-2026-before-refinement` conserva el estado anterior.

**Datos y despliegue:** las claves existentes, el formato `bifurca-v4` y la lógica de árboles no cambian. Esta iteración no se ha desplegado; la exportación y verificación de una copia real del navegador personal siguen siendo requisitos previos a publicar.

## Rediseño UX/UI — rama `feature/redesign-ux-ui-2026`

Esta rama reorganiza la interfaz como un espacio de exploración cartográfica: el árbol conserva el protagonismo, la barra superior muestra las acciones frecuentes y «Más herramientas» reúne las opciones de configuración y exportación. La selección de un nodo abre un panel de lectura con su ruta, explicación, ejemplo, notas y acciones rápidas. En móvil, ese panel aparece como una hoja inferior que se puede cerrar.

El encabezado del lienzo muestra el árbol activo y cuántos conceptos están visibles. Una guía breve explica cómo abrir ramas y buscar entre temarios. Se mejoraron los estados de enfoque, la jerarquía de tarjetas, las conexiones, los diálogos y la biblioteca. Las tarjetas admiten ↑/↓, Inicio/Fin, ←/→ para recorrer y plegar/desplegar ramas, y F2 para editar; Enter y Espacio mantienen su acción original.

**Compatibilidad:** no cambian las claves `bifurca_v3_app`, `bifurca_v3_before_visual_v1` ni `bifurca_audio_v1`, el formato `bifurca-v4`, la migración, el importador/exportador ni la estructura de árboles. `redesign.css` y el panel contextual solo afectan a la interfaz. Se conservaron los ocho temarios, sonidos, glosarios, filtros, IA revisable, conexiones y copias de seguridad.

**Pruebas:** `python tests/qa_redesign.py` con Playwright en un perfil nuevo comprueba árbol pequeño y grande, navegación, búsqueda, filtro, edición, deshacer/rehacer, conexión transversal, importación, exportación, backup, persistencia, glosario, sonido, IA, móvil y movimiento reducido. Las capturas comparativas están en [`docs/capturas`](docs/capturas). El análisis y las limitaciones están en [`docs/REDISENO-UX-UI.md`](docs/REDISENO-UX-UI.md).

**Publicación:** la rama no se ha desplegado. Antes de reemplazar la web pública, exporta una copia JSON completa desde el navegador que contiene tus árboles personales y verifica su lectura en una sesión aislada. La prueba automatizada usa exclusivamente datos de prueba.

## v1.3.0 — filtro por glosario, microsonidos y temas diferenciados

- **Filtrar por color:** nuevo botón **◉ Filtrar** en el lienzo. Muestra los cinco significados definidos en el glosario del árbol y la cantidad de **nodos visibles** de cada color. Al elegir uno, los demás nodos y sus conexiones se vuelven semitransparentes. Puedes volver a **Mostrar todos los colores** o pulsar de nuevo el color seleccionado. El filtro es temporal: no borra ni edita datos, y se reinicia al cambiar de árbol.
- **Enfoque con salida intuitiva:** al estar en modo **Enfocar**, un clic en el fondo del lienzo restablece la vista general sin alterar ramas. Un movimiento de arrastre no lo cierra; también puedes salir con **Escape**. Al hacer clic fuera del filtro se oculta su panel.
- **Sonidos al desplegar y plegar:** los sonidos existentes se refuerzan para que sean audibles y diferenciables. También suena al usar **Plegar niveles**; siguen respetando el botón **Sonidos**, el volumen y el modo de accesibilidad de movimiento reducido.
- **Color más presente en los nodos:** los nodos marcados tienen un borde y una franja lateral de su color, además de un fondo suavemente tintado. El selector de color del editor y las cinco filas del glosario destacan visualmente la selección.
- **Diseño más despejado:** barra superior más ligera, sombras menos intensas, jerarquía de botones más discreta y panel de filtro plegado por defecto.
- **Cuatro temas más diferenciados:** Arcilla, Lino, Salvia e Iris ahora varían más claramente en paleta y patrón del lienzo, también en modo oscuro.
- **Sin imágenes sugeridas por IA:** el prompt nuevo solo pide **CONCEPTO**, **EXPLICACION**, **EJEMPLO** y **NOTAS**. Se ha retirado la casilla de imágenes sugeridas y ya no se añaden sugerencias de imagen a las notas. **Se conservan las imágenes que ya estaban guardadas y la opción de adjuntarlas manualmente**; un buscador integrado podrá añadirse más adelante. Las respuestas antiguas con campo IMAGEN pueden leerse, pero este se ignora.

**Protección de los árboles:** la clave local `bifurca_v3_app`, el backup `bifurca_v3_before_visual_v1`, el formato de exportación y las funciones de deshacer no cambian. Los filtros y los estados de los paneles son solo de interfaz.

**Verificación:** sintaxis JS completa, estructura de controles, compatibilidad del parser y pruebas de filtrado/teclas y sonidos (sin pruebas de audio perceptual). Pendientes prueba visual en navegador real y verificación del despliegue Cloudflare.

## v1.2.0 — respuestas de IA sin JSON

Para evitar los fallos de pegado de respuestas JSON desde ChatGPT, **BIFURCA solicita ahora texto plano etiquetado**. Es el formato recomendado, no requiere comillas, llaves, corchetes ni caracteres escapados.

Ejemplo:

```text
CONCEPTO: GraphSAGE
EXPLICACION: Agrega información de una muestra de nodos vecinos.
EJEMPLO: Representar productos según sus conexiones.
NOTAS: Muestreo de vecinos.
IMAGEN: Diagrama de agregación.
---
CONCEPTO: GAT
EXPLICACION: Utiliza atención para ponderar los vecinos.
EJEMPLO: Analizar una red de artículos científicos.
NOTAS: Arquitectura GNN.
IMAGEN:
---
```

Cada bloque se interpreta como **un único nodo** con título, explicación, ejemplo, notas y sugerencia visual dentro de notas. La vista previa muestra el contenido y exige aceptar o rechazar propuestas; ninguna sugerencia se guarda antes de su aprobación. Se admite `EXPLICACIÓN` con tilde, encabezados en negrita y texto partido en varias líneas.

Los JSON anteriores, los listados simples y la importación desde archivo siguen disponibles como formatos compatibles, pero **ya no son el flujo preferido**. Si falla un JSON viejo, el error incluye un código Unicode de diagnóstico y se recomienda generar una respuesta nueva con el formato etiquetado.

La nueva versión conserva las claves de almacenamiento local y de respaldo. Pruebas realizadas: sintaxis completa JavaScript, lectura de formato etiquetado, acentos, multilínea, JSON clásico, Unicode anómalo y líneas antiguas. Pendiente: prueba visual interactiva y confirmación del despliegue en Cloudflare.

## v1.1.4 — importar propuestas directamente desde el portapapeles

**Flujo recomendado:** en ChatGPT copia el JSON generado, vuelve a **Ideas / IA** y pulsa **Pegar del portapapeles y revisar**. BIFURCA lee el texto, valida sus propuestas y muestra inmediatamente las tarjetas provisionales, con sus explicaciones y ejemplos **dentro**; puedes aceptar/rechazar cada una. **No hace falta descargar ni subir archivos.**

El botón necesita permiso del navegador para leer el portapapeles y un contexto seguro HTTPS (el Worker de BIFURCA dispone de HTTPS). Si el navegador deniega ese permiso, se muestra una alternativa: pegar manualmente en el campo con **Ctrl+V → Revisar texto pegado**. El importador por archivo se conserva como recurso adicional. Las propuestas no se guardan antes de confirmarlas.

La **integración directa con un modelo de IA** para completar ramas sin copiar respuestas todavía está pendiente de configurar en el backend. El portapapeles elimina los pasos de descarga/importación de archivos, no elimina el paso de copiar de ChatGPT.

## v1.1.3 — cargar propuestas desde archivo JSON

En **Ideas / IA**, el botón **Cargar respuesta JSON** permite seleccionar un archivo `.json` o `.txt` y convertir sus `propuestas` en una **vista previa con aceptación individual**. Esta opción evita los fallos al copiar texto enriquecido desde el chat. La importación **no modifica el árbol** hasta pulsar **Añadir seleccionadas**.

El pegado también se ha reforzado para normalizar espacios Unicode no estándar, caracteres invisibles, comillas tipográficas, entidades de comillas HTML, llaves exteriores duplicadas y comillas escapadas en el JSON. No usa `eval` ni acepta cualquier expresión JavaScript: el texto corregido debe convertirse en JSON válido, con una lista de propuestas.

**Pruebas:** diez variantes de entrada aceptadas, dos casos inválidos rechazados, sintaxis del script validada. Pendiente: verificación visual en navegador y confirmación del despliegue público.

## v1.1.2 — corrección al pegar JSON desde ChatGPT

El importador acepta JSON completo y válido, bloques de código `json`, texto introductorio/conclusiones alrededor del JSON, etiquetas de copia como `<escape>` y secuencias literales de salto de línea (`\\n`) fuera de las cadenas. Sigue aceptando listas antiguas y líneas separadas por `|`.

El importador valida que exista `propuestas` y cada elemento tenga `concepto`. Muestra un mensaje más específico si el JSON está realmente mal formado, incompleto o no contiene conceptos válidos. **Nunca modifica el árbol hasta la aceptación visual de cada propuesta**.

Se han comprobado mediante pruebas JavaScript: JSON puro, Markdown, texto adicional, etiquetas, saltos escapados, arrays, texto antiguo, JSON entrecomillado, JSON truncado, JSON incorrecto y lista vacía. Pendiente validación visual de navegador y comprobación de la publicación en Cloudflare.

## v1.1 — completar conceptos por dentro (10/11/2026)

Al pulsar **Ideas / IA → Copiar prompt para IA**, BIFURCA solicita una respuesta JSON donde cada propuesta contenga un **concepto** y su **explicacion**, **ejemplo** y **notas**. La propuesta se previsualiza como una sola tarjeta, con su título y contenidos internos. Solo después de aprobarla, los datos pasan al nodo real; el detalle se deja desplegado. **Las explicaciones no se crean como ramas hijas**.

Formato recomendado:

```json
{
  "propuestas": [
    {
      "concepto": "K-Means",
      "explicacion": "Agrupa datos según su cercanía a K centroides.",
      "ejemplo": "Segmentar clientes por patrones de compra.",
      "notas": "K se elige antes del entrenamiento.",
      "imagen_sugerida": "Diagrama de asignación al centroide más próximo"
    }
  ]
}
```

El campo `imagen_sugerida` es opcional y se guarda como sugerencia en las notas; **no descarga ninguna imagen ni inventa enlaces**. Se aceptan también variantes de nombres de campos en español e inglés, líneas `Concepto | Explicación | Ejemplo | Notas` y listas antiguas con solo títulos. Los datos existentes, los árboles exportados y el formato `bifurca-v4` permanecen compatibles.

**Limitación actual:** BIFURCA genera un prompt para una IA externa y permite pegar su respuesta estructurada. Todavía no llama a un modelo directamente; «Completar con un clic» necesita un backend de IA seguro.

**Pruebas de esta entrega:** análisis sintáctico de todo el JavaScript, pruebas de lectura JSON y formatos antiguos, rechazo de JSON incorrecto, aprobación parcial de propuestas, guardado en una sola operación y preservación de las claves de almacenamiento. **Pendiente:** prueba completa visual e interactiva en navegador y confirmación de la publicación en Cloudflare.

## Actualización propuesta v1.0 — nodos visuales

> **Seguridad de datos:** los árboles personales viven en `localStorage` del navegador, NO en este repositorio. **Antes de desplegar una nueva versión, desde la versión pública actual exporta una copia JSON de tus árboles.** No borres los datos de BIFURCA ni cambies de navegador antes de respaldarlos.

### Funciones nuevas

- **Vista previa revisable de sugerencias:** tanto las preguntas rápidas como las respuestas de una IA externa pegadas por el usuario se muestran como nodos temporales de borde discontinuo, conectados visualmente a la rama de origen. Un panel permite **Aceptar/Rechazar cada sugerencia**, descartar todas o pulsar **Añadir seleccionadas** para incorporarlas en una sola operación deshacible. Los nodos de vista previa **no se guardan en `localStorage` ni en JSON** antes de confirmarlos. La versión actual NO llama automáticamente a un modelo; el backend de IA para completar con un clic continúa pendiente.


- **Imagen por nodo:** pega una URL HTTPS de fotografía o sube un PNG/JPG/WebP/GIF; la imagen subida se comprime y se almacena dentro del JSON del árbol. Las imágenes de URL externa requieren conexión.
- **Cinco colores de nodos:** gris, verde, amarillo, rojo y azul. **Colores** abre un glosario editable en cada árbol; los estados de colores anteriores se mantienen.
- **Animaciones:** breve realce al guardar información, dibujo al conectar y desaparición con sonido al eliminar una rama. Se respeta la opción de silenciar y el ajuste de accesibilidad `prefers-reduced-motion`.
- **Desconectar sin borrar:** la sección «Conexiones con otras ramas» del editor permite quitar enlaces transversales; **Desvincular** convierte una rama jerárquica en una independiente, conservando sus descendientes y notas.
- **Nodo auxiliar:** crear notas independientes, desplazarlas arrastrando por la cabecera, editarlas y conectarlas a otras ramas.
- **Sugerencias visuales:** el botón **Ideas / IA** incluye «Sugerir imágenes y diagramas». Esto mejora el prompt que se copia para ChatGPT; BIFURCA **no** tiene conexión directa a modelos ni descarga imágenes automáticamente.
- **Completar tabla:** crea un prompt con los conceptos, explicaciones, ejemplos, conexiones y significados de colores del árbol abierto para ampliarlo usando ChatGPT. No sobrescribe datos automáticamente.
- **Copia de seguridad completa:** disponible en la barra lateral y desde «Organizar biblioteca»; guarda toda la biblioteca, incluyendo imágenes incrustadas y glosarios. «Recuperar copia» **fusiona** árboles sin borrar los actuales. Los duplicados modificados se recuperan como copias independientes.
- **Copia preventiva de migración:** la primera vez que se abre la versión nueva, se intenta guardar una instantánea del estado anterior en la misma ubicación del navegador. «Recuperar versión anterior» permite importar los árboles de esa instantánea. Esta protección local NO reemplaza un JSON descargado.

### Advertencias importantes

1. El `localStorage` tiene límite de espacio, variable según navegador. Para muchos nodos ilustrados, prioriza URLs de imágenes o subidas pequeñas; cuando se agote el espacio, las nuevas imágenes no podrán persistirse. **Exporta periódicamente toda la biblioteca.**
2. No existe sincronización entre navegadores o dispositivos. GitHub solo conserva el código; el archivo HTML no contiene tus árboles personales.
3. Los nodos auxiliares guardados aparecen en las exportaciones JSON de la versión nueva. Las versiones antiguas no permiten editar todas sus propiedades, por lo que conviene importar las copias nuevas también en la v1.0.
4. No se ha desplegado automáticamente esta rama en la web pública. Antes de actualizar, respalda los datos del navegador usado habitualmente.

## Abrir la aplicación

Abre `index.html` en un navegador moderno. No requiere instalar dependencias ni montar un servidor.

## Árboles disponibles al abrir

La **v0.9 muestra automáticamente ocho mapas de conocimiento**, sin importar archivos: mapa general, IA, Machine Learning, Big Data, MongoDB, Python/SQL, Matemáticas/Bayes y proyectos. Los verás en el **panel lateral «Temarios incluidos»** y puedes cambiar entre ellos con un clic.

- En ordenador, la biblioteca queda abierta a la izquierda. El botón **Árboles** permite plegarla y volver a abrirla.
- En móvil, toca **Árboles** para abrirla como panel lateral y selecciona un temario.
- El botón **Importar JSON** está destacado en la barra superior y repetido al pie del panel. Sirve para **añadir otros mapas tuyos**; no es necesario para los ocho incluidos.
- Cada árbol tiene un **icono de papelera** a la derecha en la biblioteca, tanto en ordenador como en móvil. Se pide confirmación antes de borrarlo.
- Si eliminas un **temario incluido**, se oculta y no reaparece al recargar. Puedes recuperarlo con **Restaurar temarios ocultos** (recupera la versión original, no sus modificaciones anteriores).
- Si eliminas un **árbol personal**, se elimina de este navegador. **Exporta primero un JSON** si quieres guardar una copia; no existe papelera para estos árboles.
- **Organizar biblioteca** también permite renombrar, duplicar y eliminar tus árboles.

Los temarios forman parte del archivo `index.html` y no necesitan conexión de red adicional para cargarse. Los ficheros de `temarios/` siguen disponibles como copias independientes y para compartir.

## Leer y buscar en los temarios

- **Escalonado** es la vista predeterminada: el árbol crece verticalmente, con cada subtema sangrado. La rueda del ratón desplaza el lienzo hacia arriba o abajo; usa los botones **+ / −** para el zoom.
- El botón **Escalonado / Horizontal** dentro del lienzo permite recuperar la distribución horizontal tradicional.
- Los ocho temarios incluidos aparecen inicialmente con sus **bloques principales plegados** para evitar cientos de tarjetas a la vez. Pulsa un bloque para abrir o cerrar sus subramas. El lápiz sirve para editar.
- **Plegar niveles** vuelve a cerrar los bloques de segundo nivel y posteriores.
- El **buscador de la biblioteca** encuentra coincidencias en títulos, explicaciones, ejemplos y notas de todos los árboles guardados, aunque estén plegados. Ignora mayúsculas y tildes; por ejemplo, «regresion» encuentra «regresión». Al pulsar un resultado, BIFURCA abre las ramas necesarias y te lleva al concepto.
- Usa **Ctrl+K** (o **⌘K** en Mac) para ir al buscador.
- Los cambios de disposición y plegado se guardan localmente; los datos anteriores se conservan.

## Crear un árbol

1. Pulsa **Nuevo** y escribe un nombre.
2. Elige **Decisiones e ideas** o **Conocimientos y temarios**.
3. Para conocimientos, puedes empezar con un mapa vacío o pegar un esquema de texto usando sangrías.
4. Amplía, edita, pliega y conecta nodos dentro del lienzo.

### Ejemplo de esquema para estudiar

Pega el siguiente texto en el formulario del modo Conocimientos:

```text
Machine Learning | Disciplina que aprende patrones de datos.
  Aprendizaje supervisado | Usa ejemplos etiquetados.
    Regresión | Predice valores continuos.
      Regresión lineal | Ajusta una relación lineal. | Predecir precios.
    Clasificación | Predice categorías.
      Regresión logística | Clasificador probabilístico. | Detectar spam.
  Aprendizaje no supervisado
    Clustering
      DBSCAN | Encuentra regiones densas y ruido.
```

La primera línea será el nodo raíz. Cada nivel de sangría crea subramas. También se admiten guiones de lista y tabulaciones. El formato **`concepto | explicación | ejemplo`** es opcional. Usa **Usar ejemplo de Machine Learning** para probarlo sin pegar nada.

La sangría representa una relación jerárquica. Para relaciones transversales, usa el botón de **conectar nodos**; no es necesario forzar una clasificación incorrecta.

## Funcionalidades (v1.0, compatible con v0.9)

- Árboles de decisiones con notas y estados semánticos: positivo, negativo, incierto y neutral.
- Mapas de conocimientos con título, **explicación**, **ejemplo práctico** y **notas personales** por concepto.
- Ramas y subramas, plegado/desplegado, enfoque, conexiones secundarias, zoom y navegación por el lienzo.
- Deshacer/rehacer, biblioteca lateral siempre visible en escritorio y duplicado de árboles.
- Ocho mapas precargados (304 conceptos en total) con apertura inicial por bloques y migración automática desde versiones anteriores, conservando sus conceptos y notas.
- Vista escalonada de anchura limitada, vista horizontal opcional, búsqueda transversal con navegación directa y desplazamiento vertical mediante rueda.
- Importación/exportación JSON y exportación de texto.
- Formato JSON **bifurca-v4**, compatible con importaciones previas **bifurca-v3** y el formato legado simple.
- Cuatro temas (Arcilla, Lino, Salvia e Iris), modo oscuro, animación de bifurcación y efectos sonoros opcionales.
- Preguntas orientativas sin conexión y un prompt contextual para copiar a una IA externa. **No hay conexión directa con una IA ni generación automática a partir de un PDF.**

## Almacenamiento y privacidad

Los datos se guardan automáticamente en el almacenamiento local del navegador (`localStorage`), sin base de datos ni sincronización entre dispositivos. La versión 0.7 **mantiene la misma clave de almacenamiento que las versiones anteriores** para conservar los árboles anteriores, tratándolos como árboles de decisiones. Las explicaciones y ejemplos se guardan junto a cada concepto.

**Exporta periódicamente una copia JSON.** Si borras los datos del navegador o cambias de dispositivo, necesitarás importar dicha copia.

## Verificación

Se han comprobado la sintaxis JavaScript, la búsqueda con y sin tildes, la apertura de ramas ocultas desde resultados y la distribución de los ocho temarios sin solapamientos de tarjetas. Se ha validado la reducción de anchura de la vista escalonada frente a la horizontal. Falta una prueba visual completa en navegador y verificar el despliegue público.

## Despliegue

Puede publicarse desde la rama `main` y la carpeta raíz mediante GitHub Pages, tras activar Pages en la configuración del repositorio, o mediante Cloudflare Pages. El punto de entrada es `index.html`.

**Estado de desarrollo:** v1.0 en rama separada; se han validado sintaxis JavaScript, importación de los ocho temarios, migración de datos y distribución geométrica de auxiliares. **Pendiente:** prueba visual e interactiva completa en un navegador real, conexión a un backend de IA para completar automáticamente y publicación.
