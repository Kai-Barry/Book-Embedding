// 2D Galaxy State & Spatial Index for 60fps Performance with 25,000+ points
let galaxyData = [];
let galaxySpatialGrid = new Map(); // Grid key "gridX_gridY" -> Array of point indices
const GRID_CELL_SIZE = 10; // spatial cell in data units (-100 to 100)

let galaxyTransform = { x: 0, y: 0, scale: 2.8 };
let isDraggingGalaxy = false;
let dragStart = { x: 0, y: 0 };
let mouseStartPos = { x: 0, y: 0 };
let hasDragged = false;
let hoveredPoint = null;
let selectedPoint = null;
let galaxyCanvas, galaxyCtx;
let focusConstellationOnly = false;
let animFrameRequested = false;

// Vector Weight Tuning State
let currentWeights = {
  plot: 1.0,
  tone: 0.7,
  style: 0.5,
  pacing: 0.4
};
let currentConceptKeywords = [];
let activeKeywords = new Set();
let currentTargetId = null;

// Modal & Navigation State
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeBookModal();
});

function toggleFocusConstellation() {
  focusConstellationOnly = !focusConstellationOnly;
  const btn = document.getElementById('btn-focus-constellation');
  if (btn) {
    btn.textContent = focusConstellationOnly ? '✨ Constellation Isolated' : '🌌 Highlighting Mode';
    btn.style.background = focusConstellationOnly ? 'rgba(6, 182, 212, 0.3)' : 'rgba(6, 182, 212, 0.15)';
  }
  requestGalaxyDraw();
}

function zoomGalaxy(factor) {
  galaxyTransform.scale = Math.max(0.2, Math.min(50.0, galaxyTransform.scale * factor));
  updateZoomIndicator();
  requestGalaxyDraw();
}

function updateZoomIndicator() {
  const el = document.getElementById('zoom-indicator');
  if (el) {
    el.textContent = `Zoom: ${galaxyTransform.scale.toFixed(1)}x`;
  }
}

function handleFilterChange() {
  if (currentTargetId) {
    handleBookSimilarSearch(currentTargetId);
  } else {
    requestGalaxyDraw();
  }
}

function onWeightSliderChange(weightKey, val) {
  currentWeights[weightKey] = parseFloat(val);
  const labelEl = document.getElementById(`val-${weightKey}`);
  if (labelEl) labelEl.textContent = `${Math.round(currentWeights[weightKey] * 100)}%`;
  
  // Highlight Apply button to indicate pending changes
  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function toggleConceptKeyword(keyword) {
  if (activeKeywords.has(keyword)) {
    activeKeywords.delete(keyword);
  } else {
    activeKeywords.add(keyword);
  }
  
  document.querySelectorAll('.concept-pill').forEach(pill => {
    if (pill.dataset.keyword === keyword) {
      pill.classList.toggle('active', activeKeywords.has(keyword));
    }
  });

  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function applyTuningSearch() {
  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.remove('pending-changes');
    btn.textContent = '✅ Weights Applied';
    setTimeout(() => {
      if (btn) btn.textContent = '🔍 Apply Weights & Re-Search';
    }, 2000);
  }
  if (currentTargetId) {
    handleBookSimilarSearch(currentTargetId, true);
  }
}

// RequestAnimationFrame Batching
function requestGalaxyDraw() {
  if (!animFrameRequested) {
    animFrameRequested = true;
    requestAnimationFrame(() => {
      drawGalaxy();
      animFrameRequested = false;
    });
  }
}

// Build Spatial Hash Grid for O(1) hover search among 25,000 points
function buildSpatialGrid() {
  galaxySpatialGrid.clear();
  for (let i = 0; i < galaxyData.length; i++) {
    const p = galaxyData[i];
    const gx = Math.floor((p.x || 0) / GRID_CELL_SIZE);
    const gy = Math.floor((p.y || 0) / GRID_CELL_SIZE);
    const key = `${gx}_${gy}`;
    if (!galaxySpatialGrid.has(key)) {
      galaxySpatialGrid.set(key, []);
    }
    galaxySpatialGrid.get(key).push(i);
  }
}

async function openBookModal(bookId) {
  const overlay = document.getElementById('book-modal-overlay');
  const content = document.getElementById('modal-content');
  if (!overlay || !content) return;

  content.innerHTML = `
    <div style="text-align: center; padding: 2rem;">
      <div class="spinner"></div>
      <p style="color: var(--text-secondary);">Loading full book details & stylistic profile...</p>
    </div>
  `;
  overlay.style.display = 'flex';

  try {
    const res = await fetch(`/api/book/${encodeURIComponent(bookId)}`);
    if (!res.ok) throw new Error('Book not found');
    const book = await res.json();

    const genresHtml = (book.genres || 'General')
      .split(',')
      .map(g => `<span class="genre-tag">${escapeHtml(g.trim())}</span>`)
      .join('');

    const style = book.style_profile || {
      pov: 'Third Person',
      pacing: 'Moderate Pacing',
      prose_density: 'Direct & Accessible',
      tone: 'Grounded & Dramatic'
    };

    content.innerHTML = `
      <div style="border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 1.2rem; margin-bottom: 1.5rem;">
        <span class="spotlight-anchor-tag">📖 Book Detail Analysis</span>
        <h2 style="font-size: 1.8rem; font-weight: 800; color: #fff; margin: 0.5rem 0 0.2rem 0;">${escapeHtml(book.title)}</h2>
        <div style="font-size: 1.05rem; color: var(--text-secondary);">
          by <strong style="color: #67e8f9;">${escapeHtml(book.author || 'Unknown')}</strong> &bull; 
          <span style="color: var(--text-muted);">${escapeHtml(book.pub_date || 'N/A')}</span>
        </div>
      </div>

      <div class="genre-tags">${genresHtml}</div>

      <!-- Stylistic Feature Grid -->
      <div class="style-badge-grid">
        <div class="style-badge-item">
          <span class="style-badge-label">🎯 Point of View</span>
          <span class="style-badge-val">${escapeHtml(style.pov)}</span>
        </div>
        <div class="style-badge-item">
          <span class="style-badge-label">⏱️ Story Pacing</span>
          <span class="style-badge-val">${escapeHtml(style.pacing)}</span>
        </div>
        <div class="style-badge-item">
          <span class="style-badge-label">🎨 Prose Density</span>
          <span class="style-badge-val">${escapeHtml(style.prose_density)}</span>
        </div>
        <div class="style-badge-item">
          <span class="style-badge-label">🌌 Atmospheric Tone</span>
          <span class="style-badge-val">${escapeHtml(style.tone)}</span>
        </div>
      </div>

      <div style="margin-bottom: 2rem;">
        <h4 style="font-size: 0.95rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Synopsis & Narrative Excerpt</h4>
        <p style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.7; background: rgba(0, 0, 0, 0.2); padding: 1.2rem; border-radius: var(--radius-md); border: 1px solid rgba(255, 255, 255, 0.05); max-height: 250px; overflow-y: auto;">
          ${escapeHtml(book.summary)}
        </p>
      </div>

      <div style="display: flex; gap: 1rem; justify-content: flex-end;">
        <button class="action-btn" style="background: rgba(99, 102, 241, 0.2); border-color: #6366f1; color: #a5b4fc;" onclick="closeBookModal(); exploreBook('${escapeHtml(book.id)}', '${escapeHtml(book.title).replace(/'/g, "\\'")}')">
          🔍 Find Similar Books
        </button>
        <button class="action-btn" onclick="closeBookModal()">
          Close
        </button>
      </div>
    `;
  } catch (err) {
    content.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: #ef4444;">
        <h3>Failed to load book details</h3>
        <p>${escapeHtml(err.message)}</p>
        <button class="action-btn" style="margin-top: 1rem;" onclick="closeBookModal()">Close</button>
      </div>
    `;
  }
}

function closeBookModal() {
  const overlay = document.getElementById('book-modal-overlay');
  if (overlay) overlay.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', async () => {
  await fetchStatus();
  await fetchGenres();
  initGalaxyCanvas();
  await loadGalaxyData();
});

async function fetchStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    
    const gpuEl = document.getElementById('gpu-info');
    if (data.gpu && data.gpu.available) {
      gpuEl.textContent = `RTX 4080 CUDA Active (${data.gpu.vram})`;
    } else {
      gpuEl.textContent = 'CPU Mode';
    }

    const statsEl = document.getElementById('index-stats');
    if (data.index.books_count > 0) {
      statsEl.textContent = `Indexed: ${data.index.books_count.toLocaleString()} books (${data.index.vector_dimension}-dim vectors)`;
    } else {
      statsEl.textContent = 'Index empty. Run ingestion script.';
    }
  } catch (err) {
    console.error('Failed to load status:', err);
  }
}

async function fetchGenres() {
  try {
    const res = await fetch('/api/genres');
    const genres = await res.json();
    const select = document.getElementById('genre-select');
    genres.forEach(g => {
      const opt = document.createElement('option');
      opt.value = g;
      opt.textContent = g;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error('Failed to load genres:', err);
  }
}

function showLoading(msg = 'Computing dense vector similarities on GPU...') {
  document.getElementById('loading').style.display = 'block';
  document.getElementById('loading-msg').textContent = msg;
  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('books-grid').innerHTML = '';
  document.getElementById('results-header').style.display = 'none';
}

function hideLoading() {
  document.getElementById('loading').style.display = 'none';
}

// Distinct 3-Stage Workflow Controller:
// Stage 1: Select Book -> loads book into Step 2 (Tuning Panel). Step 3 is hidden until user tunes or clicks search.
// Stage 2: User adjusts sliders / keywords.
// Stage 3: User clicks "Apply Weights & Search" -> reveals 2D Constellation & Recommendations.

async function handleBookSelection(bookIdOrTitle) {
  const target = bookIdOrTitle || document.getElementById('book-input').value.trim();
  if (!target) return;
  currentTargetId = target;

  showLoading(`Loading book details for "${target}"...`);

  try {
    const res = await fetch(`/api/book/${encodeURIComponent(target)}`);
    if (!res.ok) throw new Error('Book not found');
    const book = await res.json();
    hideLoading();

    // Fetch concept keywords for this target book
    const kwRes = await fetch(`/api/similar/${encodeURIComponent(target)}?top_k=1`);
    const kwData = await kwRes.json();
    currentConceptKeywords = kwData.concept_keywords || [];
    activeKeywords = new Set(currentConceptKeywords);

    // Save target book coordinates
    targetBookPoint = {
      id: book.id,
      title: book.title,
      genres: book.genres || 'General',
      x: kwData.target_book ? kwData.target_book.x : 0,
      y: kwData.target_book ? kwData.target_book.y : 0
    };

    // Show Step 2 (Selected Book & Tuning Panel)
    const step2 = document.getElementById('step-2-section');
    const step3 = document.getElementById('step-3-section');
    const emptyState = document.getElementById('empty-state');
    if (step2) step2.style.display = 'block';
    if (step3) step3.style.display = 'none'; // Step 3 stays hidden until user initiates search!
    if (emptyState) emptyState.style.display = 'none';

    renderTargetSpotlight(book, currentConceptKeywords);

    // Smoothly scroll to Step 2
    step2.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    hideLoading();
    alert('Could not load book: ' + err.message);
  }
}

function renderTargetSpotlight(targetBook, conceptKeywords = []) {
  const spotlightCard = document.getElementById('target-book-spotlight');
  if (!spotlightCard || !targetBook) return;

  const genres = (targetBook.genres || 'General')
    .split(',')
    .slice(0, 4)
    .map(g => `<span class="genre-tag" style="background:rgba(245, 158, 11, 0.15); color:#fde68a; border-color:rgba(245, 158, 11, 0.3);">${escapeHtml(g.trim())}</span>`)
    .join('');

  const kws = conceptKeywords.length > 0 ? conceptKeywords : currentConceptKeywords;
  const keywordPillsHtml = kws.map(kw => {
    const isActive = activeKeywords.has(kw);
    return `<span class="concept-pill ${isActive ? 'active' : ''}" data-keyword="${escapeHtml(kw)}" onclick="toggleConceptKeyword('${escapeHtml(kw)}')">🏷️ ${escapeHtml(kw)}</span>`;
  }).join('');

  spotlightCard.innerHTML = `
    <div class="spotlight-header">
      <div>
        <span class="spotlight-anchor-tag">⭐ Selected Target Book</span>
        <h2 style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-top: 0.4rem; cursor: pointer;" onclick="openBookModal('${escapeHtml(targetBook.id)}')">${escapeHtml(targetBook.title)}</h2>
        <div style="font-size: 1rem; color: var(--text-secondary); margin-top: 0.2rem;">
          by <strong style="color: #fff;">${escapeHtml(targetBook.author || 'Unknown')}</strong> &bull; 
          <span style="color: var(--text-muted);">${escapeHtml(targetBook.pub_date || '')}</span>
        </div>
      </div>
      <div style="display: flex; gap: 0.6rem;">
        <button class="action-btn" style="background: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); color: #fbbf24;" onclick="openBookModal('${escapeHtml(targetBook.id)}')">
          📖 View Full Details
        </button>
      </div>
    </div>
    <div class="genre-tags">${genres}</div>
    <p style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; margin: 0.5rem 0;">${escapeHtml(targetBook.summary)}</p>

    <!-- Interactive Vector Importance Tuning Sliders & Clustered Concept Pills -->
    <div class="tuning-panel">
      <div class="tuning-header">
        <div>
          <span class="tuning-title">🎛️ Tune Matching Vector Importance & Clustered Motifs</span>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">Adjust sliders and keywords below, then click to calculate Step 3</div>
        </div>
        <div style="display: flex; gap: 0.6rem;">
          <button id="btn-apply-tuning" class="action-btn apply-tuning-btn pending-changes" onclick="handleBookSimilarSearch(currentTargetId)">
            ⚡ Run Vector Search & Discover Similar ➔
          </button>
        </div>
      </div>

      <div class="sliders-grid">
        <div class="slider-group">
          <div class="slider-label-row">
            <span>📖 Plot & Premise</span>
            <span id="val-plot">${Math.round(currentWeights.plot * 100)}%</span>
          </div>
          <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.plot}" oninput="onWeightSliderChange('plot', this.value)" />
        </div>

        <div class="slider-group">
          <div class="slider-label-row">
            <span>🌌 Atmospheric Mood</span>
            <span id="val-tone">${Math.round(currentWeights.tone * 100)}%</span>
          </div>
          <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.tone}" oninput="onWeightSliderChange('tone', this.value)" />
        </div>

        <div class="slider-group">
          <div class="slider-label-row">
            <span>🎯 Writing Style & POV</span>
            <span id="val-style">${Math.round(currentWeights.style * 100)}%</span>
          </div>
          <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.style}" oninput="onWeightSliderChange('style', this.value)" />
        </div>

        <div class="slider-group">
          <div class="slider-label-row">
            <span>⏱️ Story Pacing</span>
            <span id="val-pacing">${Math.round(currentWeights.pacing * 100)}%</span>
          </div>
          <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.pacing}" oninput="onWeightSliderChange('pacing', this.value)" />
        </div>
      </div>

      <div>
        <div style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.3rem;">🎯 Clustered Concept Keywords (Toggle to filter/boost):</div>
        <div class="concept-pills-row">
          ${keywordPillsHtml}
        </div>
      </div>
    </div>
  `;
}

async function handleBookSimilarSearch(bookIdOrTitle) {
  const target = bookIdOrTitle || currentTargetId || document.getElementById('book-input').value.trim();
  if (!target) return;
  currentTargetId = target;

  const topK = parseInt(document.getElementById('topk-select').value);
  const genre = document.getElementById('genre-select').value;

  showLoading(`Searching 25,101 books for nearest weighted vectors to "${target}"...`);

  try {
    const kwParams = Array.from(activeKeywords).join(',');
    let url = `/api/similar/${encodeURIComponent(target)}?top_k=${topK}&weight_plot=${currentWeights.plot}&weight_tone=${currentWeights.tone}&weight_style=${currentWeights.style}&weight_pacing=${currentWeights.pacing}`;
    if (genre) url += `&genre=${encodeURIComponent(genre)}`;
    if (kwParams) url += `&keywords=${encodeURIComponent(kwParams)}`;
    
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error((await res.json()).detail || 'Book not found');
    }

    const data = await res.json();
    hideLoading();

    // Reveal Step 3 (Constellation and Recommendations)
    const step3 = document.getElementById('step-3-section');
    if (step3) {
      step3.style.display = 'block';
      setTimeout(() => step3.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    }

    renderResults(data.results, `Books similar to "${target}"`, data.latency_ms);
    
    // Set Target with exact 2D coordinates from API
    activeSearchResultPoints = data.results || [];
    
    if (data.target_book && data.target_book.x !== undefined && data.target_book.y !== undefined) {
      targetBookPoint = {
        id: data.target_book.id,
        title: data.target_book.title,
        genres: data.target_book.genres || 'General',
        x: data.target_book.x,
        y: data.target_book.y
      };
    }

    focusGalaxyOnTarget(targetBookPoint, activeSearchResultPoints);
  } catch (err) {
    hideLoading();
    alert('Search error: ' + err.message);
  }
}

function focusGalaxyOnTarget(target, neighbors) {
  if (!galaxyCanvas || !target) return;
  const targetScale = 3.8;
  galaxyTransform.scale = targetScale;
  galaxyTransform.x = galaxyCanvas.width / 2 - (target.x || 0) * targetScale;
  galaxyTransform.y = galaxyCanvas.height / 2 - (target.y || 0) * targetScale;
  updateZoomIndicator();
  drawGalaxy();
}

function focusGalaxyOnPoints(points) {
  if (!galaxyCanvas || points.length === 0) return;
  const avgX = points.reduce((sum, p) => sum + (p.x || 0), 0) / points.length;
  const avgY = points.reduce((sum, p) => sum + (p.y || 0), 0) / points.length;
  galaxyTransform.scale = 3.5;
  galaxyTransform.x = galaxyCanvas.width / 2 - avgX * 3.5;
  galaxyTransform.y = galaxyCanvas.height / 2 - avgY * 3.5;
  updateZoomIndicator();
  drawGalaxy();
}

// ----------------- SMART AUTOCOMPLETE WITH KEYBOARD NAVIGATION -----------------
function handleCatalogAutocomplete(val) {
  clearTimeout(debounceTimer);
  const list = document.getElementById('autocomplete-list');
  if (!val || val.trim().length < 1) {
    list.style.display = 'none';
    autocompleteItems = [];
    activeAutocompleteIndex = -1;
    return;
  }

  debounceTimer = setTimeout(async () => {
    try {
      const res = await fetch(`/api/catalog?q=${encodeURIComponent(val)}&limit=10`);
      autocompleteItems = await res.json();
      activeAutocompleteIndex = -1;
      
      list.innerHTML = '';
      if (autocompleteItems.length === 0) {
        list.style.display = 'none';
        return;
      }

      autocompleteItems.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'autocomplete-item';
        div.id = `auto-item-${index}`;
        
        const badge = item.is_dynamic ? `<span style="font-size:0.7rem; background:#3b82f6; color:#fff; padding:2px 6px; border-radius:4px; margin-left:6px;">Online Fetch</span>` : '';
        const genres = (item.genres || '').split(',').slice(0, 2).join(', ');

        div.innerHTML = `
          <div style="flex: 1;">
            <div class="autocomplete-title">${escapeHtml(item.title)} ${badge}</div>
            <div class="autocomplete-author">by ${escapeHtml(item.author)} &bull; <span style="color:#64748b;">${escapeHtml(genres)}</span></div>
          </div>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${escapeHtml(item.pub_date || '')}</span>
        `;
        div.onmousedown = () => selectAutocompleteItem(index);
        list.appendChild(div);
      });
      list.style.display = 'block';
    } catch (e) {
      console.error(e);
    }
  }, 50);
}

function handleAutocompleteKeydown(e) {
  const list = document.getElementById('autocomplete-list');
  if (list.style.display === 'none' || autocompleteItems.length === 0) return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    activeAutocompleteIndex = Math.min(activeAutocompleteIndex + 1, autocompleteItems.length - 1);
    updateAutocompleteFocus();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    activeAutocompleteIndex = Math.max(activeAutocompleteIndex - 1, 0);
    updateAutocompleteFocus();
  } else if (e.key === 'Enter' && activeAutocompleteIndex >= 0) {
    e.preventDefault();
    selectAutocompleteItem(activeAutocompleteIndex);
  } else if (e.key === 'Escape') {
    list.style.display = 'none';
  }
}

function updateAutocompleteFocus() {
  autocompleteItems.forEach((_, idx) => {
    const el = document.getElementById(`auto-item-${idx}`);
    if (el) {
      el.style.background = idx === activeAutocompleteIndex ? 'rgba(99, 102, 241, 0.35)' : '';
    }
  });
  if (activeAutocompleteIndex >= 0) {
    const activeEl = document.getElementById(`auto-item-${activeAutocompleteIndex}`);
    if (activeEl) activeEl.scrollIntoView({ block: 'nearest' });
  }
}

function selectAutocompleteItem(index) {
  if (index >= 0 && index < autocompleteItems.length) {
    const item = autocompleteItems[index];
    document.getElementById('book-input').value = item.title;
    document.getElementById('autocomplete-list').style.display = 'none';
    handleBookSelection(item.id);
  }
}

// ----------------- 2D GALAXY VISUALIZER (UMAP CANVAS) -----------------
function initGalaxyCanvas() {
  galaxyCanvas = document.getElementById('galaxy-canvas');
  if (!galaxyCanvas) return;
  galaxyCtx = galaxyCanvas.getContext('2d');

  function resize() {
    if (!galaxyCanvas || !galaxyCanvas.parentElement) return;
    const rect = galaxyCanvas.parentElement.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      galaxyCanvas.width = rect.width;
      galaxyCanvas.height = rect.height;
      requestGalaxyDraw();
    }
  }
  window.addEventListener('resize', resize);
  setTimeout(resize, 50);
  setTimeout(resize, 200);
  setTimeout(resize, 500);

  // Mouse pan & zoom with gesture disambiguation (>= 5px travel is drag, not click)
  galaxyCanvas.addEventListener('mousedown', (e) => {
    isDraggingGalaxy = true;
    hasDragged = false;
    mouseStartPos = { x: e.clientX, y: e.clientY };
    dragStart = { x: e.clientX - galaxyTransform.x, y: e.clientY - galaxyTransform.y };
    galaxyCanvas.style.cursor = 'grabbing';
  });

  window.addEventListener('mousemove', (e) => {
    if (isDraggingGalaxy) {
      const dist = Math.hypot(e.clientX - mouseStartPos.x, e.clientY - mouseStartPos.y);
      if (dist > 5) {
        hasDragged = true;
      }
      galaxyTransform.x = e.clientX - dragStart.x;
      galaxyTransform.y = e.clientY - dragStart.y;
      requestGalaxyDraw();
    } else {
      handleGalaxyHover(e);
    }
  });

  window.addEventListener('mouseup', () => {
    if (isDraggingGalaxy) {
      isDraggingGalaxy = false;
      if (galaxyCanvas) galaxyCanvas.style.cursor = 'grab';
    }
  });

  // Extended zoom up to 50x magnification
  galaxyCanvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    galaxyTransform.scale = Math.max(0.2, Math.min(50.0, galaxyTransform.scale * zoomFactor));
    updateZoomIndicator();
    requestGalaxyDraw();
  });

  // Only open book if stationary click (NOT after panning/dragging)
  galaxyCanvas.addEventListener('click', () => {
    if (!hasDragged && hoveredPoint) {
      selectedPoint = hoveredPoint;
      openBookModal(hoveredPoint.id);
    }
  });
}

async function loadGalaxyData() {
  try {
    const statusTag = document.getElementById('galaxy-status-tag');
    if (statusTag) statusTag.textContent = 'Loading 25,100+ vector stars...';

    const res = await fetch('/api/visualize?max_points=30000');
    const data = await res.json();
    galaxyData = data.points;
    
    if (statusTag) {
      statusTag.textContent = `${galaxyData.length.toLocaleString()} Vector Stars Active`;
    }

    if (galaxyCanvas) {
      const rect = galaxyCanvas.parentElement.getBoundingClientRect();
      if (rect.width > 0) {
        galaxyCanvas.width = rect.width;
        galaxyCanvas.height = rect.height;
      }
    }
    resetGalaxyView();
  } catch (e) {
    console.error('Galaxy load failed:', e);
  }
}

async function loadGalaxyData() {
  try {
    const statusTag = document.getElementById('galaxy-status-tag');
    if (statusTag) statusTag.textContent = 'Loading 25,100+ vector stars...';

    const res = await fetch('/api/visualize?max_points=30000');
    const data = await res.json();
    galaxyData = data.points;
    buildSpatialGrid();
    
    if (statusTag) {
      statusTag.textContent = `${galaxyData.length.toLocaleString()} Vector Stars Active (60fps Engine)`;
    }

    if (galaxyCanvas) {
      const rect = galaxyCanvas.parentElement.getBoundingClientRect();
      if (rect.width > 0) {
        galaxyCanvas.width = rect.width;
        galaxyCanvas.height = rect.height;
      }
    }
    resetGalaxyView();
  } catch (e) {
    console.error('Galaxy load failed:', e);
  }
}

function resetGalaxyView() {
  if (!galaxyCanvas) return;
  galaxyTransform = {
    x: galaxyCanvas.width / 2,
    y: galaxyCanvas.height / 2,
    scale: Math.min(galaxyCanvas.width, galaxyCanvas.height) / 220
  };
  updateZoomIndicator();
  requestGalaxyDraw();
}

function getGenreColor(genres) {
  const g = (genres || '').toLowerCase();
  if (g.includes('science fiction') || g.includes('speculative')) return '#06b6d4'; // Cyan
  if (g.includes('horror') || g.includes('gothic')) return '#ef4444'; // Red
  if (g.includes('fantasy') || g.includes('magic')) return '#a855f7'; // Purple
  if (g.includes('mystery') || g.includes('crime') || g.includes('detective')) return '#f59e0b'; // Amber
  if (g.includes('romance') || g.includes('love')) return '#ec4899'; // Pink
  if (g.includes('history') || g.includes('biography')) return '#10b981'; // Emerald
  return '#6366f1'; // Indigo
}

// Current search constellation state
let activeSearchResultPoints = [];
let targetBookPoint = null;
let currentLegendFilter = '';

// High-Performance Color Lookup
const GENRE_COLORS = {
  '#06b6d4': [],
  '#ef4444': [],
  '#a855f7': [],
  '#f59e0b': [],
  '#ec4899': [],
  '#10b981': [],
  '#6366f1': []
};

function drawGalaxy() {
  if (!galaxyCtx || !galaxyCanvas) return;
  const ctx = galaxyCtx;
  const w = galaxyCanvas.width || 1200;
  const h = galaxyCanvas.height || 480;

  ctx.clearRect(0, 0, w, h);

  // Background deep space gradient
  ctx.fillStyle = '#050b1a';
  ctx.fillRect(0, 0, w, h);

  // Background subtle grid lines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
  ctx.lineWidth = 1;
  const gridSize = 60 * (galaxyTransform.scale / 3);
  for (let x = (galaxyTransform.x % gridSize); x < w; x += gridSize) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
  }
  for (let y = (galaxyTransform.y % gridSize); y < h; y += gridSize) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
  }

  // 1. Draw Constellation Connection Rays
  if (targetBookPoint && activeSearchResultPoints.length > 0) {
    const originX = galaxyTransform.x + (targetBookPoint.x || 0) * galaxyTransform.scale;
    const originY = galaxyTransform.y + (targetBookPoint.y || 0) * galaxyTransform.scale;

    activeSearchResultPoints.forEach(neighbor => {
      const targetX = galaxyTransform.x + (neighbor.x || 0) * galaxyTransform.scale;
      const targetY = galaxyTransform.y + (neighbor.y || 0) * galaxyTransform.scale;

      const sim = neighbor.weighted_score || neighbor.similarity_score || 0.7;
      ctx.beginPath();
      ctx.moveTo(originX, originY);
      ctx.lineTo(targetX, targetY);
      ctx.strokeStyle = `rgba(6, 182, 212, ${Math.max(0.4, sim * 0.95)})`;
      ctx.lineWidth = Math.max(1.8, sim * 3.8);
      ctx.setLineDash([5, 4]);
      ctx.stroke();
      ctx.setLineDash([]);
    });
  }

  // 2. High-Performance Batched Star Rendering (Grouped by Color)
  const hasActiveConstellation = targetBookPoint || activeSearchResultPoints.length > 0;
  
  // Clear batch buckets
  for (let color in GENRE_COLORS) GENRE_COLORS[color].length = 0;
  const backgroundBatch = [];
  const neighborStars = [];
  let targetStarData = null;

  const targetId = targetBookPoint ? targetBookPoint.id : null;
  const targetTitleLower = targetBookPoint && targetBookPoint.title ? targetBookPoint.title.toLowerCase() : '';
  const neighborIds = new Set(activeSearchResultPoints.map(r => r.id));

  // Determine viewport bounds in data coordinates for instantaneous viewport culling
  const minDataX = (-50 - galaxyTransform.x) / galaxyTransform.scale;
  const maxDataX = (w + 50 - galaxyTransform.x) / galaxyTransform.scale;
  const minDataY = (-50 - galaxyTransform.y) / galaxyTransform.scale;
  const maxDataY = (h + 50 - galaxyTransform.y) / galaxyTransform.scale;

  const dataLen = galaxyData.length;
  for (let i = 0; i < dataLen; i++) {
    const p = galaxyData[i];
    const px = p.x || 0;
    const py = p.y || 0;

    // Viewport cull
    if (px < minDataX || px > maxDataX || py < minDataY || py > maxDataY) continue;

    if (currentLegendFilter && !p.genres.toLowerCase().includes(currentLegendFilter.toLowerCase())) {
      continue;
    }

    const screenX = galaxyTransform.x + px * galaxyTransform.scale;
    const screenY = galaxyTransform.y + py * galaxyTransform.scale;

    const isTarget = (p.id === targetId) || (targetTitleLower && p.title.toLowerCase() === targetTitleLower);
    const isNeighbor = neighborIds.has(p.id);

    if (isTarget) {
      targetStarData = { p, screenX, screenY };
      continue;
    }
    if (isNeighbor) {
      neighborStars.push({ p, screenX, screenY });
      continue;
    }

    if (focusConstellationOnly && hasActiveConstellation) {
      backgroundBatch.push(screenX, screenY);
      continue;
    }

    const color = getGenreColor(p.genres);
    if (GENRE_COLORS[color]) {
      GENRE_COLORS[color].push(screenX, screenY);
    }
  }

  // Draw Dimmed Background Stars in one single batch draw
  if (backgroundBatch.length > 0) {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.beginPath();
    for (let i = 0; i < backgroundBatch.length; i += 2) {
      ctx.rect(backgroundBatch[i], backgroundBatch[i+1], 2, 2);
    }
    ctx.fill();
  }

  // Draw Standard Stars Batch (Grouped by Color)
  const starRadius = hasActiveConstellation ? 2.5 : 3.5;
  for (let color in GENRE_COLORS) {
    const coords = GENRE_COLORS[color];
    if (coords.length === 0) continue;
    ctx.fillStyle = color;
    ctx.beginPath();
    for (let i = 0; i < coords.length; i += 2) {
      ctx.moveTo(coords[i] + starRadius, coords[i+1]);
      ctx.arc(coords[i], coords[i+1], starRadius, 0, Math.PI * 2);
    }
    ctx.fill();
  }

  // Draw Suggested Neighbor Stars (Glowing Cyan)
  neighborStars.forEach(({ p, screenX, screenY }) => {
    ctx.beginPath();
    ctx.arc(screenX, screenY, 9, 0, Math.PI * 2);
    ctx.fillStyle = '#06b6d4';
    ctx.shadowBlur = 20;
    ctx.shadowColor = '#06b6d4';
    ctx.fill();
    ctx.shadowBlur = 0;

    // Star Title Tag
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11px Inter, sans-serif';
    ctx.fillText(p.title, screenX + 13, screenY + 4);
  });

  // Draw Target Book Star (Radiant Gold)
  if (targetStarData || (targetBookPoint && targetBookPoint.x !== undefined)) {
    const screenX = targetStarData ? targetStarData.screenX : (galaxyTransform.x + targetBookPoint.x * galaxyTransform.scale);
    const screenY = targetStarData ? targetStarData.screenY : (galaxyTransform.y + targetBookPoint.y * galaxyTransform.scale);
    const title = targetStarData ? targetStarData.p.title : targetBookPoint.title;

    ctx.beginPath();
    ctx.arc(screenX, screenY, 14, 0, Math.PI * 2);
    ctx.fillStyle = '#f59e0b';
    ctx.shadowBlur = 30;
    ctx.shadowColor = '#f59e0b';
    ctx.fill();
    ctx.shadowBlur = 0;

    // Glowing Pulse Rings
    ctx.beginPath();
    ctx.arc(screenX, screenY, 22, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(245, 158, 11, 0.8)';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(screenX, screenY, 28, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(245, 158, 11, 0.25)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 14px Outfit, Inter, sans-serif';
    ctx.fillText(title, screenX + 32, screenY + 5);
  }

  // Draw Hovered Star Details if active
  if (hoveredPoint) {
    const hx = galaxyTransform.x + (hoveredPoint.x || 0) * galaxyTransform.scale;
    const hy = galaxyTransform.y + (hoveredPoint.y || 0) * galaxyTransform.scale;
    ctx.beginPath();
    ctx.arc(hx, hy, 8, 0, Math.PI * 2);
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}

// O(1) Spatial Hash Grid Mouse Hover Lookup
function handleGalaxyHover(e) {
  if (!galaxyCanvas || galaxyData.length === 0) return;
  const rect = galaxyCanvas.getBoundingClientRect();
  if (rect.width === 0 || rect.height === 0) return;

  // Exact pixel scaling between CSS bounding box and canvas internal resolution
  const scaleX = galaxyCanvas.width / rect.width;
  const scaleY = galaxyCanvas.height / rect.height;

  const mouseX = (e.clientX - rect.left) * scaleX;
  const mouseY = (e.clientY - rect.top) * scaleY;

  // Convert mouse screen coordinates to data coordinates
  const dataMouseX = (mouseX - galaxyTransform.x) / galaxyTransform.scale;
  const dataMouseY = (mouseY - galaxyTransform.y) / galaxyTransform.scale;
  const dataRadius = 18 / galaxyTransform.scale;

  const centerGx = Math.floor(dataMouseX / GRID_CELL_SIZE);
  const centerGy = Math.floor(dataMouseY / GRID_CELL_SIZE);

  let closest = null;
  let minDist = dataRadius;

  // Check 3x3 neighboring spatial grid cells
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const key = `${centerGx + dx}_${centerGy + dy}`;
      const indices = galaxySpatialGrid.get(key);
      if (!indices) continue;

      for (let i = 0; i < indices.length; i++) {
        const p = galaxyData[indices[i]];
        const dist = Math.hypot(dataMouseX - (p.x || 0), dataMouseY - (p.y || 0));
        if (dist < minDist) {
          minDist = dist;
          closest = p;
        }
      }
    }
  }

  if (hoveredPoint !== closest) {
    hoveredPoint = closest;
    requestGalaxyDraw();
  }

  const tooltip = document.getElementById('galaxy-tooltip');
  if (hoveredPoint && tooltip) {
    const cssX = e.clientX - rect.left;
    const cssY = e.clientY - rect.top;
    tooltip.style.display = 'block';
    tooltip.style.left = `${cssX + 15}px`;
    tooltip.style.top = `${cssY + 15}px`;
    tooltip.innerHTML = `
      <div style="font-weight: 700; color: #fff; font-size: 0.95rem;">${escapeHtml(hoveredPoint.title)}</div>
      <div style="color: var(--accent-cyan); font-size: 0.8rem; margin: 0.2rem 0;">by ${escapeHtml(hoveredPoint.author || 'Unknown')}</div>
      <div style="color: var(--text-muted); font-size: 0.75rem;">${escapeHtml(hoveredPoint.genres || '')}</div>
      <div style="font-size: 0.75rem; color: #a5b4fc; margin-top: 0.4rem;">Click star to view full details ➔</div>
    `;
    galaxyCanvas.style.cursor = 'pointer';
  } else if (tooltip) {
    tooltip.style.display = 'none';
    if (!isDraggingGalaxy) galaxyCanvas.style.cursor = 'grab';
  }
}

function filterByLegend(genre) {
  currentLegendFilter = genre;
  document.querySelectorAll('.legend-pill').forEach(pill => {
    if (genre === '') {
      pill.style.opacity = '1';
    } else {
      pill.style.opacity = pill.textContent.toLowerCase().includes(genre.toLowerCase()) ? '1' : '0.4';
    }
  });
  requestGalaxyDraw();
}

// ----------------- RESULTS & SPOTLIGHT RENDERER -----------------
function renderResults(books, title, latency, targetBook = null, conceptKeywords = []) {
  const container = document.getElementById('books-grid');
  const header = document.getElementById('results-header');
  const countEl = document.getElementById('results-count');
  const latencyEl = document.getElementById('latency-tag');
  const emptyState = document.getElementById('empty-state');
  const spotlightCard = document.getElementById('target-book-spotlight');

  container.innerHTML = '';

  // Render Searched Book Hero Spotlight Card + Interactive Weight Sliders
  if (targetBook) {
    spotlightCard.style.display = 'block';
    const genres = (targetBook.genres || 'General')
      .split(',')
      .slice(0, 4)
      .map(g => `<span class="genre-tag" style="background:rgba(245, 158, 11, 0.15); color:#fde68a; border-color:rgba(245, 158, 11, 0.3);">${escapeHtml(g.trim())}</span>`)
      .join('');

    const kws = conceptKeywords.length > 0 ? conceptKeywords : currentConceptKeywords;
    const keywordPillsHtml = kws.map(kw => {
      const isActive = activeKeywords.has(kw);
      return `<span class="concept-pill ${isActive ? 'active' : ''}" data-keyword="${escapeHtml(kw)}" onclick="toggleConceptKeyword('${escapeHtml(kw)}')">🏷️ ${escapeHtml(kw)}</span>`;
    }).join('');

    spotlightCard.innerHTML = `
      <div class="spotlight-header">
        <div>
          <span class="spotlight-anchor-tag">⭐ Searched Target Book</span>
          <h2 style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-top: 0.4rem; cursor: pointer;" onclick="openBookModal('${escapeHtml(targetBook.id)}')">${escapeHtml(targetBook.title)}</h2>
          <div style="font-size: 1rem; color: var(--text-secondary); margin-top: 0.2rem;">
            by <strong style="color: #fff;">${escapeHtml(targetBook.author || 'Unknown')}</strong> &bull; 
            <span style="color: var(--text-muted);">${escapeHtml(targetBook.pub_date || '')}</span>
          </div>
        </div>
        <div style="display: flex; gap: 0.6rem;">
          <button class="action-btn" style="background: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); color: #fbbf24;" onclick="openBookModal('${escapeHtml(targetBook.id)}')">
            📖 View Full Details
          </button>
          <button class="action-btn" style="background: rgba(6, 182, 212, 0.2); border: 1px solid rgba(6, 182, 212, 0.5); color: #67e8f9;" onclick="focusGalaxyOnTarget(targetBookPoint)">
            🔭 Locate in Constellation
          </button>
        </div>
      </div>
      <div class="genre-tags">${genres}</div>
      <p style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; margin: 0.5rem 0;">${escapeHtml(targetBook.summary)}</p>

      <!-- Interactive Vector Importance Tuning Sliders & Clustered Concept Pills -->
      <div class="tuning-panel">
        <div class="tuning-header">
          <div>
            <span class="tuning-title">🎛️ Tune Matching Vector Importance & Clustered Motifs</span>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">Adjust sliders and keywords, then click Apply to re-search all 25,101 books</div>
          </div>
          <div style="display: flex; gap: 0.6rem;">
            <button id="btn-apply-tuning" class="action-btn apply-tuning-btn" onclick="applyTuningSearch()">
              🔍 Apply Weights & Re-Search
            </button>
          </div>
        </div>

        <div class="sliders-grid">
          <div class="slider-group">
            <div class="slider-label-row">
              <span>📖 Plot & Premise</span>
              <span id="val-plot">${Math.round(currentWeights.plot * 100)}%</span>
            </div>
            <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.plot}" oninput="onWeightSliderChange('plot', this.value)" />
          </div>

          <div class="slider-group">
            <div class="slider-label-row">
              <span>🌌 Atmospheric Mood</span>
              <span id="val-tone">${Math.round(currentWeights.tone * 100)}%</span>
            </div>
            <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.tone}" oninput="onWeightSliderChange('tone', this.value)" />
          </div>

          <div class="slider-group">
            <div class="slider-label-row">
              <span>🎯 Writing Style & POV</span>
              <span id="val-style">${Math.round(currentWeights.style * 100)}%</span>
            </div>
            <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.style}" oninput="onWeightSliderChange('style', this.value)" />
          </div>

          <div class="slider-group">
            <div class="slider-label-row">
              <span>⏱️ Story Pacing</span>
              <span id="val-pacing">${Math.round(currentWeights.pacing * 100)}%</span>
            </div>
            <input type="range" class="custom-range" min="0" max="2" step="0.1" value="${currentWeights.pacing}" oninput="onWeightSliderChange('pacing', this.value)" />
          </div>
        </div>

        <div>
          <div style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.3rem;">🎯 Clustered Concept Keywords (Toggle to filter/boost):</div>
          <div class="concept-pills-row">
            ${keywordPillsHtml}
          </div>
        </div>
      </div>
    `;
  } else {
    spotlightCard.style.display = 'none';
  }

  // Filter books by POV and Pacing client-side if active
  const povFilter = document.getElementById('pov-select')?.value || '';
  const pacingFilter = document.getElementById('pacing-select')?.value || '';

  let filteredBooks = books || [];
  if (povFilter) {
    filteredBooks = filteredBooks.filter(b => {
      const s = (b.summary || '').toLowerCase();
      if (povFilter === 'First Person') return s.includes(' i ') || s.includes(' my ') || s.includes(' me ') || s.includes(' we ');
      if (povFilter === 'Third Person') return s.includes(' he ') || s.includes(' she ') || s.includes(' they ');
      return true;
    });
  }
  if (pacingFilter) {
    filteredBooks = filteredBooks.filter(b => {
      const g = (b.genres || '' + b.summary).toLowerCase();
      if (pacingFilter === 'Slow-Burn') return g.includes('slow') || g.includes('atmospheric') || g.includes('dread') || g.includes('character');
      if (pacingFilter === 'Fast-Paced') return g.includes('thriller') || g.includes('action') || g.includes('chase') || g.includes('fast');
      return true;
    });
  }

  if (filteredBooks.length === 0) {
    emptyState.style.display = 'block';
    emptyState.innerHTML = `<h3>No matching books found</h3><p>Try adjusting your search query or removing stylistic/genre filters.</p>`;
    header.style.display = 'none';
    return;
  }

  emptyState.style.display = 'none';
  header.style.display = 'flex';
  countEl.textContent = `${title} (${filteredBooks.length})`;
  latencyEl.textContent = `⚡ Inference & Vector Search: ${latency} ms`;

  filteredBooks.forEach(b => {
    const card = document.createElement('div');
    card.className = 'book-card';
    
    const scoreVal = b.weighted_score !== undefined ? b.weighted_score : b.similarity_score;
    const simPercent = scoreVal !== undefined ? Math.round(scoreVal * 100) : null;

    const genresHtml = (b.genres || 'General')
      .split(',')
      .slice(0, 3)
      .map(g => `<span class="genre-tag">${escapeHtml(g.trim())}</span>`)
      .join('');

    // Explainability Reasons HTML
    let reasonsHtml = '';
    if (b.similarity_reasons && b.similarity_reasons.length > 0) {
      const reasonPills = b.similarity_reasons
        .map(r => `<span class="reason-pill">💡 ${escapeHtml(r)}</span>`)
        .join('');
      reasonsHtml = `
        <div class="why-similar-box">
          <div class="why-similar-title">🔍 Similarity Rationale:</div>
          <div class="why-similar-tags">${reasonPills}</div>
        </div>
      `;
    }

    card.innerHTML = `
      <div>
        <div class="card-top">
          <div>
            <h3 class="book-title" style="cursor: pointer;" onclick="openBookModal('${escapeHtml(b.id)}')">${escapeHtml(b.title)}</h3>
            <div class="book-author">by ${escapeHtml(b.author || 'Unknown')}</div>
          </div>
          ${simPercent !== null ? `<div class="sim-score-badge">${simPercent}% Match</div>` : ''}
        </div>
        <div class="genre-tags">${genresHtml}</div>
        ${reasonsHtml}
        <p class="book-summary" title="${escapeHtml(b.summary)}" style="cursor: pointer;" onclick="openBookModal('${escapeHtml(b.id)}')">${escapeHtml(b.summary)}</p>
      </div>
      <div class="card-footer">
        <button class="action-btn" style="padding: 0.35rem 0.7rem; font-size: 0.8rem;" onclick="openBookModal('${escapeHtml(b.id)}')">
          📖 Details
        </button>
        <button class="btn-similar" onclick="exploreBook('${escapeHtml(b.id)}', '${escapeHtml(b.title).replace(/'/g, "\\'")}')">
          Find Similar ➔
        </button>
      </div>
    `;
    container.appendChild(card);
  });
}

function exploreBook(id, title) {
  document.getElementById('book-input').value = title;
  handleBookSelection(id);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
