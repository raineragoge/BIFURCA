# BIFURCA — Instrucciones para Codex

## Prioridad: integridad de datos
- Nunca borrar, restablecer ni migrar datos del navegador sin autorización explícita. La app conserva mapas, notas y conexiones locales.
- No alterar claves de almacenamiento, esquema, importación/exportación ni mapas de ejemplo al realizar mejoras de animación.
- No modificar `main` directamente: trabajar en ramas, revisar el diff y validar antes de fusionar o desplegar.
- No alterar la lógica de editar, añadir, borrar, conectar, deshacer/rehacer, cambiar mapa, búsqueda o glosarios por cambios de movimiento.

## Animación
- Consultar `.agents/skills/motion-design/SKILL.md` y referencias enlazadas para ritmo y microinteracciones.
- Para GSAP: `.agents/skills/gsap-core/SKILL.md`, `.agents/skills/gsap-timeline/SKILL.md` y `.agents/skills/gsap-performance/SKILL.md`.
- BIFURCA usa HTML, CSS, JavaScript, SVG, Web Animations API y requestAnimationFrame; no es React. Priorizar mejorar el motor existente antes de añadir frameworks o dependencias CDN.
- Coordinar transiciones de nodos y conexiones, preferir transform y opacity, limitar el trabajo en árboles grandes y respetar `prefers-reduced-motion`.
- No interferir con arrastre del lienzo, zoom, teclado, pulsación de nodos, enlaces ni acciones del editor.

## Verificación
- Revisar las pruebas de `tests/` y probar escritorio/móvil, ramas abiertas/cerradas, árboles densos y movimiento reducido antes de publicar.
- Documentar las limitaciones de validación del PR. No afirmar que un despliegue funciona si no se ha comprobado.
