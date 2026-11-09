# BIFURCA

**Un árbol para pensar y aprender.** Aplicación web estática de exploración visual que crece de arriba hacia abajo. Permite árboles de **decisiones e ideas** y mapas de **conocimientos y temarios**, usando el mismo lienzo y las mismas conexiones.

## Abrir la aplicación

Abre `index.html` en un navegador moderno. No requiere instalar dependencias ni montar un servidor.

## Árboles disponibles al abrir

La **v0.7 muestra automáticamente ocho mapas de conocimiento**, sin importar archivos: mapa general, IA, Machine Learning, Big Data, MongoDB, Python/SQL, Matemáticas/Bayes y proyectos. Los verás en el **panel lateral «Temarios incluidos»** y puedes cambiar entre ellos con un clic.

- En ordenador, la biblioteca queda abierta a la izquierda. El botón **Árboles** permite plegarla y volver a abrirla.
- En móvil, toca **Árboles** para abrirla como panel lateral y selecciona un temario.
- El botón **Importar JSON** está destacado en la barra superior y repetido al pie del panel. Sirve para **añadir otros mapas tuyos**; no es necesario para los ocho incluidos.
- Cada árbol tiene un **icono de papelera** a la derecha en la biblioteca, tanto en ordenador como en móvil. Se pide confirmación antes de borrarlo.
- Si eliminas un **temario incluido**, se oculta y no reaparece al recargar. Puedes recuperarlo con **Restaurar temarios ocultos** (recupera la versión original, no sus modificaciones anteriores).
- Si eliminas un **árbol personal**, se elimina de este navegador. **Exporta primero un JSON** si quieres guardar una copia; no existe papelera para estos árboles.
- **Organizar biblioteca** también permite renombrar, duplicar y eliminar tus árboles.

Los temarios forman parte del archivo `index.html` y no necesitan conexión de red adicional para cargarse. Los ficheros de `temarios/` siguen disponibles como copias independientes y para compartir.

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

## Funcionalidades (v0.8)

- Árboles de decisiones con notas y estados semánticos: positivo, negativo, incierto y neutral.
- Mapas de conocimientos con título, **explicación**, **ejemplo práctico** y **notas personales** por concepto.
- Ramas y subramas, plegado/desplegado, enfoque, conexiones secundarias, zoom y navegación por el lienzo.
- Deshacer/rehacer, biblioteca lateral siempre visible en escritorio y duplicado de árboles.
- Ocho mapas precargados (304 conceptos en total) y migración automática desde versiones anteriores, sin sobrescribir árboles ya importados ni sus modificaciones.
- Importación/exportación JSON y exportación de texto.
- Formato JSON **bifurca-v4**, compatible con importaciones previas **bifurca-v3** y el formato legado simple.
- Cuatro temas (Arcilla, Lino, Salvia e Iris), modo oscuro, animación de bifurcación y efectos sonoros opcionales.
- Preguntas orientativas sin conexión y un prompt contextual para copiar a una IA externa. **No hay conexión directa con una IA ni generación automática a partir de un PDF.**

## Almacenamiento y privacidad

Los datos se guardan automáticamente en el almacenamiento local del navegador (`localStorage`), sin base de datos ni sincronización entre dispositivos. La versión 0.7 **mantiene la misma clave de almacenamiento que las versiones anteriores** para conservar los árboles anteriores, tratándolos como árboles de decisiones. Las explicaciones y ejemplos se guardan junto a cada concepto.

**Exporta periódicamente una copia JSON.** Si borras los datos del navegador o cambias de dispositivo, necesitarás importar dicha copia.

## Verificación

Se ha comprobado la sintaxis JavaScript y, mediante pruebas automatizadas de lógica, la confirmación y cancelación del borrado, la eliminación de árboles activos e inactivos, el caso del último árbol, la conservación de datos personales, la restauración de temarios y la persistencia tras recargar. No se ha realizado una prueba visual completa del flujo en navegador.

## Despliegue

Puede publicarse desde la rama `main` y la carpeta raíz mediante GitHub Pages, tras activar Pages en la configuración del repositorio, o mediante Cloudflare Pages. El punto de entrada es `index.html`.

**Estado:** v0.8 · biblioteca visible, eliminación de árboles y restauración de temarios · sin backend.
