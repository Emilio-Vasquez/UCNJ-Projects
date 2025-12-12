document.addEventListener("DOMContentLoaded", () => {
  if (typeof DATA === "undefined") {
    console.error("DATA variable is not defined.");
    return;
  }

  const createHistogram = (canvasId, histData, label, color) => {
    const ctx = document.getElementById(canvasId);
    if (!ctx || !histData) return;

    const { counts, bin_edges } = histData;
    const histLabels = bin_edges
      .slice(0, -1)
      .map((edge, i) => `${(edge / 1000).toFixed(0)}k - ${(bin_edges[i + 1] / 1000).toFixed(0)}k`);

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: histLabels,
        datasets: [{
          label: label,
          data: counts,
          backgroundColor: color,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true },
          x: { ticks: { maxRotation: 90, minRotation: 70 } },
        },
      },
    });
  };

  const createScatterPlot = (canvasId, scatterData, label, xLabel, yLabel) => {
    const ctx = document.getElementById(canvasId);
    if (!ctx || !scatterData) return;

    new Chart(ctx, {
      type: "scatter",
      data: {
        datasets: [{
          label: label,
          data: scatterData,
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { type: "linear", position: "bottom", title: { display: true, text: xLabel } },
          y: { title: { display: true, text: yLabel } },
        },
      },
    });
  };

  const housesCtx = document.getElementById("housesPerBoroughChart");
  if (housesCtx && DATA.houses_per_borough) {
    const labels = DATA.houses_per_borough.map((item) => item.borough);
    const counts = DATA.houses_per_borough.map((item) => item.count);
    new Chart(housesCtx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Number of Properties",
          data: counts,
          backgroundColor: "rgba(75, 192, 192, 0.6)",
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true } },
      },
    });
  }

  createHistogram(
    "salePriceHistChart",
    DATA.histograms?.sale_price,
    "Frequency",
    "rgba(255, 99, 132, 0.6)"
  );

  createHistogram(
    "landSqftHistChart",
    DATA.histograms?.land_square_feet,
    "Frequency",
    "rgba(153, 102, 255, 0.6)"
  );

  createHistogram(
    "grossSqftHistChart",
    DATA.histograms?.gross_square_feet,
    "Frequency",
    "rgba(255, 159, 64, 0.6)"
  );

  const scatterData1 = DATA.scatterplots?.gross_sqft_vs_sale_price?.map(p => ({ x: p.x, y: p.y }));
  createScatterPlot(
    "sqftVsPriceScatterChart",
    scatterData1,
    "Square Feet vs. Price",
    "Gross Square Feet",
    "Sale Price ($)"
  );

  const scatterData2 = DATA.scatterplots?.log_gross_sqft_vs_log_sale_price?.map(p => ({ x: p.x, y: p.y }));
  createScatterPlot(
    "logSqftVsPriceScatterChart",
    scatterData2,
    "Log(Square Feet) vs. Log(Price)",
    "Log(Square Feet)",
    "Log(Sale Price)"
  );
});