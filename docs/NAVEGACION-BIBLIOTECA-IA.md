# Biblioteca y propuestas de IA

## Recorridos

- **Biblioteca → árbol:** un botón propio abre la biblioteca completa. La búsqueda examina nombres, descripción y conceptos. Los filtros y la ordenación solo afectan a la presentación. Abrir un árbol devuelve al espacio de trabajo. El título superior deja de ser un selector.
- **Ideas / IA → revisión:** se conserva el texto pegado. Tras pegar o importar, se abre directamente una ventana centrada con una lista de propuestas y un editor amplio. Cada campo, color y padre es editable; las rutas se pueden buscar. **Volver al origen** recupera el texto; **Cerrar y volver al árbol** conserva el borrador para reanudar; **Descartar todo** lo elimina.
- **Completar árbol → revisión:** el prompt editable incluye la estructura y los IDs reales. La respuesta etiquetada puede crear conceptos en ramas distintas y varios niveles. Cada padre se resuelve por ID, luego por ruta completa; el nombre solo se usa si es inequívoco y no se ha dado una ruta. Cualquier duda exige selección manual. Los nodos nuevos aparecen como opciones con su ruta.
- **Confirmación:** solo las propuestas aceptadas, con padres válidos y sin duplicados ni ciclos, llegan al resumen. El botón final crea todos los nodos en un único `commit`; Deshacer revierte el lote completo.
- **Vista del árbol:** se abre desde una propuesta seleccionada y muestra solo su conexión provisional (y sus antecesores nuevos si depende de otra propuesta). Regresar al editor conserva todos los campos y decisiones.

## Protección de datos

El almacenamiento sigue en `bifurca_v3_app`; el respaldo y `bifurca-v4` permanecen compatibles. La vista previa, los colores elegidos y los borradores viven en memoria. Ninguna propuesta modifica los árboles hasta la confirmación. Los tests usan un perfil de navegador nuevo y un árbol de prueba añadido a ese perfil.

## Verificación

`tests/qa_navigation_ai.py` comprueba seis propuestas en escritorio y móvil, edición de nombre, explicación, ejemplo y notas, ID prioritario ante ruta contradictoria, ruta ante ID inexistente, nombres repetidos, búsqueda y corrección de padre, propuesta hija de otra, padre rechazado, ciclo, duplicado, color por propuesta, cierre y reanudación, vista provisional sin superposición, confirmación de cuatro propuestas, operación única de deshacer, persistencia tras recarga, importación externa y navegación fluida con treinta propuestas. `qa_redesign.py` cubre importación/exportación JSON y el resto de regresiones; `qa_refinement.py` cubre editor, glosario e imagen.

Capturas: [biblioteca](../tests/captures-navigation-ai/01-biblioteca-escritorio.png), [seis propuestas](../tests/captures-navigation-ai/02-revision-expandida.png), [ubicación provisional](../tests/captures-navigation-ai/03-ubicacion-en-arbol.png), [confirmación](../tests/captures-navigation-ai/04-confirmacion.png), [seis propuestas en móvil](../tests/captures-navigation-ai/09-seis-propuestas-movil.png), [treinta propuestas](../tests/captures-navigation-ai/10-treinta-propuestas.png).

## Pendiente

No hay integración directa con una API de IA: el usuario copia el prompt y pega la respuesta. No se ha desplegado esta iteración.
