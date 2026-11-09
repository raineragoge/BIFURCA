# BIFURCA

Un lienzo para explorar decisiones, ideas y consecuencias mediante un árbol visual que crece **de arriba hacia abajo** y permite ramificaciones recursivas.

## Abrir

Abre `index.html` en un navegador moderno. Es una aplicación estática que no requiere instalar dependencias ni disponer de servidor.

## Funcionalidades (v0.5)

- Crear y editar nodos, con ramas y subramas ilimitadas en la estructura de datos.
- Notas desplegables y etiquetas de significado (positivo, negativo, incertidumbre, neutral).
- Modo enfoque, conexiones secundarias entre ramas y navegación por el lienzo.
- Deshacer y rehacer.
- Biblioteca de árboles, con almacenamiento local en el navegador y herramientas de importación y exportación JSON.
- Cuatro temas visuales (Arcilla, Lino, Salvia e Iris) y modos claro/oscuro.
- Animación de bifurcación con un pequeño temblor y separación elástica.
- Efectos de sonido sintetizados en el navegador; botón de silencio y control de volumen.
- Sugerencias locales para explorar posibilidades y opción de copiar el contexto para usar una IA externa. **No incluye integración directa con un modelo de IA.**

## Privacidad y persistencia

El contenido se guarda **localmente en el navegador**, no en GitHub ni en una base de datos. Exporta periódicamente tus árboles a JSON para hacer copias de seguridad. Abrir la app en otro navegador o dispositivo no sincroniza los datos.

## Despliegue

Para publicar mediante GitHub Pages, configura el origen de Pages en la rama principal (`main`) y en la carpeta raíz (`/`). El archivo `index.html` será la página de entrada.

## Estado

Versión 0.5 — prototipo de aplicación web estática, sin backend.