# BIFURCA

**Un árbol para pensar y aprender.** Aplicación web estática de exploración visual que crece de arriba hacia abajo. Permite árboles de **decisiones e ideas** y mapas de **conocimientos y temarios**, usando el mismo lienzo y las mismas conexiones.

## Actualización propuesta v1.0 — nodos visuales

> **Seguridad de datos:** los árboles personales viven en `localStorage` del navegador, NO en este repositorio. **Antes de desplegar una nueva versión, desde la versión pública actual exporta una copia JSON de tus árboles.** No borres los datos de BIFURCA ni cambies de navegador antes de respaldarlos.

### Funciones nuevas

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

**Estado de desarrollo:** v1.0 en rama separada; se han validado sintaxis JavaScript, importación de los ocho temarios, migración de datos y distribución geométrica de auxiliares. **Pendiente:** prueba visual e interactiva completa en un navegador real y publicación.
