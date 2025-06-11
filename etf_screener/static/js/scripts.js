// ETF data from Django backend
const etfDataFromBackend = JSON.parse("{{ etf_data_json|escapejs }}");

function getTrinkoChoiceRating(trinkoChoice) {
  if (trinkoChoice) {
    return "🚀🚀";
  }
  return "";
}

function formatChange(value) {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function formatPrice(value) {
  return `${value.toFixed(2)} USD`;
}

function formatAUM(value) {
  return `${value.toFixed(2)}B USD`;
}

function createTable(data) {
  const tableHTML = `
        <table class="screener-table">
            <thead>
                <tr>
                    <th class="sortable" data-sort="ticker">Ticker</th>
                    <th class="sortable" data-sort="name">Name</th>
                    <th class="sortable" data-sort="price">Price</th>
                    <th class="sortable" data-sort="change">Change % (1D)</th>
                    <th class="sortable" data-sort="high52w">High (52W)</th>
                    <th class="sortable" data-sort="aum">AUM</th>
                    <th class="sortable" data-sort="focus">Focus</th>
                    <th class="sortable" data-sort="index">Index</th>
                    <th class="perf-header">
                        Perf (%)
                        <div class="perf-dropdown" id="perfDropdown">
                            <div class="dropdown-section">
                                <div class="dropdown-label">Timeframe</div>
                                <div class="timeframe-buttons">
                                    <button class="timeframe-btn" data-timeframe="1w">1W</button>
                                    <button class="timeframe-btn" data-timeframe="1m">1M</button>
                                    <button class="timeframe-btn" data-timeframe="3m">3M</button>
                                    <button class="timeframe-btn" data-timeframe="6m">6M</button>
                                    <button class="timeframe-btn" data-timeframe="ytd">YTD</button>
                                    <button class="timeframe-btn" data-timeframe="1y">1Y</button>
                                    <button class="timeframe-btn" data-timeframe="5y">5Y</button>
                                    <button class="timeframe-btn" data-timeframe="10y">10Y</button>
                                </div>
                            </div>
                            <div class="dropdown-section">
                                <div class="dropdown-label">Sort Direction</div>
                                <div class="sort-direction-buttons">
                                    <button class="direction-btn" data-direction="asc">↑ Ascending</button>
                                    <button class="direction-btn" data-direction="desc">↓ Descending</button>
                                </div>
                            </div>
                        </div>
                    </th>
                    <th class="sortable" data-sort="recovery">
                        Recovery Upside (%)
                        <span class="help-icon" data-tooltip="recovery">?</span>
                    </th>
                    <th class="zscore-header">
                        Z-score
                        <span class="help-icon" data-tooltip="zscore">?</span>
                        <div class="zscore-dropdown" id="zscoreDropdown">
                            <div class="dropdown-section">
                                <div class="dropdown-label">Timeframe</div>
                                <div class="timeframe-buttons">
                                    <button class="timeframe-btn" data-timeframe="20d">20D</button>
                                    <button class="timeframe-btn" data-timeframe="100d">100D</button>
                                    <button class="timeframe-btn" data-timeframe="365d">365D</button>
                                </div>
                            </div>
                            <div class="dropdown-section">
                                <div class="dropdown-label">Sort Direction</div>
                                <div class="sort-direction-buttons">
                                    <button class="direction-btn" data-direction="asc">↑ Ascending</button>
                                    <button class="direction-btn" data-direction="desc">↓ Descending</button>
                                </div>
                            </div>
                        </div>
                    </th>
                    <th>
                        Trinko Choice
                        <span class="help-icon" data-tooltip="trinko">?</span>
                    </th>
                </tr>
            </thead>
            <tbody id="tableBody">
                ${data
                  .map(
                    (row) => `
                    <tr>
                        <td><span class="ticker-symbol">${
                          row.ticker
                        }</span></td>
                        <td>${row.name}</td>
                        <td class="price-value">${formatPrice(row.price)}</td>
                        <td class="${
                          row.change_1d >= 0 ? "positive" : "negative"
                        }">${formatChange(row.change_1d)}</td>
                        <td>${
                          row.high_52w ? formatPrice(row.high_52w) : "N/A"
                        }</td>
                        <td class="aum-value">${formatAUM(row.aum)}</td>
                        <td>${row.focus}</td>
                        <td>${row.index_tracked}</td>
                        <td>
                            <div class="perf-grid">
                                <div class="perf-item"><span class="perf-label">1W:</span><span class="${
                                  row.perf_1w >= 0 ? "positive" : "negative"
                                }">${row.perf_1w.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">1M:</span><span class="${
                                  row.perf_1m >= 0 ? "positive" : "negative"
                                }">${row.perf_1m.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">3M:</span><span class="${
                                  row.perf_3m >= 0 ? "positive" : "negative"
                                }">${row.perf_3m.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">6M:</span><span class="${
                                  row.perf_6m >= 0 ? "positive" : "negative"
                                }">${row.perf_6m.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">YTD:</span><span class="${
                                  row.perf_ytd >= 0 ? "positive" : "negative"
                                }">${row.perf_ytd.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">1Y:</span><span class="${
                                  row.perf_1y >= 0 ? "positive" : "negative"
                                }">${row.perf_1y.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">5Y:</span><span class="${
                                  row.perf_5y >= 0 ? "positive" : "negative"
                                }">${row.perf_5y.toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">10Y:</span><span class="${
                                  row.perf_10y >= 0 ? "positive" : "negative"
                                }">${row.perf_10y.toFixed(2)}%</span></div>
                            </div>
                        </td>
                        <td class="${
                          row.recovery_upside ? "positive" : "neutral"
                        }">${
                      row.recovery_upside
                        ? "+" + row.recovery_upside.toFixed(2) + "%"
                        : ""
                    }</td>
                        <td>
                            <div class="zscore-grid">
                                <div class="zscore-item"><span class="zscore-label">20D:</span><span class="${
                                  row.zscore_20d < -2
                                    ? "positive"
                                    : row.zscore_20d > 2
                                    ? "negative"
                                    : "neutral"
                                }">${row.zscore_20d.toFixed(2)}</span></div>
                                <div class="zscore-item"><span class="zscore-label">100D:</span><span class="${
                                  row.zscore_100d < -2
                                    ? "positive"
                                    : row.zscore_100d > 2
                                    ? "negative"
                                    : "neutral"
                                }">${row.zscore_100d.toFixed(2)}</span></div>
                                <div class="zscore-item"><span class="zscore-label">365D:</span><span class="${
                                  row.zscore_365d < -2
                                    ? "positive"
                                    : row.zscore_365d > 2
                                    ? "negative"
                                    : "neutral"
                                }">${row.zscore_365d.toFixed(2)}</span></div>
                            </div>
                        </td>
                        <td class="trinko-choice">${getTrinkoChoiceRating(
                          row.trinko_choice
                        )}</td>
                    </tr>
                `
                  )
                  .join("")}
            </tbody>
        </table>
    `;

  document.getElementById("tableContainer").innerHTML = tableHTML;
  setupSorting();
}

function setupSorting() {
  const headers = document.querySelectorAll(".sortable");
  const perfHeader = document.querySelector(".perf-header");
  const perfDropdown = document.getElementById("perfDropdown");
  const zscoreHeader = document.querySelector(".zscore-header");
  const zscoreDropdown = document.getElementById("zscoreDropdown");
  let currentSort = { column: null, direction: "asc" };
  let selectedPerfTimeframe = null;
  let selectedZscoreTimeframe = null;

  headers.forEach((header) => {
    header.addEventListener("click", () => {
      const column = header.dataset.sort;

      if (currentSort.column === column) {
        currentSort.direction =
          currentSort.direction === "asc" ? "desc" : "asc";
      } else {
        currentSort.column = column;
        currentSort.direction = "asc";
      }

      // Update header classes
      headers.forEach((h) => {
        h.classList.remove("sort-asc", "sort-desc");
      });
      header.classList.add(
        currentSort.direction === "asc" ? "sort-asc" : "sort-desc"
      );

      // Sort and re-render
      sortTable(currentSort.column, currentSort.direction);
    });
  });

  // Performance column special handling
  perfHeader.addEventListener("click", (e) => {
    e.stopPropagation();
    perfDropdown.classList.toggle("show");
    zscoreDropdown.classList.remove("show");
  });

  // Z-score column special handling
  zscoreHeader.addEventListener("click", (e) => {
    e.stopPropagation();
    zscoreDropdown.classList.toggle("show");
    perfDropdown.classList.remove("show");
  });

  // Close dropdowns when clicking outside
  document.addEventListener("click", (e) => {
    if (!perfHeader.contains(e.target)) {
      perfDropdown.classList.remove("show");
    }
    if (!zscoreHeader.contains(e.target)) {
      zscoreDropdown.classList.remove("show");
    }
  });

  // Performance timeframe buttons
  const perfTimeframeButtons = perfDropdown.querySelectorAll(".timeframe-btn");
  perfTimeframeButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      perfTimeframeButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      selectedPerfTimeframe = btn.dataset.timeframe;
    });
  });

  // Performance direction buttons
  const perfDirectionButtons = perfDropdown.querySelectorAll(".direction-btn");
  perfDirectionButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (!selectedPerfTimeframe) {
        alert("Please select a timeframe first");
        return;
      }

      perfDirectionButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const direction = btn.dataset.direction;
      sortByPerformance(selectedPerfTimeframe, direction);
      perfDropdown.classList.remove("show");

      // Update header visual
      headers.forEach((h) => h.classList.remove("sort-asc", "sort-desc"));
      perfHeader.classList.add(direction === "asc" ? "sort-asc" : "sort-desc");
    });
  });

  // Z-score timeframe buttons
  const zscoreTimeframeButtons =
    zscoreDropdown.querySelectorAll(".timeframe-btn");
  zscoreTimeframeButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      zscoreTimeframeButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      selectedZscoreTimeframe = btn.dataset.timeframe;
    });
  });

  // Z-score direction buttons
  const zscoreDirectionButtons =
    zscoreDropdown.querySelectorAll(".direction-btn");
  zscoreDirectionButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (!selectedZscoreTimeframe) {
        alert("Please select a timeframe first");
        return;
      }

      zscoreDirectionButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const direction = btn.dataset.direction;
      sortByZscore(selectedZscoreTimeframe, direction);
      zscoreDropdown.classList.remove("show");

      // Update header visual
      headers.forEach((h) => h.classList.remove("sort-asc", "sort-desc"));
      zscoreHeader.classList.add(
        direction === "asc" ? "sort-asc" : "sort-desc"
      );
    });
  });
}

function sortByPerformance(timeframe, direction) {
  processedData.sort((a, b) => {
    const aVal = a.perf[timeframe];
    const bVal = b.perf[timeframe];

    if (direction === "asc") {
      return aVal - bVal;
    } else {
      return bVal - aVal;
    }
  });

  createTable(processedData);
}

function sortByZscore(timeframe, direction) {
  processedData.sort((a, b) => {
    const aVal = a.zscore[timeframe];
    const bVal = b.zscore[timeframe];

    if (direction === "asc") {
      return aVal - bVal;
    } else {
      return bVal - aVal;
    }
  });

  createTable(processedData);
}

function sortTable(column, direction) {
  const tbody = document.getElementById("tableBody");
  const rows = Array.from(tbody.querySelectorAll("tr"));

  const sortedData = processedData.sort((a, b) => {
    let aVal = a[column];
    let bVal = b[column];

    // Handle different data types
    if (typeof aVal === "string") {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }

    if (direction === "asc") {
      return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
    } else {
      return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
    }
  });

  // Re-render sorted data
  createTable(sortedData);
}

// Process data
let processedData = [];

function loadData() {
  // Use the ETF data from Django backend
  processedData = etfDataFromBackend;
  createTable(processedData);
  setupTooltips();
  setupDropdowns();
  setupSearch();
}

// Initialize
loadData();

// Search functionality
function setupSearch() {
  const searchBox = document.getElementById("searchBox");

  searchBox.addEventListener("input", (e) => {
    const searchTerm = e.target.value.toLowerCase();
    filterTable(searchTerm);
  });
}

function filterTable(searchTerm) {
  if (!searchTerm) {
    createTable(processedData);
    return;
  }

  const filteredData = processedData.filter((row) => {
    return (
      row.ticker.toLowerCase().includes(searchTerm) ||
      row.name.toLowerCase().includes(searchTerm) ||
      row.focus.toLowerCase().includes(searchTerm) ||
      row.index_tracked.toLowerCase().includes(searchTerm)
    );
  });

  createTable(filteredData);
}

// Tooltip functionality
const tooltipData = {
  recovery: {
    title: "Recovery Upside %",
    content: [
      "What it measures: The potential gain if the ETF price returns to its 1-year high.",
      "How to read: +20% means the ETF could gain 20% if it recovers to its 52-week high.",
      "How it's calculated: (52-week High ÷ Current Price - 1) × 100",
    ],
  },
  zscore: {
    title: "Z-Score",
    content: [
      "What it measures: How far the current price is from its average, in standard deviations.",
      "How to read: -2.0 means the price is 2 standard deviations below average (oversold). +2.0 means 2 standard deviations above (overbought).",
      "How it's calculated: (Current Price - Moving Average) ÷ Standard Deviation",
    ],
  },
  trinko: {
    title: "Trinko Choice Rating",
    content: [
      "What it measures: A rating system that identifies undervalued ETFs likely to outperform. It's calculated using recovery upside and z-score to identify assets that are likely to be undervalued.",
      "How to read: More rockets = stronger buy signal.",
      "Rating logic:<br>🚀🚀🚀 = Recovery >10% AND 3+ z-scores <-2<br>🚀🚀 = Recovery >5% AND 2+ z-scores <-2<br>🚀 = Recovery >0% AND 1+ z-score <-2",
      "Why it works: ETFs with high ratings are deeply undervalued. Historical data shows they outperform regular DCA investing.",
    ],
  },
};

function setupTooltips() {
  const helpIcons = document.querySelectorAll(".help-icon");
  const tooltip = document.getElementById("tooltip");

  helpIcons.forEach((icon) => {
    icon.addEventListener("click", (e) => {
      e.stopPropagation();
      const type = icon.dataset.tooltip;
      const data = tooltipData[type];

      if (data) {
        tooltip.innerHTML = `
                    <h4>${data.title}</h4>
                    ${data.content.map((text) => `<p>${text}</p>`).join("")}
                `;

        // Position tooltip near the clicked icon
        const iconRect = icon.getBoundingClientRect();
        const tooltipWidth = 300; // max-width from CSS

        // Calculate position
        let left = iconRect.left + iconRect.width + 10;
        let top = iconRect.top - 10;

        // Adjust if tooltip would go off right edge
        if (left + tooltipWidth > window.innerWidth) {
          left = iconRect.left - tooltipWidth - 10;
        }

        // Adjust if tooltip would go off top edge
        if (top < 10) {
          top = iconRect.bottom + 10;
        }

        tooltip.style.top = `${top + window.scrollY}px`;
        tooltip.style.left = `${left + window.scrollX}px`;
        tooltip.classList.add("show");
      }
    });
  });

  // Close tooltip when clicking outside
  document.addEventListener("click", () => {
    tooltip.classList.remove("show");
  });
}

// Call setupTooltips after table is created
function createTable(data) {
  const tableHTML = `
        <table class="screener-table">
            <thead>
                <tr>
                    <th class="sortable" data-sort="ticker">Ticker</th>
                    <th class="sortable" data-sort="name">Name</th>
                    <th class="sortable" data-sort="price">Price</th>
                    <th class="sortable" data-sort="change">Change % (1D)</th>
                    <th class="sortable" data-sort="high52w">High (52W)</th>
                    <th class="sortable" data-sort="aum">AUM</th>
                    <th class="sortable" data-sort="focus">Focus</th>
                    <th class="sortable" data-sort="index">Index</th>
                    <th class="perf-header">
                        Perf (%)
                        <div class="perf-dropdown" id="perfDropdown">
                            <div class="dropdown-section">
                                <div class="dropdown-label">Timeframe</div>
                                <div class="timeframe-buttons">
                                    <button class="timeframe-btn" data-timeframe="1W">1W</button>
                                    <button class="timeframe-btn" data-timeframe="1M">1M</button>
                                    <button class="timeframe-btn" data-timeframe="3M">3M</button>
                                    <button class="timeframe-btn" data-timeframe="6M">6M</button>
                                    <button class="timeframe-btn" data-timeframe="YTD">YTD</button>
                                    <button class="timeframe-btn" data-timeframe="1Y">1Y</button>
                                    <button class="timeframe-btn" data-timeframe="5Y">5Y</button>
                                    <button class="timeframe-btn" data-timeframe="10Y">10Y</button>
                                </div>
                            </div>
                            <div class="dropdown-section">
                                <div class="dropdown-label">Sort Direction</div>
                                <div class="sort-direction-buttons">
                                    <button class="direction-btn" data-direction="asc">↑ Ascending</button>
                                    <button class="direction-btn" data-direction="desc">↓ Descending</button>
                                </div>
                            </div>
                        </div>
                    </th>
                    <th class="sortable" data-sort="recovery">
                        Recovery Upside (%)
                        <span class="help-icon" data-tooltip="recovery">?</span>
                    </th>
                    <th class="zscore-header">
                        Z-score
                        <span class="help-icon" data-tooltip="zscore">?</span>
                        <div class="zscore-dropdown" id="zscoreDropdown">
                            <div class="dropdown-section">
                                <div class="dropdown-label">Timeframe</div>
                                <div class="timeframe-buttons">
                                    <button class="timeframe-btn" data-timeframe="20D">20D</button>
                                    <button class="timeframe-btn" data-timeframe="100D">100D</button>
                                    <button class="timeframe-btn" data-timeframe="365D">365D</button>
                                </div>
                            </div>
                            <div class="dropdown-section">
                                <div class="dropdown-label">Sort Direction</div>
                                <div class="sort-direction-buttons">
                                    <button class="direction-btn" data-direction="asc">↑ Ascending</button>
                                    <button class="direction-btn" data-direction="desc">↓ Descending</button>
                                </div>
                            </div>
                        </div>
                    </th>
                    <th>
                        Trinko Choice
                        <span class="help-icon" data-tooltip="trinko">?</span>
                    </th>
                </tr>
            </thead>
            <tbody id="tableBody">
                ${data
                  .map(
                    (row) => `
                    <tr>
                        <td><span class="ticker-symbol">${
                          row.ticker
                        }</span></td>
                        <td>${row.name}</td>
                        <td class="price-value">${formatPrice(row.price)}</td>
                        <td class="${
                          row.change1D >= 0 ? "positive" : "negative"
                        }">${formatChange(row.change1D)}</td>
                        <td>${formatPrice(row.high52W)}</td>
                        <td class="aum-value">${formatAUM(row.aum)}</td>
                        <td>${row.focus}</td>
                        <td>${row.index}</td>
                        <td>
                            <div class="perf-grid">
                                <div class="perf-item"><span class="perf-label">1W:</span><span class="${
                                  row.perf["1W"] >= 0 ? "positive" : "negative"
                                }">${row.perf["1W"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">1M:</span><span class="${
                                  row.perf["1M"] >= 0 ? "positive" : "negative"
                                }">${row.perf["1M"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">3M:</span><span class="${
                                  row.perf["3M"] >= 0 ? "positive" : "negative"
                                }">${row.perf["3M"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">6M:</span><span class="${
                                  row.perf["6M"] >= 0 ? "positive" : "negative"
                                }">${row.perf["6M"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">YTD:</span><span class="${
                                  row.perf["YTD"] >= 0 ? "positive" : "negative"
                                }">${row.perf["YTD"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">1Y:</span><span class="${
                                  row.perf["1Y"] >= 0 ? "positive" : "negative"
                                }">${row.perf["1Y"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">5Y:</span><span class="${
                                  row.perf["5Y"] >= 0 ? "positive" : "negative"
                                }">${row.perf["5Y"].toFixed(2)}%</span></div>
                                <div class="perf-item"><span class="perf-label">10Y:</span><span class="${
                                  row.perf["10Y"] >= 0 ? "positive" : "negative"
                                }">${row.perf["10Y"].toFixed(2)}%</span></div>
                            </div>
                        </td>
                        <td class="${
                          row.recoveryUpside ? "positive" : "neutral"
                        }">${
                      row.recoveryUpside ? "+" + row.recoveryUpside + "%" : ""
                    }</td>
                        <td>
                            <div class="zscore-grid">
                                <div class="zscore-item"><span class="zscore-label">20D:</span><span class="${
                                  row.zscore["20D"] < -2
                                    ? "positive"
                                    : row.zscore["20D"] > 2
                                    ? "negative"
                                    : "neutral"
                                }">${row.zscore["20D"].toFixed(2)}</span></div>
                                <div class="zscore-item"><span class="zscore-label">100D:</span><span class="${
                                  row.zscore["100D"] < -2
                                    ? "positive"
                                    : row.zscore["100D"] > 2
                                    ? "negative"
                                    : "neutral"
                                }">${row.zscore["100D"].toFixed(2)}</span></div>
                                <div class="zscore-item"><span class="zscore-label">365D:</span><span class="${
                                  row.zscore["365D"] < -2
                                    ? "positive"
                                    : row.zscore["365D"] > 2
                                    ? "negative"
                                    : "neutral"
                                }">${row.zscore["365D"].toFixed(2)}</span></div>
                            </div>
                        </td>
                        <td class="trinko-choice">${row.trinkoChoice}</td>
                    </tr>
                `
                  )
                  .join("")}
            </tbody>
        </table>
    `;

  document.getElementById("tableContainer").innerHTML = tableHTML;
  setupSorting();
  setupTooltips();
  setupSearch();
}
