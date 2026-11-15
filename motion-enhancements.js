/* BIFURCA Motion: choreografía ligera para ramas y conexiones. */
(() => {
  'use strict';
  const MAX_GHOSTS = 12;
  let ghosts = 0;
  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));
  const reduceMotion = () => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches === true;

  function enterNode(element, point, parent, order = 0) {
    if (!element?.animate || !parent || reduceMotion()) return;
    const dx = clamp((parent.x - point.x) * .34, -105, 105);
    const dy = clamp((parent.y + parent.h * .6 - point.y) * .34, -75, 75);
    element.animate([
      { opacity: 0, transform: `translate(${dx}px, ${dy}px) scale(.92)` },
      { opacity: 1, transform: 'translate(0, 0) scale(1)' }
    ], { duration: 490, delay: Math.min(order * 25, 150), easing: 'cubic-bezier(.22,.88,.28,1)', fill: 'backwards' });
  }

  function exitNode(element, oldPoint, parentPoint, layer) {
    if (!element?.animate || !oldPoint || !parentPoint || !layer || reduceMotion() || ghosts >= MAX_GHOSTS) return;
    const ghost = element.cloneNode(true);
    ghost.classList.remove('selected', 'fresh', 'link-target', 'mitosis-parent', 'mitosis-sibling');
    ghost.setAttribute('aria-hidden', 'true');
    ghost.tabIndex = -1;
    ghost.inert = true;
    ghost.style.pointerEvents = 'none';
    ghost.style.transition = 'none';
    ghost.style.zIndex = '2';
    // El clon es visual: no tiene escuchas ni participa en el mapa o el almacenamiento.
    layer.appendChild(ghost);
    ghosts += 1;
    const dx = clamp((parentPoint.x - oldPoint.x) * .24, -75, 75);
    const dy = clamp((parentPoint.y - oldPoint.y) * .24, -65, 65);
    const anim = ghost.animate([
      { opacity: 1, transform: 'translate(0, 0) scale(1)' },
      { opacity: 0, transform: `translate(${dx}px, ${dy}px) scale(.88)` }
    ], { duration: 230, easing: 'cubic-bezier(.4,0,1,1)', fill: 'forwards' });
    let cleaned = false;
    const clean = () => { if (cleaned) return; cleaned = true; ghost.remove(); ghosts -= 1; };
    anim.addEventListener('finish', clean, { once: true });
    anim.addEventListener('cancel', clean, { once: true });
  }

  function drawConnector(path) {
    if (!path?.animate || reduceMotion()) return;
    try {
      const length = path.getTotalLength();
      if (!Number.isFinite(length) || length < 2) return;
      path.animate([
        { opacity: .16, strokeDasharray: `${length}`, strokeDashoffset: `${length}` },
        { opacity: 1, strokeDasharray: `${length}`, strokeDashoffset: '0' }
      ], { duration: 520, easing: 'cubic-bezier(.22,.88,.28,1)' });
    } catch (_) { /* SVG no disponible: mantener la línea estática. */ }
  }

  window.BIFURCA_MOTION = Object.freeze({ enterNode, exitNode, drawConnector });
})();
