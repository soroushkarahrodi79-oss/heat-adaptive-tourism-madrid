/* HATI-Madrid — keyboard activation for map markers.
 *
 * Leaflet's `keyboard: true` makes a marker tab-focusable and is documented
 * to activate it on Enter, but with dash-leaflet's DivMarker the keypress
 * never reaches Leaflet's marker click path (verified: keydown / keypress /
 * keyup all arrive on the icon element, no click is produced). Asset
 * selection is the gateway to every other view, so leaving it pointer-only
 * would make most of the interface unreachable without a mouse.
 *
 * This dispatches the pointer sequence a real activation produces. The
 * mousedown matters: Leaflet suppresses a click that arrives without one
 * after a map drag (Map._draggableMoved stays true until the next press), so
 * a bare click() would work only until the user first pans the map.
 *
 * The command bar's asset picker remains the primary, conventional keyboard
 * path; this makes the markers themselves behave the way their tabindex and
 * role promise.
 */
(function () {
  "use strict";

  function activate(el) {
    var r = el.getBoundingClientRect();
    var x = r.left + r.width / 2;
    var y = r.top + r.height / 2;
    ["mousedown", "mouseup", "click"].forEach(function (type) {
      el.dispatchEvent(new MouseEvent(type, {
        bubbles: true, cancelable: true, view: window,
        clientX: x, clientY: y, button: 0, buttons: type === "mousedown" ? 1 : 0
      }));
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " " && e.key !== "Spacebar") { return; }
    var el = document.activeElement;
    if (!el || !el.classList || !el.classList.contains("leaflet-marker-icon")) {
      return;
    }
    e.preventDefault();   // Space must not scroll the page
    activate(el);
  }, true);
})();
