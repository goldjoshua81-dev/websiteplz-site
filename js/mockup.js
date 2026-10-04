/* Private mockup pages (MP-3): after the real expiry date, swap the page for the expired message.
   The build also deletes expired pages, so this only matters for a cached copy. No countdown. */
(function () {
  var box = document.querySelector('[data-expires]'); if (!box) return;
  var p = box.getAttribute('data-expires').split('-');
  var end = new Date(+p[0], +p[1] - 1, +p[2], 23, 59, 59);
  if (new Date() > end) {
    var t = document.getElementById('mk-expired');
    box.innerHTML = t ? t.innerHTML : '<p>This mockup link has expired.</p>';
    document.title = 'Mockup link expired | WebsitePlz';
  }
})();
