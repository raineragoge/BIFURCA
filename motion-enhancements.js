/* Transient scene coordinates, in the same space as the SVG paths. */
(() => {
  'use strict';
  const flights = new Map();
  const exits = new Map();
  const ease = 'cubic-bezier(.2,0,.18,1)';

  function point(id, fallback) {
    const flight = flights.get(id) || exits.get(id);
    if (!flight) return fallback;
    const t = flight.animation.effect.getComputedTiming().progress ?? 0;
    const {from, to} = flight;
    return {x: from.x + (to.x - from.x) * t, y: from.y + (to.y - from.y) * t, h: to.h};
  }

  function snapshot(layout) {
    const previous = new Map(layout);
    for (const [id, flight] of flights) {
      previous.set(id, point(id, flight.to));
    }
    for (const [id, flight] of exits) previous.set(id, point(id, flight.to));
    return previous;
  }

  function stopNode(id) {
    flights.get(id)?.animation.cancel();
    flights.delete(id);
  }

  function moveNode(element, from, to, delay = 0, entering = false) {
    const id = element.dataset.id;
    const active = flights.get(id);
    if (active && active.to.x === to.x && active.to.y === to.y && active.to.h === to.h) return;
    stopNode(id);
    exits.get(id)?.dispose();
    const dx = from.x - to.x, dy = from.y - to.y;
    if (!entering && !dx && !dy) return;
    const start = {translate: `${dx}px ${dy}px`}, end = {translate: '0px 0px'};
    if (entering) { start.opacity = 0; end.opacity = 1; }
    const animation = element.animate([start, end], {
      duration: entering ? 320 : 340, delay, easing: ease, fill: 'both'
    });
    flights.set(id, {from, to, animation});
    animation.onfinish = () => {
      if (flights.get(id)?.animation !== animation) return;
      flights.delete(id);
      animation.cancel();
    };
  }

  function enterNode(element, to, parent, order) {
    const from = {x: parent.x, y: parent.y + (parent.h - to.h) / 2};
    moveNode(element, from, to, Math.min(order * 22, 110), true);
  }

  function exitNode(element, from, parent, layer) {
    if (!from || !parent || exits.size >= 12) return;
    const id = element.dataset.id, ghost = element.cloneNode(true);
    const to = {x: parent.x, y: parent.y + (parent.h - from.h) / 2, h: from.h};
    ghost.removeAttribute('data-id');
    ghost.inert = true;
    ghost.setAttribute('aria-hidden', 'true');
    ghost.style.cssText += ';pointer-events:none;transition:none;animation:none;transform:none';
    ghost.style.left = (from.x - element.offsetWidth / 2) + 'px';
    ghost.style.top = from.y + 'px';
    layer.append(ghost);
    const animation = ghost.animate([
      {translate: '0px 0px', opacity: .85},
      {translate: `${to.x-from.x}px ${to.y-from.y}px`, opacity: 0}
    ], {duration: 200, easing: 'cubic-bezier(.35,0,.85,.5)', fill: 'both'});
    function dispose() {
      exits.delete(id);
      flight.path?.remove();
      ghost.remove();
      animation.cancel();
    }
    const flight = {from, to, animation, dispose};
    exits.set(id, flight);
    animation.onfinish = dispose;
  }

  function retireConnector(path, parentId, childId, layout, geometry) {
    const exit = exits.get(childId);
    if (!exit || (!layout.has(parentId) && !exits.has(parentId))) return false;
    exit.path = path;
    path.removeAttribute('data-child');
    path.animate([{opacity: .65}, {opacity: 0}], {duration: 200, fill: 'both'});
    function follow() {
      const parent = point(parentId, layout.get(parentId));
      if (exits.get(childId) !== exit || !parent) { path.remove(); return; }
      path.setAttribute('d', geometry(parent, point(childId, exit.to)));
      requestAnimationFrame(follow);
    }
    follow();
    return true;
  }

  function drawConnector(path) {
    path.setAttribute('pathLength', '1');
    path.animate([{strokeDasharray: '1', strokeDashoffset: '1'},
                  {strokeDasharray: '1', strokeDashoffset: '0'}],
                 {duration: 320, easing: ease});
  }

  function reset() {
    for (const flight of flights.values()) flight.animation.cancel();
    flights.clear();
    for (const exit of exits.values()) exit.dispose();
  }

  window.BIFURCA_MOTION = Object.freeze({
    point, moving: id => flights.has(id), snapshot, stopNode, moveNode, enterNode, exitNode, retireConnector, drawConnector, reset
  });
})();
