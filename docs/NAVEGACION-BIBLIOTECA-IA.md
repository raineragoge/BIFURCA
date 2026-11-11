# Biblioteca y propuestas de IA

## Recorridos

- **Biblioteca → árbol:** un botón propio abre la biblioteca completa. La búsqueda examina nombres, descripción y conceptos. Los filtros y la ordenación solo afectan a la presentación. Abrir un árbol devuelve al espacio de trabajo. El título superior deja de ser un selector.
- **Ideas / IA → revisión:** se conserva el texto pegado. La vista compacta ofrece el botón **Expandir**; la ampliada muestra campos completos, ubicación cuando procede, color y decisión individual. **Volver** recupera el panel de origen; **Vista compacta** mantiene la selección; **Descartar** abandona las propuestas.
- **Completar árbol → revisión:** el prompt editable incluye la estructura y los IDs reales. La respuesta etiquetada puede crear conceptos en ramas distintas y varios niveles. Cada padre se resuelve por ID, luego por ruta completa; el nombre solo se usa si es inequívoco y no se ha dado una ruta. Cualquier duda exige selección manual. Los nodos nuevos aparecen como opciones con su ruta.
- **Confirmación:** solo las propuestas aceptadas, con padres válidos y sin duplicados ni ciclos, llegan al resumen. El botón final crea todos los nodos en un único `commit`; Deshacer revierte el lote completo.

## Protección de datos

El almacenamiento sigue en `bifurca_v3_app`; el respaldo y `bifurca-v4` permanecen compatibles. La vista previa, los colores elegidos y los borradores viven en memoria. Ninguna propuesta modifica los árboles hasta la confirmación. Los tests usan un perfil de navegador nuevo y un árbol de prueba añadido a ese perfil.

## Verificación

`tests/qa_navigation_ai.py` comprueba ID prioritario ante ruta contradictoria, ruta ante ID inexistente, nombres repetidos, corrección manual, propuesta hija de otra, padre rechazado, ciclo, duplicado, color por propuesta, campos internos, operación única de deshacer, persistencia tras recarga, navegación entre pantallas y versión móvil. `qa_redesign.py` cubre importación/exportación JSON y el resto de regresiones; `qa_refinement.py` cubre editor, glosario e imagen.

Capturas: [biblioteca](../tests/captures-navigation-ai/01-biblioteca-escritorio.png), [revisión](../tests/captures-navigation-ai/03-ubicaciones-corregidas.png), [confirmación](../tests/captures-navigation-ai/04-confirmacion.png), [móvil](../tests/captures-navigation-ai/06-biblioteca-movil.png).

## Pendiente

No hay integración directa con una API de IA: el usuario copia el prompt y pega la respuesta. No se ha desplegado esta iteración.
