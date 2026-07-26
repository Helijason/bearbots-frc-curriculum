/**
 * version-picker.js
 * Floating version switcher. Reads /versions.json from the docs root.
 * Place in v1/js/ (and v2/js/ etc). No external dependencies.
 */
(function () {
  // ── Resolve paths ────────────────────────────────────────────────────────────
  const parts = window.location.pathname.split('/').filter(Boolean);
  const vIdx  = parts.findIndex(p => /^v\d+$/.test(p));
  if (vIdx === -1) return; // not inside a versioned directory

  const currentVersion = parts[vIdx];
  // Base = everything before the version segment, e.g. /bearbots-frc-curriculum/
  const base = '/' + parts.slice(0, vIdx).join('/') + '/';

  // ── Inject styles ────────────────────────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    #ver-picker {
      position: fixed;
      bottom: 18px;
      left: 18px;
      z-index: 9999;
      font-family: Helvetica, Arial, sans-serif;
      font-size: 12px;
    }
    #ver-picker .ver-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #2D6B6B;
      color: #fff;
      padding: 5px 10px;
      border-radius: 20px;
      cursor: pointer;
      user-select: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.25);
      transition: background 0.15s;
    }
    #ver-picker .ver-badge:hover { background: #245858; }
    #ver-picker .ver-badge .ver-caret {
      font-size: 9px;
      opacity: 0.75;
      transition: transform 0.15s;
    }
    #ver-picker.open .ver-caret { transform: rotate(180deg); }
    #ver-picker .ver-dropdown {
      display: none;
      position: absolute;
      bottom: calc(100% + 6px);
      left: 0;
      background: #fff;
      border: 1px solid #ccc;
      border-radius: 6px;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(0,0,0,0.15);
      min-width: 170px;
    }
    #ver-picker.open .ver-dropdown { display: block; }
    #ver-picker .ver-dropdown a {
      display: block;
      padding: 8px 12px;
      color: #222;
      text-decoration: none;
      transition: background 0.1s;
    }
    #ver-picker .ver-dropdown a:hover { background: #EAF4F4; }
    #ver-picker .ver-dropdown a.ver-current {
      font-weight: bold;
      color: #2D6B6B;
      pointer-events: none;
    }
    #ver-picker .ver-dropdown .ver-label {
      font-size: 10px;
      color: #888;
      padding: 6px 12px 2px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
  `;
  document.head.appendChild(style);

  // ── Fetch versions.json then render ─────────────────────────────────────────
  fetch(base + 'versions.json')
    .then(r => r.json())
    .then(data => render(data))
    .catch(() => renderFallback());

  function render(data) {
    const wrapper = document.createElement('div');
    wrapper.id = 'ver-picker';

    const badge = document.createElement('div');
    badge.className = 'ver-badge';
    badge.innerHTML = `
      <span>📦 ${currentVersion}${data.stable === currentVersion ? ' (stable)' : ''}</span>
      <span class="ver-caret">▲</span>
    `;

    const dropdown = document.createElement('div');
    dropdown.className = 'ver-dropdown';

    const lbl = document.createElement('div');
    lbl.className = 'ver-label';
    lbl.textContent = 'Switch version';
    dropdown.appendChild(lbl);

    data.versions.forEach(v => {
      const a = document.createElement('a');
      a.href = base + v + '/';
      const label = (data.labels && data.labels[v]) ? data.labels[v] : v;
      a.textContent = label + (data.stable === v ? ' ✓' : '');
      if (v === currentVersion) a.className = 'ver-current';
      dropdown.appendChild(a);
    });

    badge.addEventListener('click', () => wrapper.classList.toggle('open'));
    document.addEventListener('click', e => {
      if (!wrapper.contains(e.target)) wrapper.classList.remove('open');
    });

    wrapper.appendChild(dropdown);
    wrapper.appendChild(badge);
    document.body.appendChild(wrapper);
  }

  function renderFallback() {
    // versions.json unreachable — show static badge only
    const wrapper = document.createElement('div');
    wrapper.id = 'ver-picker';
    wrapper.innerHTML = `<div class="ver-badge">${currentVersion}</div>`;
    document.body.appendChild(wrapper);
  }
})();
