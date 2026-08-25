// ----------------- VECTOR SVG ICONS REPOSITORY -----------------
const ICONS = {
  'book-open': `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>`,
  'sparkles': `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>`,
  'star': `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
  'flame': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>`,
  'library': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/></svg>`,
  'target': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
  'clock': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  'feather': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/></svg>`,
  'orbit': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M20.188 10.934c.988 2.113-.082 4.417-2.39 5.145-2.308.729-4.992-.416-5.98-2.529-.988-2.113.082-4.417 2.39-5.145 2.308-.729 4.992.416 5.98 2.529z"/></svg>`,
  'users': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  'theater': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 10s3-3 3-8"/><path d="M22 10s-3-3-3-8"/><path d="M10 2c0 4.418-3.582 8-8 8v11a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1V10c-4.418 0-8-3.582-8-8z"/></svg>`,
  'swords': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5"/><line x1="13" y1="19" x2="19" y2="13"/><line x1="16" y1="16" x2="20" y2="20"/><line x1="19" y1="21" x2="21" y2="19"/></svg>`,
  'brain': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04z"/></svg>`,
  'globe': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
  'bar-chart': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
  'zap': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  'sliders': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>`,
  'crosshair': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>`,
  'compass': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>`,
  'arrow-right': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>`,
  'rotate-ccw': `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>`,
  'plus': `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
  'lightbulb': `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5"/></svg>`
};

function renderIcon(name, extraClass = '') {
  return ICONS[name] ? `<span class="svg-icon-wrap ${extraClass}">${ICONS[name]}</span>` : '';
}

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

// Vector Weight Tuning State (1 to 7 Priority Scale for Global Feature Dimensions)
const PRIORITY_LEVELS = {
  1: { label: 'Ignore / Off', mult: 0.0, badgeClass: 'priority-ignore' },
  2: { label: 'Trace', mult: 0.35, badgeClass: 'priority-trace' },
  3: { label: 'Low', mult: 0.7, badgeClass: 'priority-low' },
  4: { label: 'Balanced', mult: 1.0, badgeClass: 'priority-balanced' },
  5: { label: 'High', mult: 1.4, badgeClass: 'priority-high' },
  6: { label: 'Very High', mult: 1.8, badgeClass: 'priority-vhigh' },
  7: { label: 'Dominant', mult: 2.2, badgeClass: 'priority-dominant' }
};

// Per-Motif Individual Multi-Level Priorities (with crisp SVG status dots)
const MOTIF_LEVELS = {
  'neutral': { label: 'Neutral', mult: 0.0, icon: '<span class="status-indicator-dot dot-neutral"></span>', class: 'state-neutral', tag: '' },
  'boost-2': { label: 'Balanced (+1.0x)', mult: 1.0, icon: '<span class="status-indicator-dot dot-boost-2"></span>', class: 'state-boost-2', tag: '+1.0x' },
  'boost-3': { label: 'High (+1.6x)', mult: 1.6, icon: '<span class="status-indicator-dot dot-boost-3"></span>', class: 'state-boost-3', tag: '+1.6x' },
  'boost-4': { label: 'Dominant (+2.2x)', mult: 2.2, icon: '<span class="status-indicator-dot dot-boost-4"></span>', class: 'state-boost-4', tag: '+2.2x' },
  'exclude': { label: 'Exclude (-)', mult: -1.5, icon: '<span class="status-indicator-dot dot-exclude"></span>', class: 'state-exclude', tag: 'Exclude' }
};

let currentWeights = {
  plot: 4,        // Balanced (1.0x)
  tone: 3,        // Low (0.7x)
  style: 3,       // Low (0.7x)
  pacing: 3,      // Low (0.7x)
  community: 4    // Balanced (1.0x) - Reader Co-Taste & Collaborative Affinity
};
let currentSubclusteredMotifs = {};
let motifStates = new Map(); // keyword -> 'neutral' | 'boost-2' | 'boost-3' | 'boost-4' | 'exclude'
let customMotifs = new Set();
let selectedCustomMotifLevel = 'boost-2';
let currentTargetBook = null;
let currentTargetId = null;

// Autocomplete State
let debounceTimer = null;
let autocompleteItems = [];
let activeAutocompleteIndex = -1;

// Modal & Navigation State
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeBookModal();
});

// Dismiss autocomplete dropdown when clicking outside
document.addEventListener('click', (e) => {
  const list = document.getElementById('autocomplete-list');
  const input = document.getElementById('book-input');
  if (list && input && !list.contains(e.target) && e.target !== input) {
    list.style.display = 'none';
  }
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

const COMMUNITY_PRIORITY_LABELS = {
  1: 'Ignore Overlap (0x)',
  2: 'Trace Overlap (0.35x)',
  3: 'Low Co-Reading (0.7x)',
  4: 'Balanced Taste (1.0x)',
  5: 'Strong Overlap (1.4x)',
  6: 'High Affinity (1.8x)',
  7: 'Dominant Community (2.2x)'
};

function onWeightSliderChange(weightKey, val) {
  const level = parseInt(val, 10);
  currentWeights[weightKey] = level;
  const info = PRIORITY_LEVELS[level] || PRIORITY_LEVELS[4];
  
  // Update badge
  const badgeEl = document.getElementById(`badge-${weightKey}`);
  if (badgeEl) {
    if (weightKey === 'community') {
      badgeEl.textContent = `${level}: ${COMMUNITY_PRIORITY_LABELS[level] || info.label}`;
    } else {
      badgeEl.textContent = `${level}: ${info.label} (${info.mult}x)`;
    }
    badgeEl.className = `priority-badge ${info.badgeClass}`;
  }

  // Update discrete indentation ticks
  const ticksContainer = document.getElementById(`ticks-${weightKey}`);
  if (ticksContainer) {
    const tickMarks = ticksContainer.querySelectorAll('.tick-mark');
    tickMarks.forEach((tm, idx) => {
      if (idx + 1 <= level) {
        tm.classList.add('active-tick');
      } else {
        tm.classList.remove('active-tick');
      }
    });
  }

  // Update discrete tick labels
  const labelsContainer = document.getElementById(`labels-${weightKey}`);
  if (labelsContainer) {
    const labels = labelsContainer.querySelectorAll('span');
    labels.forEach((lbl, idx) => {
      if (idx + 1 === level) {
        lbl.classList.add('active-label');
      } else {
        lbl.classList.remove('active-label');
      }
    });
  }
  
  // Highlight Apply button to indicate pending changes
  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

// ----------------- VECTOR TUNING STUDIO STATE & PRESETS -----------------
let currentStudioTab = 'weights'; // 'weights' | 'motifs'
let currentMotifCategoryFilter = 'all';
let selectedInlineTropeLevel = 'boost-2';

const TUNING_PRESETS = [
  { id: 'balanced', icon: 'crosshair', label: 'Balanced Manifold', weights: { plot: 4, tone: 4, style: 4, pacing: 4, community: 4 }, desc: 'Equal consideration of plot, tone, style, and community' },
  { id: 'plot_focus', icon: 'book-open', label: 'Narrative & Plot Depth', weights: { plot: 7, tone: 5, style: 4, pacing: 4, community: 1 }, desc: 'Prioritizes story premise and thematic depth' },
  { id: 'audience_focus', icon: 'users', label: 'Reader Co-Taste Cluster', weights: { plot: 4, tone: 3, style: 3, pacing: 3, community: 7 }, desc: 'Emphasizes reader community overlap' },
  { id: 'style_twin', icon: 'feather', label: 'Prose & Pacing Twin', weights: { plot: 3, tone: 4, style: 7, pacing: 7, community: 3 }, desc: 'Matches POV, pacing, and prose craft' },
  { id: 'mood_dread', icon: 'orbit', label: 'Atmospheric Tone & Aura', weights: { plot: 4, tone: 7, style: 4, pacing: 6, community: 2 }, desc: 'Focuses on atmosphere, tone, and tension' }
];

function setStudioTab(tabName) {
  currentStudioTab = tabName;
  const tabWeightsBtn = document.getElementById('tab-btn-weights');
  const tabMotifsBtn = document.getElementById('tab-btn-motifs');
  const panelWeights = document.getElementById('studio-panel-weights');
  const panelMotifs = document.getElementById('studio-panel-motifs');

  if (tabName === 'weights') {
    if (tabWeightsBtn) tabWeightsBtn.classList.add('active');
    if (tabMotifsBtn) tabMotifsBtn.classList.remove('active');
    if (panelWeights) panelWeights.style.display = 'block';
    if (panelMotifs) panelMotifs.style.display = 'none';
  } else {
    if (tabWeightsBtn) tabWeightsBtn.classList.remove('active');
    if (tabMotifsBtn) tabMotifsBtn.classList.add('active');
    if (panelWeights) panelWeights.style.display = 'none';
    if (panelMotifs) panelMotifs.style.display = 'block';
  }
}

function applyTuningPreset(presetId) {
  const preset = TUNING_PRESETS.find(p => p.id === presetId);
  if (!preset) return;
  
  Object.keys(preset.weights).forEach(k => {
    currentWeights[k] = preset.weights[k];
    const slider = document.getElementById(`slider-input-${k}`);
    if (slider) slider.value = preset.weights[k];
    onWeightSliderChange(k, preset.weights[k]);
  });

  updateStudioSummary();

  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function updateStudioSummary() {
  const activeMotifCount = Array.from(motifStates.values()).filter(s => s !== 'neutral').length;
  const summaryEl = document.getElementById('studio-summary-text');
  const countBadge = document.getElementById('motifs-tab-count');
  if (countBadge) {
    countBadge.textContent = activeMotifCount > 0 ? `${activeMotifCount} active` : '0';
  }
  if (summaryEl) {
    summaryEl.textContent = `Active Vector Config: 5 Dimensions Set • ${activeMotifCount} Thematic Filters Active`;
  }
  renderActiveMotifsTray();
}

function renderActiveMotifsTray() {
  const trayContainer = document.getElementById('active-motifs-chips');
  const emptyLabel = document.getElementById('active-motifs-empty');
  if (!trayContainer) return;

  const activeEntries = Array.from(motifStates.entries()).filter(([_, s]) => s !== 'neutral');
  if (activeEntries.length === 0) {
    trayContainer.innerHTML = '';
    if (emptyLabel) emptyLabel.style.display = 'inline';
    return;
  }

  if (emptyLabel) emptyLabel.style.display = 'none';
  trayContainer.innerHTML = activeEntries.map(([kw, state]) => {
    const info = MOTIF_LEVELS[state] || MOTIF_LEVELS['neutral'];
    return `
      <span class="active-motif-tag ${info.class}" onclick="removeActiveMotif('${escapeHtml(kw)}')">
        <span>${info.icon} ${escapeHtml(kw)} (${info.tag || 'Active'})</span>
        <span class="active-motif-remove" title="Remove filter">✕</span>
      </span>
    `;
  }).join('') + `
    <button class="action-btn" style="padding: 0.15rem 0.5rem; font-size: 0.7rem; background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.15); color: #94a3b8; border-radius: 999px;" onclick="clearAllActiveMotifs()">
      Clear All (${activeEntries.length})
    </button>
  `;
}

function removeActiveMotif(keyword) {
  motifStates.delete(keyword);
  updateMotifPillUI(keyword, 'neutral');
  updateStudioSummary();

  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function clearAllActiveMotifs() {
  const allKeywords = Array.from(motifStates.keys());
  motifStates.clear();
  allKeywords.forEach(kw => updateMotifPillUI(kw, 'neutral'));
  updateStudioSummary();

  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function filterMotifsByCategory(catKey) {
  currentMotifCategoryFilter = catKey;
  document.querySelectorAll('.category-tab-chip').forEach(c => {
    c.classList.toggle('active', c.getAttribute('data-cat') === catKey);
  });

  document.querySelectorAll('.subcluster-category-card').forEach(card => {
    if (catKey === 'all') {
      card.style.display = 'flex';
    } else {
      card.style.display = card.getAttribute('data-cat') === catKey ? 'flex' : 'none';
    }
  });
}

function selectInlineTropeLevel(level, el) {
  selectedInlineTropeLevel = level;
  const parent = el.closest('.priority-choice-pills');
  if (parent) {
    parent.querySelectorAll('.choice-pill').forEach(p => p.classList.remove('active'));
    el.classList.add('active');
  }
}

function submitInlineCustomTrope() {
  const input = document.getElementById('inline-trope-input');
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;

  customMotifs.add(val);
  motifStates.set(val, selectedInlineTropeLevel);
  input.value = '';

  renderCustomMotifsCategoryCard();
  updateStudioSummary();

  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function renderCustomMotifsCategoryCard() {
  const customCard = document.getElementById('custom-motifs-subcluster-card');
  if (!customCard) return;
  if (customMotifs.size === 0) {
    customCard.style.display = 'none';
    return;
  }

  const pillsHtml = Array.from(customMotifs).map(kw => {
    const state = motifStates.get(kw) || 'neutral';
    const info = MOTIF_LEVELS[state] || MOTIF_LEVELS['neutral'];
    return `
      <span class="concept-pill ${info.class}" data-keyword="${escapeHtml(kw)}" onclick="cycleMotifState('${escapeHtml(kw)}')">
        <span>${info.icon}</span>
        <span>✨ ${escapeHtml(kw)}</span>
        ${info.tag ? `<span class="pill-badge-tag">${info.tag}</span>` : ''}
      </span>
    `;
  }).join('');

  customCard.style.display = 'flex';
  const row = customCard.querySelector('.concept-pills-row');
  if (row) row.innerHTML = pillsHtml;
}

function cycleMotifState(keyword) {
  const current = motifStates.get(keyword) || 'neutral';
  let next = 'boost-2'; // default jump: +1.0x Balanced
  if (current === 'boost-2') next = 'boost-3'; // +1.6x High
  else if (current === 'boost-3') next = 'boost-4'; // +2.2x Dominant
  else if (current === 'boost-4') next = 'exclude'; // Exclude
  else if (current === 'exclude') next = 'neutral';
  else next = 'boost-2';

  if (next === 'neutral') {
    motifStates.delete(keyword);
  } else {
    motifStates.set(keyword, next);
  }

  updateMotifPillUI(keyword, next);
  updateStudioSummary();

  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

function updateMotifPillUI(keyword, state) {
  const escapedKw = (window.CSS && CSS.escape) ? CSS.escape(keyword) : keyword.replace(/"/g, '\\"');
  const pills = document.querySelectorAll(`.concept-pill[data-keyword="${escapedKw}"]`);
  const info = MOTIF_LEVELS[state] || MOTIF_LEVELS['neutral'];

  pills.forEach(pill => {
    pill.className = `concept-pill ${info.class}`;
    pill.innerHTML = `
      <span>${info.icon}</span>
      <span>${escapeHtml(keyword)}</span>
      ${info.tag ? `<span class="pill-badge-tag">${info.tag}</span>` : ''}
    `;
  });
}

function resetTuningDefaults() {
  currentWeights = {
    plot: 4,
    tone: 3,
    style: 3,
    pacing: 3,
    community: 4
  };
  motifStates.clear();
  customMotifs.clear();
  
  if (currentTargetBook) {
    renderTargetSpotlight(currentTargetBook, currentSubclusteredMotifs);
  }
  
  const btn = document.getElementById('btn-apply-tuning');
  if (btn) {
    btn.classList.add('pending-changes');
    btn.textContent = '⚡ Apply Weights & Re-Search Vectors';
  }
}

async function bolsterBookLive(bookId) {
  try {
    showLoading(`Querying OpenLibrary & Google Books live for "${bookId}"...`);
    const res = await fetch(`/api/bolster/${encodeURIComponent(bookId)}`, { method: 'POST' });
    if (!res.ok) throw new Error('Could not bolster book from web sources.');
    const data = await res.json();
    hideLoading();
    if (data.book) {
      if (currentTargetId === bookId) {
        currentTargetBook = data.book;
        currentSubclusteredMotifs = data.book.subclustered_motifs || {};
        renderTargetSpotlight(currentTargetBook, currentSubclusteredMotifs);
      }
      openBookModal(bookId);
    }
  } catch (err) {
    hideLoading();
    alert('Web Bolster: ' + err.message);
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
      <p style="color: var(--text-secondary);">Decomposing narrative vectors & stylistic profile...</p>
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
      prose_style: 'Grounded & Narrative',
      prose_description: 'Clear, character-focused storytelling',
      tone: 'Grounded & Dramatic'
    };

    const pop = book.popularity || {
      tier: 'Popular Favorite',
      icon: 'library',
      label: 'Popular Favorite',
      description: 'Community Favorite',
      ratings_count: book.ratings_count || 5000,
      score: 72,
      rating: book.community_rating || 4.15
    };

    let subclustersHtml = '';
    if (book.subclustered_motifs) {
      const catEntries = Object.entries(book.subclustered_motifs).filter(([_, tags]) => tags && tags.length > 0);
      if (catEntries.length > 0) {
        const catHtml = catEntries.map(([cat, tags]) => {
          const tagsHtml = tags.map(t => `<span class="concept-pill state-neutral" style="cursor: default; font-size: 0.76rem;">${renderIcon('tag')} ${escapeHtml(t)}</span>`).join('');
          return `
            <div style="margin-bottom: 0.65rem;">
              <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.25rem;">${escapeHtml(cat)}</div>
              <div class="concept-pills-row">${tagsHtml}</div>
            </div>
          `;
        }).join('');

        subclustersHtml = `
          <div style="margin-bottom: 1.5rem; background: rgba(0, 0, 0, 0.25); padding: 1.1rem 1.3rem; border-radius: var(--radius-md); border: 1px solid rgba(255, 255, 255, 0.07);">
            <h4 style="font-size: 0.82rem; color: #e5a93c; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; display: flex; align-items: center; gap: 0.4rem;">${renderIcon('sparkles')} Thematic & Stylistic Sub-Clusters</h4>
            ${catHtml}
          </div>
        `;
      }
    }

    // Pacing thumb position percentage (Slow-Burn = 20%, Moderate = 50%, Fast-Paced = 80%)
    const pacingThumbPct = (style.pacing || '').includes('Slow') ? 20 : ((style.pacing || '').includes('Fast') ? 80 : 50);

    // Vector comparison graph if comparing a candidate against current target book
    let comparisonGraphHtml = '';
    const cand = activeSearchResultPoints.find(c => String(c.id) === String(book.id));
    if (currentTargetBook && cand && String(currentTargetBook.id) !== String(book.id)) {
      const bd = cand.match_breakdown || {
        plot_pct: Math.round((cand.similarity_score || 0.75) * 100),
        theme_pct: 75,
        style_pct: 80,
        audience_pct: Math.round((cand.collaborative_affinity || 0.65) * 100),
        composite_pct: Math.round((cand.weighted_score || 0.80) * 100)
      };

      comparisonGraphHtml = `
        <div class="modal-visual-breakdown">
          <div class="visual-graph-title">
            <span style="display: flex; align-items: center; gap: 0.4rem;">${renderIcon('bar-chart')} Vector Alignment vs. "${escapeHtml(currentTargetBook.title)}"</span>
            <span style="margin-left: auto; color: #e5a93c; font-weight: 800; font-family: monospace;">${bd.composite_pct}% Proximity</span>
          </div>

          <div class="modal-graph-row">
            <div class="modal-graph-label">${renderIcon('book-open')} Plot & Premise</div>
            <div class="modal-graph-track">
              <div class="modal-graph-fill fill-plot" style="width: ${bd.plot_pct}%;"></div>
            </div>
            <div class="modal-graph-val">${bd.plot_pct}%</div>
          </div>

          <div class="modal-graph-row">
            <div class="modal-graph-label">${renderIcon('sparkles')} Thematic Motifs</div>
            <div class="modal-graph-track">
              <div class="modal-graph-fill fill-theme" style="width: ${bd.theme_pct}%;"></div>
            </div>
            <div class="modal-graph-val">${bd.theme_pct}%</div>
          </div>

          <div class="modal-graph-row">
            <div class="modal-graph-label">${renderIcon('target')} Style & Voice</div>
            <div class="modal-graph-track">
              <div class="modal-graph-fill fill-style" style="width: ${bd.style_pct}%;"></div>
            </div>
            <div class="modal-graph-val">${bd.style_pct}%</div>
          </div>

          <div class="modal-graph-row">
            <div class="modal-graph-label">${renderIcon('users')} Audience Co-Taste</div>
            <div class="modal-graph-track">
              <div class="modal-graph-fill fill-audience" style="width: ${bd.audience_pct}%;"></div>
            </div>
            <div class="modal-graph-val">${bd.audience_pct}%</div>
          </div>
        </div>
      `;
    }

    content.innerHTML = `
      <div style="border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 1.2rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
          <span class="spotlight-anchor-tag">${renderIcon('book-open')} Literary Analysis & Decomposition</span>
          ${book.series_info ? `<span class="series-badge">${renderIcon('library')} ${escapeHtml(book.series_info.full_tag)}</span>` : ''}
        </div>
        <h2 style="font-size: 1.8rem; font-weight: 800; font-family: 'Playfair Display', serif; color: #fff; margin: 0.5rem 0 0.2rem 0;">${escapeHtml(book.title)}</h2>
        <div style="font-size: 1.05rem; color: var(--text-secondary);">
          by <strong style="color: #e5a93c;">${escapeHtml(book.author || 'Unknown')}</strong> &bull; 
          <span style="color: var(--text-muted);">${escapeHtml(book.pub_date || 'N/A')}</span>
        </div>

        <div class="book-metadata-row" style="margin-top: 0.8rem;">
          <span class="rating-badge">${renderIcon('star', 'gold-star')} ${pop.rating}★ <span style="opacity: 0.85; font-size: 0.68rem;">(${Number(pop.ratings_count).toLocaleString()} reviews)</span></span>
          <span class="popularity-badge">${renderIcon('flame', 'flame-icon')} ${pop.label}</span>
          ${book.readability ? `<span class="readability-badge" title="Flesch Reading Ease score: ${book.readability.score}">${renderIcon('book-open')} ${escapeHtml(book.readability.label)}</span>` : ''}
        </div>
        <div style="font-size: 0.76rem; color: #94a3b8; margin-top: 0.3rem;">${escapeHtml(pop.description)}</div>
      </div>

      ${comparisonGraphHtml}

      <div class="genre-tags" style="margin-bottom: 1.2rem;">${genresHtml}</div>

      <!-- Narrative Mechanics & Stylistic Profile Matrix -->
      <div class="style-badge-grid">
        <div class="style-badge-item">
          <span class="style-badge-label">${renderIcon('target')} Point of View</span>
          <span class="style-badge-val">${escapeHtml(style.pov)}</span>
        </div>

        <div class="style-badge-item">
          <span class="style-badge-label">${renderIcon('clock')} Story Pacing</span>
          <span class="style-badge-val">${escapeHtml(style.pacing)}</span>
          <div class="pacing-meter-track" title="Pacing Gauge: ${style.pacing}">
            <div class="pacing-meter-thumb" style="left: ${pacingThumbPct}%;"></div>
          </div>
        </div>

        <div class="style-badge-item">
          <span class="style-badge-label">${renderIcon('feather')} Prose & Writing Craft</span>
          <span class="style-badge-val">${escapeHtml(style.prose_style || style.prose_density || 'Grounded & Narrative')}</span>
          <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 0.2rem; line-height: 1.3;">
            ${escapeHtml(style.prose_description || 'Clear, immersive storytelling')}
          </div>
        </div>

        <div class="style-badge-item">
          <span class="style-badge-label">${renderIcon('orbit')} Atmospheric Tone</span>
          <span class="style-badge-val">${escapeHtml(style.tone)}</span>
        </div>
      </div>

      ${subclustersHtml}

      <div style="margin-bottom: 2rem;">
        <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Synopsis & Narrative Excerpt</h4>
        <p style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.7; background: rgba(0, 0, 0, 0.25); padding: 1.2rem; border-radius: var(--radius-md); border: 1px solid rgba(255, 255, 255, 0.05); max-height: 250px; overflow-y: auto;">
          ${escapeHtml(book.summary)}
        </p>
      </div>

      <div style="display: flex; gap: 1rem; justify-content: flex-end; flex-wrap: wrap;">
        <button class="action-btn bolster-btn" onclick="bolsterBookLive('${escapeHtml(book.id)}')">
          ${renderIcon('globe')} Bolster via Live Web Data
        </button>
        <button class="action-btn btn-search-primary" onclick="closeBookModal(); exploreBook('${escapeHtml(book.id)}', '${escapeHtml(book.title).replace(/'/g, "\\'")}')">
          ${renderIcon('compass')} Find Similar Literature
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
    if (select) {
      genres.forEach(g => {
        const opt = document.createElement('option');
        opt.value = g;
        opt.textContent = g;
        select.appendChild(opt);
      });
    }
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

  showLoading(`Loading book details and extracting sub-clusters for "${target}"...`);

  try {
    const res = await fetch(`/api/book/${encodeURIComponent(target)}`);
    if (!res.ok) throw new Error('Book not found');
    const book = await res.json();
    currentTargetBook = book;
    hideLoading();

    // Fetch subclustered motifs & target coordinates
    const kwRes = await fetch(`/api/similar/${encodeURIComponent(target)}?top_k=1`);
    const kwData = await kwRes.json();
    currentSubclusteredMotifs = kwData.subclustered_motifs || book.subclustered_motifs || {};
    
    // Reset active motif states for newly selected book
    motifStates.clear();
    customMotifs.clear();

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

    renderTargetSpotlight(book, currentSubclusteredMotifs);

    // Smoothly scroll to Step 2
    step2.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    hideLoading();
    alert('Could not load book: ' + err.message);
  }
}

function renderTargetSpotlight(targetBook, subclusteredMotifs = {}) {
  const spotlightCard = document.getElementById('target-book-spotlight');
  if (!spotlightCard || !targetBook) return;

  const genres = (targetBook.genres || 'General')
    .split(',')
    .slice(0, 4)
    .map(g => `<span class="genre-tag" style="background:rgba(245, 158, 11, 0.15); color:#fde68a; border-color:rgba(245, 158, 11, 0.3);">${escapeHtml(g.trim())}</span>`)
    .join('');

  // 5 Dimension Cards definitions with rich explanatory subtitles
  const DIMENSION_CONFIGS = [
    {
      key: 'plot',
      icon: 'book-open',
      title: 'Plot & Narrative Premise',
      desc: 'Controls how strictly character storylines, premise, and narrative trajectory must match the target book.'
    },
    {
      key: 'tone',
      icon: 'orbit',
      title: 'Atmospheric Mood & Emotional Tone',
      desc: 'Aligns emotional atmosphere, psychological dread, comedic warmth, or existential tension.'
    },
    {
      key: 'style',
      icon: 'target',
      title: 'Writing Style & Point of View',
      desc: 'Matches narrative voice (1st vs 3rd person) and prose complexity (Lyrical, Technical, Sharp, or Grounded).'
    },
    {
      key: 'pacing',
      icon: 'clock',
      title: 'Story Pacing & Narrative Velocity',
      desc: 'Ensures story speed syncs (Slow-burn meditative character build vs propulsive thriller velocity).'
    },
    {
      key: 'community',
      icon: 'users',
      title: 'Audience Co-Taste ("Readers Also Enjoyed")',
      desc: 'Blends Item2Vec behavioral collaborative signals from readers who loved the target book.'
    }
  ];

  const dimensionCardsHtml = DIMENSION_CONFIGS.map(dim => {
    const val = currentWeights[dim.key] || 4;
    const info = PRIORITY_LEVELS[val] || PRIORITY_LEVELS[4];
    const badgeText = (dim.key === 'community') 
      ? `${val}: ${COMMUNITY_PRIORITY_LABELS[val] || info.label}` 
      : `${val}: ${info.label} (${info.mult}x)`;

    return `
      <div class="dimension-card">
        <div class="dimension-card-header">
          <div class="dimension-info">
            <div class="dimension-title">${renderIcon(dim.icon, 'dim-icon')} ${dim.title}</div>
            <div class="dimension-subtitle">${dim.desc}</div>
          </div>
          <span id="badge-${dim.key}" class="priority-badge ${info.badgeClass}">${badgeText}</span>
        </div>
        <div class="slider-wrapper">
          <div class="slider-track-container">
            <div class="slider-ticks" id="ticks-${dim.key}">
              ${[1,2,3,4,5,6,7].map(i => `<span class="tick-mark ${i <= val ? 'active-tick' : ''}"></span>`).join('')}
            </div>
            <input type="range" id="slider-input-${dim.key}" class="custom-range priority-slider" min="1" max="7" step="1" value="${val}" oninput="onWeightSliderChange('${dim.key}', this.value); updateStudioSummary();" />
          </div>
          <div class="slider-tick-labels" id="labels-${dim.key}">
            <span>1 (Ignore 0x)</span>
            <span>2</span>
            <span>3</span>
            <span class="${val === 4 ? 'active-label' : ''}">4 (Balanced 1.0x)</span>
            <span>5</span>
            <span>6</span>
            <span>7 (Dominant 2.2x)</span>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // 1-Click Quick Presets HTML
  const presetsHtml = TUNING_PRESETS.map(p => `
    <span class="preset-chip" onclick="applyTuningPreset('${p.id}')" title="${p.desc}">
      ${renderIcon(p.icon)} <span>${p.label}</span>
    </span>
  `).join('');

  // Subclusters Rendering
  const categories = [
    { title: 'World & Setting', icon: 'orbit', key: 'World & Setting' },
    { title: 'Core Themes', icon: 'sparkles', key: 'Core Themes' },
    { title: 'Tropes & Conflicts', icon: 'swords', key: 'Tropes & Conflicts' },
    { title: 'Psychological Dynamics', icon: 'brain', key: 'Psychological Dynamics' }
  ];

  const subclusteredCardsHtml = categories.map(cat => {
    const motifs = (subclusteredMotifs && subclusteredMotifs[cat.key]) ? subclusteredMotifs[cat.key] : [];
    if (motifs.length === 0) return '';

    const pillsHtml = motifs.map(m => {
      const state = motifStates.get(m) || 'neutral';
      const info = MOTIF_LEVELS[state] || MOTIF_LEVELS['neutral'];
      return `
        <span class="concept-pill ${info.class}" data-keyword="${escapeHtml(m)}" onclick="cycleMotifState('${escapeHtml(m)}')">
          <span>${info.icon}</span>
          <span>${escapeHtml(m)}</span>
          ${info.tag ? `<span class="pill-badge-tag">${info.tag}</span>` : ''}
        </span>
      `;
    }).join('');

    return `
      <div class="subcluster-category-card" data-cat="${escapeHtml(cat.key)}">
        <div class="subcluster-category-header">
          ${renderIcon(cat.icon)} <span>${cat.title}</span>
        </div>
        <div class="concept-pills-row">
          ${pillsHtml}
        </div>
      </div>
    `;
  }).join('');

  const activeCount = Array.from(motifStates.values()).filter(s => s !== 'neutral').length;

  spotlightCard.innerHTML = `
    <!-- Top Target Book Hero Strip -->
    <div class="spotlight-header">
      <div>
        <div style="display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;">
          <span class="spotlight-anchor-tag">${renderIcon('star', 'gold-icon')} Anchor Literature</span>
          ${targetBook.series_info ? `<span class="series-badge">${renderIcon('library')} ${escapeHtml(targetBook.series_info.full_tag)}</span>` : ''}
        </div>
        <h2 style="font-size: 1.6rem; font-weight: 800; font-family: 'Playfair Display', serif; color: #ffffff; margin-top: 0.4rem; cursor: pointer;" onclick="openBookModal('${escapeHtml(targetBook.id)}')">${escapeHtml(targetBook.title)}</h2>
        <div style="font-size: 1rem; color: var(--text-secondary); margin-top: 0.2rem;">
          by <strong style="color: #e5a93c;">${escapeHtml(targetBook.author || 'Unknown')}</strong> &bull; 
          <span style="color: var(--text-muted);">${escapeHtml(targetBook.pub_date || '')}</span>
        </div>
        <div class="book-metadata-row" style="margin-top: 0.5rem;">
          ${targetBook.community_rating ? `<span class="rating-badge">${renderIcon('star', 'gold-star')} ${targetBook.community_rating}★ ${targetBook.ratings_count ? `<span style="opacity: 0.85; font-size: 0.68rem;">(${Number(targetBook.ratings_count).toLocaleString()})</span>` : ''}</span>` : ''}
          ${targetBook.popularity ? `<span class="popularity-badge">${renderIcon('flame', 'flame-icon')} ${targetBook.popularity.label}</span>` : ''}
          ${targetBook.readability ? `<span class="readability-badge">${renderIcon('book-open')} Reading Ease: ${escapeHtml(targetBook.readability.label)}</span>` : ''}
        </div>
      </div>
      <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
        <button class="action-btn bolster-btn" onclick="bolsterBookLive('${escapeHtml(targetBook.id)}')">
          ${renderIcon('globe')} Bolster via Web
        </button>
        <button class="action-btn action-btn-subtle" onclick="openBookModal('${escapeHtml(targetBook.id)}')">
          ${renderIcon('book-open')} View Full Analysis
        </button>
        <button class="action-btn apply-tuning-btn pending-changes" onclick="handleBookSimilarSearch(currentTargetId)">
          ${renderIcon('zap')} Synthesize Vector Search ➔
        </button>
      </div>
    </div>
    <div class="genre-tags">${genres}</div>
    <p style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6; margin: 0.5rem 0; background: rgba(0,0,0,0.25); padding: 0.8rem 1rem; border-radius: var(--radius-sm); border-left: 3px solid #e5a93c;">${escapeHtml(targetBook.summary)}</p>

    <!-- Vector Tuning Studio -->
    <div class="tuning-panel">
      <div class="studio-header">
        <div class="studio-tabs">
          <button id="tab-btn-weights" class="studio-tab-btn ${currentStudioTab === 'weights' ? 'active' : ''}" onclick="setStudioTab('weights')">
            ${renderIcon('sliders')}
            <span>Dimensional Weights</span>
            <span class="studio-tab-count">5</span>
          </button>
          <button id="tab-btn-motifs" class="studio-tab-btn ${currentStudioTab === 'motifs' ? 'active' : ''}" onclick="setStudioTab('motifs')">
            ${renderIcon('target')}
            <span>Thematic Motifs & Tropes</span>
            <span id="motifs-tab-count" class="studio-tab-count">${activeCount > 0 ? `${activeCount} active` : '0'}</span>
          </button>
        </div>

        <div style="display: flex; gap: 0.6rem; align-items: center;">
          <button class="action-btn" style="background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.12); color: #cbd5e1; font-size: 0.78rem; padding: 0.4rem 0.8rem;" onclick="resetTuningDefaults()" title="Reset all sliders and motif filters">
            ${renderIcon('rotate-ccw')} Reset Calibration
          </button>
        </div>
      </div>

      <!-- Quick Match Presets Bar -->
      <div class="presets-bar">
        <span class="presets-label">${renderIcon('zap')} Calibration Presets:</span>
        ${presetsHtml}
      </div>

      <!-- Tab 1: Dimensional Weights Panel -->
      <div id="studio-panel-weights" style="display: ${currentStudioTab === 'weights' ? 'block' : 'none'};">
        <div class="dimension-cards-grid">
          ${dimensionCardsHtml}
        </div>
      </div>

      <!-- Tab 2: Thematic Motifs Studio Panel -->
      <div id="studio-panel-motifs" style="display: ${currentStudioTab === 'motifs' ? 'block' : 'none'};">
        <div class="motifs-studio-container">
          <!-- Active Motifs Tray -->
          <div class="active-motifs-tray">
            <span class="active-motifs-label">${renderIcon('target')} Active Filters:</span>
            <span id="active-motifs-empty" style="font-size: 0.75rem; color: #94a3b8;">Click any motif below to cycle priority (+1.0x ➔ +1.6x ➔ +2.2x ➔ Exclude)</span>
            <div id="active-motifs-chips" style="display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center;"></div>
          </div>

          <!-- Inline Quick Trope Creator -->
          <div class="inline-trope-creator">
            <span style="font-size: 0.8rem; font-weight: 700; color: #e5a93c; white-space: nowrap; display: flex; align-items: center; gap: 0.3rem;">${renderIcon('plus')} Custom Trope:</span>
            <input type="text" id="inline-trope-input" class="inline-trope-input" placeholder="e.g. 'time loop', 'anti-hero', 'space fleet', 'hard magic system'..." onkeydown="if(event.key==='Enter') submitInlineCustomTrope();" />
            <div class="priority-choice-pills">
              <span class="choice-pill active" data-level="boost-2" onclick="selectInlineTropeLevel('boost-2', this)"><span class="status-indicator-dot dot-boost-2"></span> +1.0x</span>
              <span class="choice-pill" data-level="boost-3" onclick="selectInlineTropeLevel('boost-3', this)"><span class="status-indicator-dot dot-boost-3"></span> +1.6x</span>
              <span class="choice-pill" data-level="boost-4" onclick="selectInlineTropeLevel('boost-4', this)"><span class="status-indicator-dot dot-boost-4"></span> +2.2x</span>
              <span class="choice-pill" data-level="exclude" onclick="selectInlineTropeLevel('exclude', this)"><span class="status-indicator-dot dot-exclude"></span> Exclude</span>
            </div>
            <button class="action-btn btn-search-primary" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;" onclick="submitInlineCustomTrope()">
              ${renderIcon('plus')} Inject
            </button>
          </div>

          <!-- Category Filter Bar -->
          <div class="motif-category-tabs">
            <span class="category-tab-chip active" data-cat="all" onclick="filterMotifsByCategory('all')">All Sub-Clusters</span>
            <span class="category-tab-chip" data-cat="World & Setting" onclick="filterMotifsByCategory('World & Setting')">${renderIcon('orbit')} World & Setting</span>
            <span class="category-tab-chip" data-cat="Core Themes" onclick="filterMotifsByCategory('Core Themes')">${renderIcon('sparkles')} Core Themes</span>
            <span class="category-tab-chip" data-cat="Tropes & Conflicts" onclick="filterMotifsByCategory('Tropes & Conflicts')">${renderIcon('swords')} Tropes & Conflicts</span>
            <span class="category-tab-chip" data-cat="Psychological Dynamics" onclick="filterMotifsByCategory('Psychological Dynamics')">${renderIcon('brain')} Psychological Dynamics</span>
          </div>

          <!-- Subclusters Grid -->
          <div class="subclusters-grid">
            ${subclusteredCardsHtml}
            <div id="custom-motifs-subcluster-card" class="subcluster-category-card" style="display: none;" data-cat="custom">
              <div class="subcluster-category-header">${renderIcon('sparkles')} User-Defined Custom Tropes</div>
              <div class="concept-pills-row"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Studio Footer Toolbar -->
      <div class="studio-footer-toolbar">
        <div id="studio-summary-text" class="studio-summary-text">
          Active Vector Config: 5 Dimensions Set • ${activeCount} Thematic Filters Active
        </div>
        <button id="btn-apply-tuning" class="action-btn apply-tuning-btn" onclick="applyTuningSearch()">
          ${renderIcon('zap')} Synthesize Vector Search ➔
        </button>
      </div>
    </div>
  `;

  renderActiveMotifsTray();
  renderCustomMotifsCategoryCard();
}

async function handleBookSimilarSearch(bookIdOrTitle) {
  const target = bookIdOrTitle || currentTargetId || document.getElementById('book-input').value.trim();
  if (!target) return;
  currentTargetId = target;

  const topK = parseInt(document.getElementById('topk-select')?.value || 12);
  const genre = document.getElementById('genre-select')?.value || '';

  showLoading(`Searching 25,101 books for nearest weighted vectors to "${target}"...`);

  try {
    const weight_plot = PRIORITY_LEVELS[currentWeights.plot]?.mult ?? 1.0;
    const weight_tone = PRIORITY_LEVELS[currentWeights.tone]?.mult ?? 0.7;
    const weight_style = PRIORITY_LEVELS[currentWeights.style]?.mult ?? 0.7;
    const weight_pacing = PRIORITY_LEVELS[currentWeights.pacing]?.mult ?? 0.7;
    const weight_community = PRIORITY_LEVELS[currentWeights.community]?.mult ?? 1.0;

    const boostList = [];
    const excludeList = [];
    motifStates.forEach((state, kw) => {
      if (state.startsWith('boost')) {
        const mult = MOTIF_LEVELS[state]?.mult ?? 1.0;
        boostList.push(`${kw}:${mult}`);
      } else if (state === 'exclude') {
        excludeList.push(kw);
      }
    });

    let url = `/api/similar/${encodeURIComponent(target)}?top_k=${topK}&weight_plot=${weight_plot}&weight_tone=${weight_tone}&weight_style=${weight_style}&weight_pacing=${weight_pacing}&weight_community=${weight_community}`;
    if (genre) url += `&genre=${encodeURIComponent(genre)}`;
    if (boostList.length > 0) url += `&boost_keywords=${encodeURIComponent(boostList.join(','))}`;
    if (excludeList.length > 0) url += `&exclude_keywords=${encodeURIComponent(excludeList.join(','))}`;

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

    const applyBtn = document.getElementById('btn-apply-tuning');
    if (applyBtn) {
      applyBtn.classList.remove('pending-changes');
      applyBtn.textContent = '✅ Search Updated';
      setTimeout(() => {
        if (applyBtn) applyBtn.textContent = '⚡ Run Vector Search & Discover Similar ➔';
      }, 2500);
    }
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

  // Extended zoom up to 50x magnification (Mouse Wheel)
  galaxyCanvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    galaxyTransform.scale = Math.max(0.2, Math.min(50.0, galaxyTransform.scale * zoomFactor));
    updateZoomIndicator();
    requestGalaxyDraw();
  }, { passive: false });

  // Mobile Touch Interactions: 1-Finger Pan & 2-Finger Pinch-to-Zoom
  let initialTouchDist = null;
  let initialTouchScale = 1.0;
  let touchStartPos = { x: 0, y: 0 };
  let touchHasDragged = false;

  galaxyCanvas.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      isDraggingGalaxy = true;
      touchHasDragged = false;
      const t = e.touches[0];
      touchStartPos = { x: t.clientX, y: t.clientY };
      dragStart = { x: t.clientX - galaxyTransform.x, y: t.clientY - galaxyTransform.y };
    } else if (e.touches.length === 2) {
      isDraggingGalaxy = false;
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      initialTouchDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      initialTouchScale = galaxyTransform.scale;
    }
  }, { passive: false });

  galaxyCanvas.addEventListener('touchmove', (e) => {
    e.preventDefault(); // Prevent accidental mobile browser page scrolling while dragging canvas
    if (e.touches.length === 1 && isDraggingGalaxy) {
      const t = e.touches[0];
      const dist = Math.hypot(t.clientX - touchStartPos.x, t.clientY - touchStartPos.y);
      if (dist > 6) {
        touchHasDragged = true;
      }
      galaxyTransform.x = t.clientX - dragStart.x;
      galaxyTransform.y = t.clientY - dragStart.y;
      requestGalaxyDraw();
    } else if (e.touches.length === 2 && initialTouchDist) {
      touchHasDragged = true;
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      const currentDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      const scaleFactor = currentDist / initialTouchDist;
      galaxyTransform.scale = Math.max(0.2, Math.min(50.0, initialTouchScale * scaleFactor));
      updateZoomIndicator();
      requestGalaxyDraw();
    }
  }, { passive: false });

  galaxyCanvas.addEventListener('touchend', (e) => {
    if (e.touches.length === 0) {
      if (!touchHasDragged) {
        // Stationary tap on star on mobile
        const found = findSpatialPointNear(touchStartPos.x, touchStartPos.y, 25);
        if (found) {
          selectedPoint = found;
          openBookModal(found.id);
        }
      }
      isDraggingGalaxy = false;
      initialTouchDist = null;
    }
  });

  galaxyCanvas.addEventListener('touchcancel', () => {
    isDraggingGalaxy = false;
    initialTouchDist = null;
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

// O(1) Spatial Hash Grid Point Finder (Mouse & Touch)
function findSpatialPointNear(clientX, clientY, hitRadiusPx = 18) {
  if (!galaxyCanvas || galaxyData.length === 0) return null;
  const rect = galaxyCanvas.getBoundingClientRect();
  if (rect.width === 0 || rect.height === 0) return null;

  const scaleX = galaxyCanvas.width / rect.width;
  const scaleY = galaxyCanvas.height / rect.height;

  const mouseX = (clientX - rect.left) * scaleX;
  const mouseY = (clientY - rect.top) * scaleY;

  const dataMouseX = (mouseX - galaxyTransform.x) / galaxyTransform.scale;
  const dataMouseY = (mouseY - galaxyTransform.y) / galaxyTransform.scale;
  const dataRadius = hitRadiusPx / galaxyTransform.scale;

  const centerGx = Math.floor(dataMouseX / GRID_CELL_SIZE);
  const centerGy = Math.floor(dataMouseY / GRID_CELL_SIZE);

  let closest = null;
  let minDist = dataRadius;

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
  return closest;
}

// O(1) Spatial Hash Grid Mouse Hover Lookup
function handleGalaxyHover(e) {
  if (!galaxyCanvas || galaxyData.length === 0) return;
  const rect = galaxyCanvas.getBoundingClientRect();
  if (rect.width === 0 || rect.height === 0) return;

  const closest = findSpatialPointNear(e.clientX, e.clientY, 18);

  if (hoveredPoint !== closest) {
    hoveredPoint = closest;
    requestGalaxyDraw();
  }

  const tooltip = document.getElementById('galaxy-tooltip');
  if (hoveredPoint && tooltip) {
    const cssX = e.clientX - rect.left;
    const cssY = e.clientY - rect.top;
    
    // Bounds-aware tooltip positioning (prevents right/bottom clipping on mobile)
    const tooltipWidth = 280;
    const leftPos = (cssX + tooltipWidth + 30 > rect.width) ? Math.max(10, cssX - tooltipWidth - 10) : cssX + 15;
    const topPos = (cssY + 140 > rect.height) ? Math.max(10, cssY - 120) : cssY + 15;

    tooltip.style.display = 'block';
    tooltip.style.left = `${leftPos}px`;
    tooltip.style.top = `${topPos}px`;
    tooltip.innerHTML = `
      <div style="font-weight: 700; color: #fff; font-size: 0.95rem;">${escapeHtml(hoveredPoint.title)}</div>
      <div style="color: var(--accent-cyan); font-size: 0.8rem; margin: 0.2rem 0;">by ${escapeHtml(hoveredPoint.author || 'Unknown')}</div>
      <div style="color: var(--text-muted); font-size: 0.75rem;">${escapeHtml(hoveredPoint.genres || '')}</div>
      <div style="font-size: 0.75rem; color: #a5b4fc; margin-top: 0.4rem;">Tap star to view full details ➔</div>
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
  latencyEl.innerHTML = `${renderIcon('zap')} Vector Search & Manifold: <strong>${latency} ms</strong>`;

  filteredBooks.forEach(b => {
    const card = document.createElement('div');
    card.className = 'book-card';
    
    const scoreVal = b.weighted_score !== undefined ? b.weighted_score : b.similarity_score;
    const simPercent = scoreVal !== undefined ? Math.round(scoreVal * 100) : 85;

    const genresHtml = (b.genres || 'General')
      .split(',')
      .slice(0, 3)
      .map(g => `<span class="genre-tag">${escapeHtml(g.trim())}</span>`)
      .join('');

    const pop = b.popularity || {
      tier: 'Popular Favorite',
      icon: 'library',
      label: 'Popular Favorite',
      description: 'Community Favorite',
      ratings_count: b.ratings_count || 4500,
      score: 70,
      rating: b.community_rating || 4.15
    };

    const style = b.style_profile || {
      pov: (b.summary || '').toLowerCase().includes(' i ') ? 'First Person' : 'Third Person',
      pacing: (b.genres || '').toLowerCase().includes('thriller') ? 'Fast-Paced' : 'Slow-Burn',
      prose_style: 'Grounded & Narrative'
    };

    const breakdown = b.match_breakdown || {
      plot_pct: Math.min(99, Math.max(50, simPercent)),
      theme_pct: Math.min(99, Math.max(45, Math.round(simPercent * 0.95))),
      style_pct: Math.min(99, Math.max(50, Math.round(simPercent * 0.92))),
      audience_pct: Math.min(99, Math.max(40, Math.round((b.collaborative_affinity || 0.65) * 100)))
    };

    // Explainability Reasons HTML
    let reasonsHtml = '';
    if (b.similarity_reasons && b.similarity_reasons.length > 0) {
      const reasonPills = b.similarity_reasons
        .map(r => `<span class="reason-pill">${renderIcon('lightbulb')} ${escapeHtml(r)}</span>`)
        .join('');
      reasonsHtml = `
        <div class="why-similar-box">
          <div class="why-similar-title">${renderIcon('target')} Similarity Rationale:</div>
          <div class="why-similar-tags">${reasonPills}</div>
        </div>
      `;
    }

    const metadataBadgesHtml = `
      <div class="book-metadata-row">
        ${b.series_info ? `<span class="series-badge">${renderIcon('library')} ${escapeHtml(b.series_info.full_tag)}</span>` : ''}
        <span class="rating-badge">${renderIcon('star', 'gold-star')} ${pop.rating}★ <span style="opacity: 0.85; font-size: 0.68rem;">(${Number(pop.ratings_count).toLocaleString()})</span></span>
        <span class="popularity-badge">${renderIcon('flame', 'flame-icon')} ${pop.label}</span>
        ${b.readability ? `<span class="readability-badge">${renderIcon('book-open')} ${escapeHtml(b.readability.label)}</span>` : ''}
        ${b.collaborative_affinity && b.collaborative_affinity >= 0.70 ? `<span class="collab-affinity-badge">${renderIcon('users')} ${Math.round(b.collaborative_affinity * 100)}% Audience Co-Taste</span>` : ''}
      </div>
    `;

    const matchBreakdownHtml = `
      <div class="match-breakdown-card">
        <div class="match-breakdown-header">
          <span>${renderIcon('bar-chart')} Vector Decomposition</span>
          <span style="color: #e5a93c; font-weight: 800; font-family: monospace;">${simPercent}% Match</span>
        </div>
        <div class="breakdown-bars-grid">
          <div class="breakdown-bar-item">
            <div class="breakdown-bar-label">
              <span>${renderIcon('book-open')} Plot & Premise</span>
              <span>${breakdown.plot_pct}%</span>
            </div>
            <div class="breakdown-bar-track">
              <div class="breakdown-bar-fill fill-plot" style="width: ${breakdown.plot_pct}%;"></div>
            </div>
          </div>
          <div class="breakdown-bar-item">
            <div class="breakdown-bar-label">
              <span>${renderIcon('sparkles')} Thematic Motifs</span>
              <span>${breakdown.theme_pct}%</span>
            </div>
            <div class="breakdown-bar-track">
              <div class="breakdown-bar-fill fill-theme" style="width: ${breakdown.theme_pct}%;"></div>
            </div>
          </div>
          <div class="breakdown-bar-item">
            <div class="breakdown-bar-label">
              <span>${renderIcon('target')} Style & Voice</span>
              <span>${breakdown.style_pct}%</span>
            </div>
            <div class="breakdown-bar-track">
              <div class="breakdown-bar-fill fill-style" style="width: ${breakdown.style_pct}%;"></div>
            </div>
          </div>
          <div class="breakdown-bar-item">
            <div class="breakdown-bar-label">
              <span>${renderIcon('users')} Audience Co-Taste</span>
              <span>${breakdown.audience_pct}%</span>
            </div>
            <div class="breakdown-bar-track">
              <div class="breakdown-bar-fill fill-audience" style="width: ${breakdown.audience_pct}%;"></div>
            </div>
          </div>
        </div>
      </div>
    `;

    const dnaStripHtml = `
      <div class="narrative-dna-strip">
        <span class="dna-pill">${renderIcon('target')} ${escapeHtml(style.pov)}</span>
        <span class="dna-pill">${renderIcon('clock')} ${escapeHtml(style.pacing)}</span>
        <span class="dna-pill">${renderIcon('feather')} ${escapeHtml(style.prose_style || 'Grounded')}</span>
      </div>
    `;

    card.innerHTML = `
      <div>
        <div class="card-top">
          <div>
            <h3 class="book-title" style="cursor: pointer;" onclick="openBookModal('${escapeHtml(b.id)}')">${escapeHtml(b.title)}</h3>
            <div class="book-author">by <strong style="color: #cbd5e1;">${escapeHtml(b.author || 'Unknown')}</strong> &bull; <span style="color: var(--text-muted); font-size: 0.8rem;">${escapeHtml(b.pub_date || '')}</span></div>
          </div>
          ${simPercent !== null ? `<div class="sim-score-badge">${simPercent}% Match</div>` : ''}
        </div>
        ${metadataBadgesHtml}
        ${matchBreakdownHtml}
        ${dnaStripHtml}
        <div class="genre-tags">${genresHtml}</div>
        ${reasonsHtml}
        <p class="book-summary" title="${escapeHtml(b.summary)}" style="cursor: pointer;" onclick="openBookModal('${escapeHtml(b.id)}')">${escapeHtml(b.summary)}</p>
      </div>
      <div class="card-footer" style="margin-top: 1rem;">
        <button class="action-btn action-btn-subtle" onclick="openBookModal('${escapeHtml(b.id)}')">
          ${renderIcon('bar-chart')} Deep Analysis
        </button>
        <button class="btn-similar" onclick="exploreBook('${escapeHtml(b.id)}', '${escapeHtml(b.title).replace(/'/g, "\\'")}')">
          <span>Discover Similar</span>
          ${renderIcon('arrow-right')}
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
