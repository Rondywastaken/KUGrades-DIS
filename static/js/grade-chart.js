const thresholdPlugin = {
  id: 'threshold',
  beforeDatasetsDraw(chart) {
    const { ctx, scales: { x, y } } = chart;
    const xPos = (x.getPixelForValue(4) + x.getPixelForValue(5)) / 2;
    const shadeEnd = (x.getPixelForValue(6) + x.getPixelForValue(7)) / 2;
    ctx.save();
    ctx.fillStyle = 'rgba(184,176,168,0.10)';
    ctx.fillRect(xPos, y.top, shadeEnd - xPos, y.bottom - y.top);
    ctx.restore();
  },
  afterDatasetsDraw(chart) {
    const { ctx, scales: { x, y } } = chart;
    const xPos = (x.getPixelForValue(4) + x.getPixelForValue(5)) / 2;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(xPos, y.top);
    ctx.lineTo(xPos, y.bottom);
    ctx.strokeStyle = 'rgba(144,26,30,0.40)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 3]);
    ctx.stroke();
    ctx.font = '600 9px Outfit, sans-serif';
    ctx.textAlign = 'center';
    const failX = (x.getPixelForValue(5) + x.getPixelForValue(6)) / 2;
    const passX = x.left + (xPos - x.left) / 2;
    ctx.fillStyle = 'rgba(144,26,30,0.65)';
    ctx.fillText('PASS', passX, y.top + 11);
    ctx.fillStyle = 'rgba(130,120,112,0.75)';
    ctx.fillText('FAIL', failX, y.top + 11);
    ctx.restore();
  }
};

const GRADE_KEYS = ['12', '10', '7', '4', '02', '00', '-3', 'N/A'];
const GRADE_COLORS = [
  'rgba(144,26,30,0.96)', 'rgba(144,26,30,0.80)',
  'rgba(144,26,30,0.63)', 'rgba(144,26,30,0.46)',
  'rgba(144,26,30,0.28)', 'rgba(184,176,168,0.75)',
  'rgba(184,176,168,0.55)', 'rgba(100,116,139,0.40)',
];

function makeChart(canvasId, gradesObj, absent) {
  const el = document.getElementById(canvasId);
  if (!el) return;
  const raw = [
    ...['12', '10', '7', '4', '02', '00', '-3'].map(k => gradesObj[k] ?? 0),
    absent ?? 0,
  ];
  const total = raw.reduce((a, b) => a + b, 0);
  const pcts = raw.map(v => total ? +(v / total * 100).toFixed(1) : 0);
  new Chart(el, {
    type: 'bar',
    plugins: [thresholdPlugin],
    data: {
      labels: GRADE_KEYS,
      datasets: [{
        data: pcts,
        backgroundColor: GRADE_COLORS,
        borderRadius: 4,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => c.label === 'N/A'
              ? ` ${c.parsed.y}% unattended`
              : ` ${c.parsed.y}% of attended students`
          }
        }
      },
      scales: {
        y: {
          grid: { color: '#f1efec' },
          border: { display: false },
          ticks: { callback: v => v + '%', font: { family: 'Outfit', size: 10 }, color: '#667085' }
        },
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { family: 'Outfit', size: 12, weight: '600' }, color: '#667085' }
        }
      },
      animation: { duration: 500, easing: 'easeOutQuart' }
    }
  });
}

function makeTrendChart(canvasId, points) {
  const el = document.getElementById(canvasId);
  if (!el || !points.length) return;
  new Chart(el, {
    type: 'line',
    data: {
      labels: points.map((d) => d.label),
      datasets: [{
        data: points.map((d) => d.avg),
        borderColor: 'rgba(144,26,30,0.75)',
        backgroundColor: 'rgba(144,26,30,0.07)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(144,26,30,0.9)',
        pointRadius: 4,
        tension: 0.35,
        fill: true,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => ` Avg: ${c.parsed.y}` } },
      },
      scales: {
        y: {
          min: 0,
          max: 12,
          grid: { color: '#f1efec' },
          border: { display: false },
          ticks: { font: { family: 'Outfit', size: 10 }, color: '#667085', stepSize: 4 },
        },
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { family: 'Outfit', size: 11 }, color: '#667085' },
        },
      },
      animation: { duration: 600, easing: 'easeOutQuart' },
    },
  });
}
