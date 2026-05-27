


function el(id) {
  return document.getElementById(id);
}



async function runAnalysis() {
  const btn       = el("run-btn");
  const loader    = el("loader");
  const results   = el("results");
  const errorBox  = el("error-box");


  const nClusters = Number(el("cluster-slider").value);

 
  btn.disabled = true;
  loader.classList.remove("hidden");
  results.classList.add("hidden");
  errorBox.classList.add("hidden");

  try {

    const response = await fetch("/analyze", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ n_clusters: nClusters }),
    });

   
    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || "Unknown server error");
    }


    el("elbow-img").src   = `data:image/png;base64,${data.elbow_img}`;
    el("scatter-img").src = `data:image/png;base64,${data.scatter_img}`;
    el("box-img").src     = `data:image/png;base64,${data.box_img}`;
    el("heat-img").src    = `data:image/png;base64,${data.heat_img}`;

   
    buildSegmentCards(data.segments);

    // --- Show results, hide loader
    results.classList.remove("hidden");

   
    results.scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (err) {
    
    errorBox.textContent = `❌ Error: ${err.message}`;
    errorBox.classList.remove("hidden");
  } finally {
    
    btn.disabled = false;
    loader.classList.add("hidden");
  }
}



function buildSegmentCards(segments) {
  const grid = el("segment-cards");

  
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
  `).join("");   
}
function showGraph(name) {
  document.querySelectorAll('.graph-panel').forEach(p => p.classList.add('hidden'));
  document.querySelectorAll('.graph-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + name).classList.remove('hidden');
  event.target.classList.add('active');
}