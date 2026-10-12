/**
 * PSIR Visual Inspector & Markup Tool
 * Allows clicking any element on the page to mark, annotate, live-edit, and copy change requests.
 */

(function () {
  'use strict';

  // Prevent multiple initializations
  if (window.__PSIR_INSPECTOR_ACTIVE__) return;
  window.__PSIR_INSPECTOR_ACTIVE__ = true;

  const STORAGE_KEY = 'psir_visual_inspector_marks';
  let isInspectorActive = false;
  let isDirectEditActive = false;
  let hoveredElement = null;
  let selectedElement = null;
  let marks = [];

  // Load persisted marks
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) marks = JSON.parse(saved);
  } catch (e) {
    console.warn('Failed to load marks from localStorage', e);
  }

  // Inject Styles
  const styleEl = document.createElement('style');
  styleEl.id = 'psir-inspector-styles';
  styleEl.textContent = `
    /* Visual Inspector Overlay */
    .__insp-hover-box {
      position: absolute;
      pointer-events: none;
      border: 2px dashed #0284c7;
      background: rgba(2, 132, 199, 0.12);
      border-radius: 4px;
      z-index: 999990;
      display: none;
      box-shadow: 0 0 12px rgba(2, 132, 199, 0.35);
      transition: top 0.05s ease, left 0.05s ease, width 0.05s ease, height 0.05s ease;
    }

    .__insp-hover-tag {
      position: absolute;
      top: -24px;
      left: 0;
      background: #0284c7;
      color: #ffffff;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }

    .__insp-pin {
      position: absolute;
      width: 24px;
      height: 24px;
      background: #ef4444;
      color: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 11px;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(239, 68, 68, 0.5), 0 0 0 2px #ffffff;
      cursor: pointer;
      z-index: 999995;
      transform: translate(-50%, -50%);
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .__insp-pin:hover {
      transform: translate(-50%, -50%) scale(1.2);
    }

    /* Floating Inspector Toolbar Dock */
    .__insp-dock {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 1000000;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 10px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .__insp-dock-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.94);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 8px 14px;
      border-radius: 9999px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.05);
      color: #f8fafc;
      transition: all 0.2s ease;
    }

    .__insp-dock-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #f1f5f9;
      font-family: inherit;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 9999px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }
    .__insp-dock-btn:hover {
      background: rgba(255, 255, 255, 0.18);
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-1px);
    }
    .__insp-dock-btn.active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(2, 132, 199, 0.5);
    }
    .__insp-dock-btn.accent {
      background: #10b981;
      border-color: #34d399;
      color: #ffffff;
    }

    .__insp-dock-badge {
      background: #ef4444;
      color: #ffffff;
      font-size: 10px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 9999px;
      margin-left: 2px;
    }

    /* Modal / Popover on Selected Element */
    .__insp-popover {
      position: fixed;
      z-index: 1000001;
      width: 320px;
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 12px;
      box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05);
      color: #f8fafc;
      padding: 14px;
      display: none;
      flex-direction: column;
      gap: 10px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      animation: __inspFadeIn 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes __inspFadeIn {
      from { opacity: 0; transform: scale(0.96) translateY(4px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }

    .__insp-popover-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 8px;
    }
    .__insp-popover-tag {
      font-family: monospace;
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
      max-width: 220px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .__insp-close-btn {
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 16px;
      cursor: pointer;
      padding: 2px;
      line-height: 1;
    }
    .__insp-close-btn:hover { color: #ffffff; }

    .__insp-preview-text {
      font-size: 11.5px;
      color: #94a3b8;
      background: rgba(0, 0, 0, 0.3);
      padding: 6px 8px;
      border-radius: 6px;
      max-height: 50px;
      overflow-y: auto;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .__insp-textarea {
      width: 100%;
      box-sizing: border-box;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      color: #ffffff;
      padding: 8px;
      font-family: inherit;
      font-size: 12px;
      resize: vertical;
      min-height: 54px;
      outline: none;
    }
    .__insp-textarea:focus {
      border-color: #38bdf8;
    }

    .__insp-quick-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }
    .__insp-chip {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      font-size: 10px;
      padding: 3px 6px;
      border-radius: 4px;
      cursor: pointer;
    }
    .__insp-chip:hover {
      background: rgba(2, 132, 199, 0.3);
      border-color: #38bdf8;
      color: #ffffff;
    }

    .__insp-popover-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
      margin-top: 4px;
    }

    /* Drawer of All Annotations */
    .__insp-drawer {
      width: 360px;
      max-height: 440px;
      background: rgba(15, 23, 42, 0.97);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 14px;
      box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.5);
      color: #f8fafc;
      padding: 16px;
      display: none;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 8px;
      animation: __inspFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .__insp-drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 10px;
    }
    .__insp-drawer-title {
      font-size: 13px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .__insp-marks-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      overflow-y: auto;
      max-height: 300px;
      padding-right: 4px;
    }
    .__insp-mark-item {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 11.5px;
    }
    .__insp-mark-item:hover {
      border-color: rgba(56, 189, 248, 0.4);
    }
    .__insp-mark-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .__insp-mark-num {
      background: #ef4444;
      color: #ffffff;
      font-weight: 800;
      font-size: 10px;
      padding: 1px 6px;
      border-radius: 999px;
    }
    .__insp-mark-selector {
      font-family: monospace;
      color: #38bdf8;
      font-size: 10.5px;
      max-width: 220px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .__insp-mark-text {
      color: #e2e8f0;
      font-size: 12px;
      line-height: 1.4;
      white-space: pre-wrap;
    }
    .__insp-toast {
      position: fixed;
      top: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: #0f172a;
      color: #ffffff;
      padding: 10px 20px;
      border-radius: 9999px;
      font-size: 12.5px;
      font-weight: 600;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
      z-index: 1000005;
      display: none;
      animation: __inspFadeIn 0.2s ease;
    }
  `;
  document.head.appendChild(styleEl);

  // Hover Outline Box
  const hoverBox = document.createElement('div');
  hoverBox.className = '__insp-hover-box';
  const hoverTag = document.createElement('div');
  hoverTag.className = '__insp-hover-tag';
  hoverBox.appendChild(hoverTag);
  document.body.appendChild(hoverBox);

  // Pin Container
  const pinContainer = document.createElement('div');
  pinContainer.id = '__insp-pins-container';
  document.body.appendChild(pinContainer);

  // Toast
  const toast = document.createElement('div');
  toast.className = '__insp-toast';
  document.body.appendChild(toast);

  function showToast(msg) {
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 3000);
  }

  // Popover for clicked element
  const popover = document.createElement('div');
  popover.className = '__insp-popover';
  popover.innerHTML = `
    <div class="__insp-popover-header">
      <span class="__insp-popover-tag" id="__inspTagTitle">Element</span>
      <button class="__insp-close-btn" id="__inspClosePopover">&times;</button>
    </div>
    <div class="__insp-preview-text" id="__inspPreviewText">Text preview...</div>
    <div class="__insp-quick-chips">
      <span class="__insp-chip" data-chip="[🎨 Color/Style]">🎨 Style</span>
      <span class="__insp-chip" data-chip="[📐 Layout/Size]">📐 Layout</span>
      <span class="__insp-chip" data-chip="[✏️ Text change]">✏️ Text</span>
      <span class="__insp-chip" data-chip="[🗑️ Remove]">🗑️ Remove</span>
      <span class="__insp-chip" data-chip="[➕ Add item]">➕ Add</span>
    </div>
    <textarea class="__insp-textarea" id="__inspNoteInput" placeholder="What should be modified here? (e.g., make bolder, change text, change button layout)..."></textarea>
    <div class="__insp-popover-actions">
      <button class="__insp-dock-btn" id="__inspLiveEditBtn" title="Directly edit words inside this element">✏️ Edit Text</button>
      <button class="__insp-dock-btn accent" id="__inspSaveMarkBtn">📌 Pin Mark</button>
    </div>
  `;
  document.body.appendChild(popover);

  // Dock & Drawer
  const dock = document.createElement('div');
  dock.className = '__insp-dock';
  dock.innerHTML = `
    <!-- Annotations Review Drawer -->
    <div class="__insp-drawer" id="__inspDrawer">
      <div class="__insp-drawer-header">
        <div class="__insp-drawer-title">
          <span>📝 Marked Modifications</span>
          <span class="__insp-dock-badge" id="__inspDrawerBadge">0</span>
        </div>
        <button class="__insp-close-btn" id="__inspCloseDrawer">&times;</button>
      </div>
      <div class="__insp-marks-list" id="__inspMarksList">
        <!-- Rendered dynamically -->
      </div>
      <div style="display: flex; gap: 8px; justify-content: space-between;">
        <button class="__insp-dock-btn" id="__inspClearAllBtn" style="color: #f87171;">🗑️ Clear All</button>
        <button class="__insp-dock-btn accent" id="__inspCopyFeedbackBtn">📋 Copy for AI</button>
      </div>
    </div>

    <!-- Main Floating Bar -->
    <div class="__insp-dock-bar">
      <button class="__insp-dock-btn" id="__inspToggleModeBtn">
        <span>🎯 Inspector Mode</span>
        <span id="__inspModeStateText" style="opacity: 0.7; font-weight: 500;">OFF</span>
      </button>

      <button class="__insp-dock-btn" id="__inspDirectEditBtn" title="Click anywhere to type edits">
        <span>✏️ Direct Edit</span>
      </button>

      <button class="__insp-dock-btn" id="__inspReviewBtn">
        <span>📋 Marks</span>
        <span class="__insp-dock-badge" id="__inspBadgeCount">0</span>
      </button>
    </div>
  `;
  document.body.appendChild(dock);

  // Elements references
  const toggleModeBtn = document.getElementById('__inspToggleModeBtn');
  const modeStateText = document.getElementById('__inspModeStateText');
  const directEditBtn = document.getElementById('__inspDirectEditBtn');
  const reviewBtn = document.getElementById('__inspReviewBtn');
  const badgeCount = document.getElementById('badgeReviewCount'); // fallback or custom
  const inspBadgeCount = document.getElementById('__inspBadgeCount');
  const inspDrawer = document.getElementById('__inspDrawer');
  const inspDrawerBadge = document.getElementById('__inspDrawerBadge');
  const closeDrawer = document.getElementById('__inspCloseDrawer');
  const marksList = document.getElementById('__inspMarksList');
  const clearAllBtn = document.getElementById('__inspClearAllBtn');
  const copyFeedbackBtn = document.getElementById('__inspCopyFeedbackBtn');

  const closePopover = document.getElementById('__inspClosePopover');
  const tagTitle = document.getElementById('__inspTagTitle');
  const previewText = document.getElementById('__inspPreviewText');
  const noteInput = document.getElementById('__inspNoteInput');
  const liveEditBtn = document.getElementById('__inspLiveEditBtn');
  const saveMarkBtn = document.getElementById('__inspSaveMarkBtn');

  // Helper: Generate unique CSS selector
  function getUniqueSelector(el) {
    if (!el || el === document.body || el === document.documentElement) return 'body';
    if (el.id) return '#' + CSS.escape(el.id);

    let path = [];
    let current = el;
    while (current && current.nodeType === Node.ELEMENT_NODE && current !== document.body) {
      let selector = current.nodeName.toLowerCase();
      if (current.id) {
        selector += '#' + CSS.escape(current.id);
        path.unshift(selector);
        break;
      } else {
        let classes = Array.from(current.classList).filter(c => !c.startsWith('__insp-'));
        if (classes.length > 0) {
          selector += '.' + classes.slice(0, 2).map(c => CSS.escape(c)).join('.');
        }
        let sibling = current;
        let nth = 1;
        while ((sibling = sibling.previousElementSibling)) {
          if (sibling.nodeName.toLowerCase() === current.nodeName.toLowerCase()) nth++;
        }
        if (nth > 1) selector += `:nth-of-type(${nth})`;
      }
      path.unshift(selector);
      current = current.parentElement;
    }
    return path.join(' > ');
  }

  // Save marks to localStorage
  function persistMarks() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(marks));
    } catch (e) {}
    updateBadge();
    renderPins();
    renderDrawerMarks();
  }

  function updateBadge() {
    inspBadgeCount.textContent = marks.length;
    inspDrawerBadge.textContent = marks.length;
  }

  // Render Pins over the document
  function renderPins() {
    pinContainer.innerHTML = '';
    marks.forEach((m, idx) => {
      try {
        const target = document.querySelector(m.selector);
        if (target) {
          const rect = target.getBoundingClientRect();
          const pin = document.createElement('div');
          pin.className = '__insp-pin';
          pin.textContent = (idx + 1);
          pin.title = `Mark #${idx + 1}: ${m.note}`;
          pin.style.top = `${window.scrollY + rect.top + 8}px`;
          pin.style.left = `${window.scrollX + rect.left + 8}px`;
          pin.onclick = (e) => {
            e.stopPropagation();
            inspDrawer.style.display = 'flex';
          };
          pinContainer.appendChild(pin);
        }
      } catch (err) {}
    });
  }

  // Render Drawer items
  function renderDrawerMarks() {
    marksList.innerHTML = '';
    if (marks.length === 0) {
      marksList.innerHTML = `
        <div style="text-align: center; color: #94a3b8; padding: 24px 0; font-size: 12px;">
          🎯 No elements marked yet.<br>Turn on <b>Inspector Mode</b> and click any element on the page to mark it!
        </div>
      `;
      return;
    }

    marks.forEach((m, idx) => {
      const item = document.createElement('div');
      item.className = '__insp-mark-item';
      item.innerHTML = `
        <div class="__insp-mark-top">
          <span class="__insp-mark-num">#${idx + 1}</span>
          <span class="__insp-mark-selector" title="${m.selector}">${m.selector}</span>
          <button class="__insp-close-btn" data-del="${idx}" title="Delete this mark">&times;</button>
        </div>
        <div class="__insp-mark-text">${escapeHtml(m.note)}</div>
        ${m.originalText ? `<div style="font-size: 10px; color: #64748b;">Snippet: "${escapeHtml(m.originalText.slice(0, 50))}"</div>` : ''}
      `;
      marksList.appendChild(item);
    });

    // Attach delete listeners
    marksList.querySelectorAll('[data-del]').forEach(btn => {
      btn.onclick = (e) => {
        const i = parseInt(btn.getAttribute('data-del'));
        marks.splice(i, 1);
        persistMarks();
      };
    });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Position Popover safely on screen
  function positionPopover(targetEl) {
    const rect = targetEl.getBoundingClientRect();
    const pWidth = 320;
    const pHeight = 260;

    let left = rect.left;
    let top = rect.bottom + 8;

    // Check bottom boundary
    if (top + pHeight > window.innerHeight) {
      top = rect.top - pHeight - 8;
    }
    // Check right boundary
    if (left + pWidth > window.innerWidth) {
      left = window.innerWidth - pWidth - 16;
    }
    if (left < 10) left = 10;
    if (top < 10) top = 10;

    popover.style.left = `${left}px`;
    popover.style.top = `${top}px`;
    popover.style.display = 'flex';
  }

  // Quick Chips logic
  popover.querySelectorAll('.__insp-chip').forEach(chip => {
    chip.onclick = () => {
      const tag = chip.getAttribute('data-chip');
      noteInput.value = (tag + ' ' + noteInput.value).trim();
      noteInput.focus();
    };
  });

  // Toggle Inspector Mode
  toggleModeBtn.onclick = () => {
    isInspectorActive = !isInspectorActive;
    if (isInspectorActive) {
      toggleModeBtn.classList.add('active');
      modeStateText.textContent = 'ON';
      showToast('🎯 Inspector Mode ON: Click any element to mark or modify it');
    } else {
      toggleModeBtn.classList.remove('active');
      modeStateText.textContent = 'OFF';
      hoverBox.style.display = 'none';
      popover.style.display = 'none';
    }
  };

  // Toggle Direct In-Place Edit Mode
  directEditBtn.onclick = () => {
    isDirectEditActive = !isDirectEditActive;
    document.body.contentEditable = isDirectEditActive ? 'true' : 'false';
    if (isDirectEditActive) {
      directEditBtn.classList.add('active');
      showToast('✏️ Direct Edit ON: Click any text directly on the page to edit words!');
    } else {
      directEditBtn.classList.remove('active');
      showToast('🔒 Direct Edit OFF: Edits locked');
    }
  };

  // Review Drawer Toggle
  reviewBtn.onclick = () => {
    inspDrawer.style.display = (inspDrawer.style.display === 'flex') ? 'none' : 'flex';
  };
  closeDrawer.onclick = () => { inspDrawer.style.display = 'none'; };

  // Clear All Marks
  clearAllBtn.onclick = () => {
    if (confirm('Clear all visual marks?')) {
      marks = [];
      persistMarks();
      showToast('All marks cleared');
    }
  };

  // Copy Feedback for AI
  copyFeedbackBtn.onclick = () => {
    if (marks.length === 0) {
      showToast('No marks to copy yet! Mark elements first.');
      return;
    }

    let report = `### 🎯 Visual Modifications Requested:\n\n`;
    marks.forEach((m, idx) => {
      report += `**${idx + 1}. Element: \`${m.selector}\`**\n`;
      if (m.originalText) {
        report += `- Current Text/Context: "${m.originalText.slice(0, 70)}..."\n`;
      }
      report += `- **Requested Change:** ${m.note}\n\n`;
    });

    navigator.clipboard.writeText(report).then(() => {
      showToast('📋 Copied feedback to clipboard! Paste it into the AI chat.');
    }).catch(() => {
      prompt('Copy your feedback text below:', report);
    });
  };

  // Close Popover
  closePopover.onclick = () => {
    popover.style.display = 'none';
    selectedElement = null;
  };

  // Live Edit on Selected Element
  liveEditBtn.onclick = () => {
    if (selectedElement) {
      selectedElement.contentEditable = 'true';
      selectedElement.focus();
      popover.style.display = 'none';
      showToast(`✏️ You can now edit text in <${selectedElement.tagName.toLowerCase()}> directly`);
    }
  };

  // Pin / Save Mark
  saveMarkBtn.onclick = () => {
    if (!selectedElement) return;
    const note = noteInput.value.trim();
    if (!note) {
      showToast('Please type a note describing what to change');
      noteInput.focus();
      return;
    }

    const selector = getUniqueSelector(selectedElement);
    const textSnippet = selectedElement.innerText ? selectedElement.innerText.trim().slice(0, 100) : '';

    marks.push({
      selector,
      note,
      originalText: textSnippet,
      timestamp: Date.now()
    });

    persistMarks();
    popover.style.display = 'none';
    noteInput.value = '';
    selectedElement = null;
    showToast(`📌 Mark #${marks.length} pinned! Click "📋 Marks" to review.`);
  };

  // Mousemove for hover highlight
  document.addEventListener('mousemove', (e) => {
    if (!isInspectorActive) return;

    const el = e.target;
    // Ignore inspector own UI
    if (el.closest('.__insp-dock') || el.closest('.__insp-popover') || el.closest('.__insp-hover-box') || el.closest('.__insp-pin')) {
      return;
    }

    hoveredElement = el;
    const rect = el.getBoundingClientRect();

    hoverBox.style.top = `${window.scrollY + rect.top}px`;
    hoverBox.style.left = `${window.scrollX + rect.left}px`;
    hoverBox.style.width = `${rect.width}px`;
    hoverBox.style.height = `${rect.height}px`;
    hoverBox.style.display = 'block';

    const tagStr = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.classList.length ? '.' + Array.from(el.classList).slice(0, 2).join('.') : '');
    hoverTag.textContent = tagStr;
  }, true);

  // Click handler when Inspector Mode is ON
  document.addEventListener('click', (e) => {
    if (!isInspectorActive) return;

    const el = e.target;
    // Don't intercept clicks inside inspector UI
    if (el.closest('.__insp-dock') || el.closest('.__insp-popover') || el.closest('.__insp-hover-box') || el.closest('.__insp-pin')) {
      return;
    }

    e.preventDefault();
    e.stopPropagation();

    selectedElement = el;
    const selector = getUniqueSelector(el);
    tagTitle.textContent = selector;
    tagTitle.title = selector;
    previewText.textContent = (el.innerText || el.textContent || '(No text content)').trim().slice(0, 120);
    noteInput.value = '';

    positionPopover(el);
    noteInput.focus();
  }, true);

  // Reposition pins on resize/scroll
  window.addEventListener('resize', renderPins);
  window.addEventListener('scroll', renderPins);

  // Initial render
  updateBadge();
  renderPins();
  renderDrawerMarks();

  console.log('✅ PSIR Visual Inspector & Markup Tool loaded successfully.');
})();
