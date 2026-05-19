/*
  static/js/main.js
  ─────────────────────────────────────────────────────────────────────────────
  JavaScript makes HTML pages INTERACTIVE.

  Here we do three things:
  1. Grab the slider value.
  2. Send it to Flask using the Fetch API (no page reload!).
  3. Take the response (JSON) and update the page with the charts & data.

  KEY JAVASCRIPT CONCEPTS USED:
  ───────────────────────────────
  • document.getElementById()   – select a single element by its id attribute
  • element.classList           – add / remove CSS classes dynamically
  • fetch()                     – make HTTP requests from the browser (async)
  • async / await               – handle asynchronous code without callback hell
  • JSON                        – the data format we exchange with Flask
  • Template literals (`...`)   – string interpolation with ${variable}
  ─────────────────────────────────────────────────────────────────────────────
*/


/* ── Helper: get a DOM element by id (shorter alias) ─────────────────────── */
function el(id) {
  return document.getElementById(id);
}


/* ── Main function: called when the button is clicked ────────────────────── */
async function runAnalysis() {
  const btn       = el("run-btn");
  const loader    = el("loader");
  const results   = el("results");
  const errorBox  = el("error-box");

  // --- Grab the current slider value (it's a string, so convert to Number)
  const nClusters = Number(el("cluster-slider").value);

  // --- UI state: show spinner, hide old results and errors
  btn.disabled = true;
  loader.classList.remove("hidden");
  results.classList.add("hidden");
  errorBox.classList.add("hidden");

  try {
    /*
      fetch() sends an HTTP request to Flask.
      Here we POST to /analyze with JSON body { n_clusters: 5 }.
      Flask reads it in request.json.

      await pauses here until the server responds – like a polite wait.
    */
    const response = await fetch("/analyze", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ n_clusters: nClusters }),
    });

    // Parse the JSON response body into a JavaScript object
    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || "Unknown server error");
    }

    // --- Populate chart images
    // Flask sent base64-encoded PNGs; we set them as the src of <img> tags
    el("elbow-img").src   = `data:image/png;base64,${data.elbow_img}`;
    el("scatter-img").src = `data:image/png;base64,${data.scatter_img}`;
    el("box-img").src     = `data:image/png;base64,${data.box_img}`;
    el("heat-img").src    = `data:image/png;base64,${data.heat_img}`;

    // --- Build segment summary cards
    buildSegmentCards(data.segments);

    // --- Show results, hide loader
    results.classList.remove("hidden");

    // Smooth scroll to results so the user sees them right away
    results.scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (err) {
    // Something went wrong – show the error message
    errorBox.textContent = `❌ Error: ${err.message}`;
    errorBox.classList.remove("hidden");
  } finally {
    // Always runs – re-enable button and hide spinner
    btn.disabled = false;
    loader.classList.add("hidden");
  }
}


/* ── Build one card per segment and inject into the grid ─────────────────── */
function buildSegmentCards(segments) {
  const grid = el("segment-cards");

  // Template literal: backtick strings can span lines and embed expressions
  grid.innerHTML = segments.map(seg => `
    <div class="seg-card">
      <div class="seg-card-title">Segment ${seg.id}
        <span style="font-size:0.78rem;color:var(--clr-muted);font-weight:400;">
          (${seg.count} customers)
        </span>
      </div>
      <div class="seg-stat">
        <span>Avg Age</span>      <span>${seg.age}</span>
      </div>
      <div class="seg-stat">
        <span>Avg Income</span>   <span>$${seg.income}k</span>
      </div>
      <div class="seg-stat">
        <span>Spending Score</span><span>${seg.spending}</span>
      </div>
      <div class="seg-reco">${seg.reco}</div>
    </div>
  `).join("");   // .join("") converts the array of strings into one big string
}
