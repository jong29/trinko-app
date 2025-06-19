// Stock data for different views
const stockData = {
  custom: [
    {
      symbol: "SN",
      logo: "SN",
      logoColor: "#ff6b35",
      company: "SnarkNinja, Inc.",
      code: "113",
      price: "82.13",
      change: "-6.60%",
      volume: "1.99M",
      relVolume: "1.04",
      marketCap: "11.53B",
      pe: "26.01",
      eps: "3.16",
      epsGrowth: "+133.76%",
      divYield: "0.00%",
      sector: "Consumer durables",
      rating: "Strong buy",
    },
    {
      symbol: "EXEL",
      logo: "X",
      logoColor: "#ff4444",
      company: "Exelixis, Inc.",
      code: "EXEL",
      price: "41.59",
      change: "-0.45%",
      volume: "2.13M",
      relVolume: "0.81",
      marketCap: "11.34B",
      pe: "18.87",
      eps: "2.20",
      epsGrowth: "+240.89%",
      divYield: "0.00%",
      sector: "Health technology",
      rating: "Buy",
    },
    {
      symbol: "JLL",
      logo: "JLL",
      logoColor: "#ff9500",
      company: "Jones Lang LaSalle Incorporated",
      code: "JLL",
      price: "236.99",
      change: "-1.90%",
      volume: "706.51K",
      relVolume: "1.57",
      marketCap: "11.25B",
      pe: "21.43",
      eps: "11.06",
      epsGrowth: "+77.72%",
      divYield: "0.00%",
      sector: "Finance",
      rating: "Buy",
    },
    {
      symbol: "CHRW",
      logo: "CHRW",
      logoColor: "#007acc",
      company: "C.H. Robinson Worldwide, Inc.",
      code: "CHRW",
      price: "93.54",
      change: "-1.54%",
      volume: "981.52K",
      relVolume: "0.97",
      marketCap: "11.11B",
      pe: "22.35",
      eps: "4.19",
      epsGrowth: "+65.29%",
      divYield: "2.64%",
      sector: "Transportation",
      rating: "Buy",
    },
    {
      symbol: "SMR",
      logo: "SMR",
      logoColor: "#888",
      company: "NuScale Power Corporation",
      code: "SMR",
      price: "38.82",
      change: "-3.86%",
      volume: "9.82M",
      relVolume: "0.58",
      marketCap: "11.04B",
      pe: "—",
      eps: "-1.37",
      epsGrowth: "-62.81%",
      divYield: "0.00%",
      sector: "Producer manufacturing",
      rating: "Buy",
    },
  ],
  relStrSP500: [
    {
      symbol: "AAPL",
      logo: "AAPL",
      logoColor: "#007aff",
      company: "Apple Inc.",
      code: "AAPL",
      price: "81.76",
      beta: "0.97",
      correlation: "0.89",
      zScore200: "-1.5",
      rating200: "STRONG UNDERPERFORM",
      zScore500: "2.6",
      rating500: "SLIGHT OUTPERFORM",
      zScoreAvg: "0.55",
      ratingAvg: "NEUTRAL",
    },
    {
      symbol: "NVDA",
      logo: "NVDA",
      logoColor: "#76b900",
      company: "NVIDIA Corporation",
      code: "NVDA",
      price: "42.89",
      beta: "0.68",
      correlation: "0.7",
      zScore200: "0.8",
      rating200: "UNDERPERFORM",
      zScore500: "0.6",
      rating500: "NEUTRAL",
      zScoreAvg: "0.7",
      ratingAvg: "NEUTRAL",
    },
    {
      symbol: "ADM",
      logo: "ADM",
      logoColor: "#ff6b35",
      company: "Archer-Daniels-Midland Company",
      code: "ADM",
      price: "198.45",
      beta: "0.46",
      correlation: "0.65",
      zScore200: "2.1",
      rating200: "OUTPERFORM",
      zScore500: "1.1",
      rating500: "SLIGHT OUTPERFORM",
      zScoreAvg: "1.6",
      ratingAvg: "SLIGHT OUTPERFORM",
    },
    {
      symbol: "ALB",
      logo: "ALB",
      logoColor: "#e74c3c",
      company: "Albemarle Corporation",
      code: "ALB",
      price: "134.67",
      beta: "0.75",
      correlation: "0.54",
      zScore200: "-0.3",
      rating200: "UNDERPERFORM",
      zScore500: "0.1",
      rating500: "NEUTRAL",
      zScoreAvg: "-0.1",
      ratingAvg: "NEUTRAL",
    },
    {
      symbol: "NEE",
      logo: "NEE",
      logoColor: "#2ecc71",
      company: "NextEra Energy, Inc.",
      code: "NEE",
      price: "91.23",
      beta: "1.25",
      correlation: "0.56",
      zScore200: "1.4",
      rating200: "NEUTRAL",
      zScore500: "0.8",
      rating500: "NEUTRAL",
      zScoreAvg: "1.1",
      ratingAvg: "SLIGHT UNDERPERFORM",
    },
  ],
};

function getRatingClass(rating) {
  const lowerRating = rating.toLowerCase();
  if (lowerRating.includes("strong") && lowerRating.includes("buy"))
    return "strong-buy";
  if (lowerRating.includes("buy")) return "buy";
  if (lowerRating.includes("outperform")) return "buy";
  if (lowerRating.includes("underperform")) return "negative";
  return "neutral";
}

function renderCustomTable() {
  const tbody = document.getElementById("stockTable");
  tbody.innerHTML = "";

  stockData.custom.forEach((stock) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>
                <div class="symbol-cell">
                    <div class="company-logo" style="background-color: ${
                      stock.logoColor
                    };">${stock.logo}</div>
                    <div>
                        <div class="company-name">${stock.company}</div>
                        <div class="symbol-code">${stock.code}</div>
                    </div>
                </div>
            </td>
            <td>${
              stock.price
            } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td class="${
              stock.change.startsWith("+") ? "positive" : "negative"
            }">${stock.change}</td>
            <td>${stock.volume}</td>
            <td>${stock.relVolume}</td>
            <td>${
              stock.marketCap
            } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td>${stock.pe}</td>
            <td${stock.eps.startsWith("-") ? ' class="negative"' : ""}>${
      stock.eps
    } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td class="${
              stock.epsGrowth.startsWith("+") ? "positive" : "negative"
            }">${stock.epsGrowth}</td>
            <td>${stock.divYield}</td>
            <td><a href="#" class="sector-link">${stock.sector}</a></td>
            <td class="rating ${getRatingClass(stock.rating)}">^ ${
      stock.rating
    }</td>
            <td><button class="close-btn">×</button></td>
        `;
    tbody.appendChild(row);
  });
}

function renderRelStrSP500Table() {
  const tbody = document.getElementById("stockTable");
  tbody.innerHTML = "";

  stockData.relStrSP500.forEach((stock) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>
                <div class="symbol-cell">
                    <div class="company-logo" style="background-color: ${
                      stock.logoColor
                    };">${stock.logo}</div>
                    <div>
                        <div class="company-name">${stock.company}</div>
                        <div class="symbol-code">${stock.code}</div>
                    </div>
                </div>
            </td>
            <td>${
              stock.price
            } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td>${stock.beta}</td>
            <td>${stock.correlation}</td>
            <td class="${
              parseFloat(stock.zScore200) < 0 ? "negative" : "positive"
            }">${stock.zScore200}</td>
            <td class="rating ${getRatingClass(stock.rating200)}">${
      stock.rating200
    }</td>
            <td class="${
              parseFloat(stock.zScore500) < 0 ? "negative" : "positive"
            }">${stock.zScore500}</td>
            <td class="rating ${getRatingClass(stock.rating500)}">${
      stock.rating500
    }</td>
            <td class="${
              parseFloat(stock.zScoreAvg) < 0 ? "negative" : "positive"
            }">${stock.zScoreAvg}</td>
            <td class="rating ${getRatingClass(stock.ratingAvg)}">${
      stock.ratingAvg
    }</td>
            <td><button class="close-btn">×</button></td>
        `;
    tbody.appendChild(row);
  });
}

function switchToTab(tabName) {
  // Hide all header rows
  document.getElementById("customHeaders").style.display = "none";
  document.getElementById("relStrSP500Headers").style.display = "none";

  // Show appropriate header and render table
  if (tabName === "RelStr_S&P500") {
    document.getElementById("relStrSP500Headers").style.display = "";
    renderRelStrSP500Table();
  } else {
    document.getElementById("customHeaders").style.display = "";
    renderCustomTable();
  }
}

// Initialize with custom table
renderCustomTable();
function toggleFilters() {
  const filtersSection = document.getElementById("filtersSection");
  const toggleBtn = document.querySelector(".toggle-btn");

  if (filtersSection.classList.contains("hidden")) {
    filtersSection.classList.remove("hidden");
    toggleBtn.textContent = "▲";
  } else {
    filtersSection.classList.add("hidden");
    toggleBtn.textContent = "▼";
  }
}

document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    // Toggle active state for demo
    this.classList.toggle("active");
  });
});

document.querySelectorAll(".preset-tab").forEach((tab) => {
  tab.addEventListener("click", function () {
    document
      .querySelectorAll(".preset-tab")
      .forEach((t) => t.classList.remove("active"));
    this.classList.add("active");
  });
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", function () {
    document
      .querySelectorAll(".tab")
      .forEach((t) => t.classList.remove("active"));
    this.classList.add("active");

    // Switch table content based on tab
    switchToTab(this.textContent);
  });
});

document.querySelectorAll(".close-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    this.closest("tr").remove();
  });
});

// Re-attach event listeners after table updates
function attachEventListeners() {
  document.querySelectorAll(".close-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      this.closest("tr").remove();
    });
  });
}

// Update the render functions to attach listeners
function renderCustomTable() {
  const tbody = document.getElementById("stockTable");
  tbody.innerHTML = "";

  stockData.custom.forEach((stock) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>
                <div class="symbol-cell">
                    <div class="company-logo" style="background-color: ${
                      stock.logoColor
                    };">${stock.logo}</div>
                    <div>
                        <div class="company-name">${stock.company}</div>
                        <div class="symbol-code">${stock.code}</div>
                    </div>
                </div>
            </td>
            <td>${
              stock.price
            } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td class="${
              stock.change.startsWith("+") ? "positive" : "negative"
            }">${stock.change}</td>
            <td>${stock.volume}</td>
            <td>${stock.relVolume}</td>
            <td>${
              stock.marketCap
            } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td>${stock.pe}</td>
            <td${stock.eps.startsWith("-") ? ' class="negative"' : ""}>${
      stock.eps
    } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td class="${
              stock.epsGrowth.startsWith("+") ? "positive" : "negative"
            }">${stock.epsGrowth}</td>
            <td>${stock.divYield}</td>
            <td><a href="#" class="sector-link">${stock.sector}</a></td>
            <td class="rating ${getRatingClass(stock.rating)}">^ ${
      stock.rating
    }</td>
            <td><button class="close-btn">×</button></td>
        `;
    tbody.appendChild(row);
  });
  attachEventListeners();
}

function renderRelStrSP500Table() {
  const tbody = document.getElementById("stockTable");
  tbody.innerHTML = "";

  stockData.relStrSP500.forEach((stock) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>
                <div class="symbol-cell">
                    <div class="company-logo" style="background-color: ${
                      stock.logoColor
                    };">${stock.logo}</div>
                    <div>
                        <div class="company-name">${stock.company}</div>
                        <div class="symbol-code">${stock.code}</div>
                    </div>
                </div>
            </td>
            <td>${
              stock.price
            } <span style="color: #888; font-size: 10px;">USD</span></td>
            <td>${stock.beta}</td>
            <td>${stock.correlation}</td>
            <td class="${
              parseFloat(stock.zScore200) < 0 ? "negative" : "positive"
            }">${stock.zScore200}</td>
            <td class="rating ${getRatingClass(stock.rating200)}">${
      stock.rating200
    }</td>
            <td class="${
              parseFloat(stock.zScore500) < 0 ? "negative" : "positive"
            }">${stock.zScore500}</td>
            <td class="rating ${getRatingClass(stock.rating500)}">${
      stock.rating500
    }</td>
            <td class="${
              parseFloat(stock.zScoreAvg) < 0 ? "negative" : "positive"
            }">${stock.zScoreAvg}</td>
            <td class="rating ${getRatingClass(stock.ratingAvg)}">${
      stock.ratingAvg
    }</td>
            <td><button class="close-btn">×</button></td>
        `;
    tbody.appendChild(row);
  });
  attachEventListeners();
}

// Add sorting functionality
document.querySelectorAll("th").forEach((header) => {
  header.addEventListener("click", function () {
    // Reset other headers
    document.querySelectorAll(".sort-icon").forEach((icon) => {
      icon.textContent = "▼";
    });

    // Toggle sort direction
    const sortIcon =
      this.querySelector(".sort-icon") ||
      this.appendChild(document.createElement("span"));
    sortIcon.className = "sort-icon";
    sortIcon.textContent = sortIcon.textContent === "▼" ? "▲" : "▼";
  });
});
