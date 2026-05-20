function initCoursePage({ charts, trend }) {
  charts.forEach((c) => makeChart(c.id, c.grades, c.absent));
  if (trend.length) makeTrendChart('trendChart', trend);

  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach((p) => p.classList.add('hidden'));
      btn.classList.add('active');
      document.getElementById('panel-' + btn.dataset.tab).classList.remove('hidden');
    });
  });
}
