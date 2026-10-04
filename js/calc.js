/* Missed-call calculator (T-2). Visitor's own numbers only; nothing is saved or sent. */
(function () {
  var s = document.getElementById('calc'); if (!s) return;
  var calls = document.getElementById('calc-calls'), book = document.getElementById('calc-book'),
      job = document.getElementById('calc-job'), out = document.getElementById('calc-out');
  var price = parseFloat(s.getAttribute('data-price')), tier = s.getAttribute('data-tier'), pl = s.getAttribute('data-price-label');
  function num(el) { if (el.value.trim() === '') return null; var x = parseFloat(el.value); return isFinite(x) && x >= 0 ? x : null; }
  function fmt(x) { return '$' + Math.round(x).toLocaleString('en-US'); }
  function upd() {
    var c = num(calls), b = num(book), j = num(job);
    if (c === null || b === null || j === null || j <= 0) { out.textContent = 'Fill in all three to see the math.'; return; }
    b = Math.min(b, 10);
    var weekly = c * (b / 10) * j, monthly = weekly * 4.33, n = Math.ceil(price / j);
    out.textContent = 'That\u2019s about ' + fmt(weekly) + ' a week, or ' + fmt(monthly) + ' a month, in jobs that went somewhere else. The ' +
      tier + ' site (' + pl + ') pays for itself after about ' + n + ' booked job' + (n === 1 ? '' : 's') + '.';
  }
  [calls, book, job].forEach(function (el) { el.addEventListener('input', upd); });
})();
