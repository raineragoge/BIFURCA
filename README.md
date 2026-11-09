# BIFURCA

**Un árbol para pensar y aprender.** Aplicación web estática de exploración visual que crece de arriba hacia abajo. Permite árboles de **decisiones e ideas** y mapas de **conocimientos y temarios**, usando el mismo lienzo y las mismas conexiones.

## Abrir la aplicación

Abre `index.html` en un navegador moderno. No requiere instalar dependencias ni montar un servidor.

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

## Funcionalidades (v0.6)

- Árboles de decisiones con notas y estados semánticos: positivo, negativo, incierto y neutral.
- Mapas de conocimientos con título, **explicación**, **ejemplo práctico** y **notas personales** por concepto.
- Ramas y subramas, plegado/desplegado, enfoque, conexiones secundarias, zoom y navegación por el lienzo.
- Deshacer/rehacer, biblioteca y duplicado de árboles.
- Importación/exportación JSON y exportación de texto.
- Formato JSON **bifurca-v4**, compatible con importaciones previas **bifurca-v3** y el formato legado simple.
- Cuatro temas (Arcilla, Lino, Salvia e Iris), modo oscuro, animación de bifurcación y efectos sonoros opcionales.
- Preguntas orientativas sin conexión y un prompt contextual para copiar a una IA externa. **No hay conexión directa con una IA ni generación automática a partir de un PDF.**

## Almacenamiento y privacidad

Los datos se guardan automáticamente en el almacenamiento local del navegador (`localStorage`), sin base de datos ni sincronización entre dispositivos. La versión 0.6 **mantiene la misma clave de almacenamiento que la 0.5** para conservar los árboles anteriores, tratándolos como árboles de decisiones. Las explicaciones y ejemplos se guardan junto a cada concepto.

**Exporta periódicamente una copia JSON.** Si borras los datos del navegador o cambias de dispositivo, necesitarás importar dicha copia.

## Verificación

Se ha comprobado la sintaxis de JavaScript y el análisis de un esquema sangrado, incluidas ramas hermanas, explicaciones, ejemplos y lectura de árboles anteriores. No se ha realizado una prueba completa de interfaz en navegador ni un despliegue web validado.

## Despliegue

Puede publicarse desde la rama `main` y la carpeta raíz mediante GitHub Pages, tras activar Pages en la configuración del repositorio, o mediante Cloudflare Pages. El punto de entrada es `index.html`.

**Estado:** v0.6 · primera versión funcional del modo Conocimientos · sin backend.
