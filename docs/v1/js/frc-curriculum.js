/* ============================================================
   FRC Programming Curriculum — Shared JavaScript
   ============================================================ */
 
/* ── Preview Mode ─────────────────────────────────────────── */
const PREVIEW_MODE = new URLSearchParams(location.search).has('preview');
function appendPreview(url) {
  return PREVIEW_MODE && !url.includes('preview=true') ? url + '?preview=true' : url;
}

   /* ── Page Population ──────────────────────────────────────── */
function initPage() {
  const lessonId = document.body.dataset.lesson;
  const lesson   = lessonId && SITE_CONFIG.lessons ? SITE_CONFIG.lessons[lessonId] : null;
 
  // WIP
  if (SITE_CONFIG.workInProgress) {
    document.body.classList.add('wip');
    const banner = document.querySelector('.wip-banner');
    if (banner) banner.textContent = SITE_CONFIG.banner;
  }

  // Build header/footer contents from config
  function buildNavBar(el) {
    const logo = document.createElement('a');
    logo.className = 'logo';
    logo.href = appendPreview('index.html');
    logo.textContent = SITE_CONFIG.siteName;
    if (SITE_CONFIG.workInProgress) {
      const badge = document.createElement('span');
      badge.className = 'wip-badge';
      badge.textContent = SITE_CONFIG.wipBadgeText;
      logo.appendChild(badge);
    }
    const label = document.createElement('span');
    label.className = 'lesson-label';
    const nav = document.createElement('nav');
    nav.className = 'site-nav';
    el.appendChild(logo);
    el.appendChild(label);
    el.appendChild(nav);
  }

  const header = document.querySelector('header.site-header');
  if (header) buildNavBar(header);

  const footer = document.querySelector('footer.site-footer');
  if (footer) buildNavBar(footer);
 
  // Page <title>
  if (lesson) {
    document.title = `Lesson ${lesson.lesson} — ${lesson.title} | ${SITE_CONFIG.siteName}`;
  } else {
    document.title = SITE_CONFIG.siteName;
  }

  // Index page — populate module cards
  document.querySelectorAll('.module-card').forEach(card => {
    const l = SITE_CONFIG.lessons[card.dataset.lesson];
    if (!l) return;

    card.href = appendPreview(l.filename);

    const badgeMap = {
      ready:   { label: "Ready",   cls: "badge-ready" },
      current: { label: "Current", cls: "badge-current" },
      review:  { label: "Review", cls: "badge-review" },
      soon:    { label: "Soon",    cls: "badge-soon" }
    };
    const badge = card.querySelector('.card-badge');
    if (badge && l.status) {
      const b = badgeMap[l.status];
      badge.textContent = b.label;
      badge.className = `card-badge ${b.cls}`;
    }

    // Lock soon cards unless preview mode
    if (l.status === 'soon' && !PREVIEW_MODE) {
      card.href = '#';
      card.classList.add('coming-soon');
    }
    
    const h3 = document.createElement('h3');
    h3.textContent = `Lesson ${l.lesson} - ${l.title}`;
    card.appendChild(h3);

    const p = document.createElement('p');
    p.textContent = l.description;
    card.appendChild(p);

    const meta = document.createElement('div');
    meta.className = 'card-meta';
    meta.textContent = `${l.hardware} · ${l.duration}`;
    card.appendChild(meta);
  });

  const hero = document.querySelector('.course-hero');
  if (hero) {
    const h1 = hero.querySelector('h1');
    const p = hero.querySelector('p');
    if (h1) h1.textContent = SITE_CONFIG.siteName;
    if (p) p.textContent = SITE_CONFIG.siteSubtitle;
  }
 
  if (!lesson) return;

  // Inject next lesson title into any .next-lesson-ref spans
  if (lesson.next) {
    const n = SITE_CONFIG.lessons[lesson.next];
    document.querySelectorAll('.next-lesson-ref').forEach(el => {
      el.textContent = `Lesson ${n.lesson} — "${n.title}"`;
    });
  }

  // Inject cross-lesson references
    document.querySelectorAll('.lesson-ref').forEach(el => {
      const id = el.dataset.lesson;
      const l = SITE_CONFIG.lessons[id];
      if (l) el.textContent = `Lesson ${l.lesson} — ${l.title}`;
    });

  const labelText = `Module ${lesson.module} - Lesson ${lesson.lesson}`;
 
  // lesson-label (header + footer)
  document.querySelectorAll('.lesson-label').forEach(el => el.textContent = labelText);
 
  // lesson-meta
  document.querySelectorAll('.lesson-meta').forEach(el => el.textContent = labelText);
 
  // lesson-title
  document.querySelectorAll('.lesson-title').forEach(el => el.textContent = lesson.title);
 
  // lesson-subtitle
  document.querySelectorAll('.lesson-subtitle').forEach(el => el.textContent = lesson.subtitle);
 
  // lesson-info-bar
  document.querySelectorAll('.lesson-info-bar').forEach(bar => {
    bar.innerHTML = '';
    const items = [
      { text: lesson.duration, label: 'Duration' },
      { text: lesson.hardware, label: 'Hardware:' },
      { text: lesson.prereq, label: 'Prereq:' },
      { text: lesson.tools, label: 'Tools:' }
    ];
    items.forEach(({ text, label }) => {
      if (!text) return;
      const div = document.createElement('div');
      div.className = 'info-item';
      div.innerHTML = '<div class="info-dot"></div>';
      if (label) {
        const strong = document.createElement('strong');
        strong.textContent = ' ' + label + ' ';
        div.appendChild(strong);
        div.appendChild(document.createTextNode(text));
      } else {
        div.appendChild(document.createTextNode(' ' + text));
      }
      bar.appendChild(div);
    });
  });

  // prev/next nav links — all .site-nav elements (header + footer)
  document.querySelectorAll('.site-nav').forEach(nav => {
    nav.innerHTML = `<a href="${appendPreview('index.html')}">All lessons</a>`;
 
    if (lesson.prev) {
      const p = SITE_CONFIG.lessons[lesson.prev];
      const a = document.createElement('a');
      if (p.status === 'soon' && !PREVIEW_MODE) {
        a.href = '#';
        a.classList.add('nav-locked');
        a.title = 'Not yet available';
      } else {
        a.href = appendPreview(p.filename);
      }
      a.innerHTML = `&larr; Lesson ${p.lesson}`;
      nav.insertBefore(a, nav.firstChild);
    }
 
    if (lesson.next) {
      const n = SITE_CONFIG.lessons[lesson.next];
      const a = document.createElement('a');

      if (n.status === 'soon' && !PREVIEW_MODE) {
        a.href = '#';
        a.classList.add('nav-locked');
        a.title = 'Not yet available';
      } else {
        a.href = appendPreview(n.filename);
      }
      a.innerHTML = `Lesson ${n.lesson} &rarr;`;
      nav.appendChild(a);
    }
  });
}
 
/* ── Section Navigation ───────────────────────────────────── */
function initSectionNav() {
  const btns = document.querySelectorAll('.section-nav-btn');
  const sections = document.querySelectorAll('.lesson-section');
 
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.section;
      btns.forEach(b => b.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));
      // Activate matching button in both top and bottom navs
      document.querySelectorAll(`.section-nav-btn[data-section="${target}"]`)
        .forEach(b => b.classList.add('active'));
      const targetSection = document.getElementById('section-' + target);
      if (targetSection) targetSection.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
}
 
/* ── Tier Challenge Tabs ──────────────────────────────────── */
function initTierTabs() {
  document.querySelectorAll('.tier-tabs').forEach(tabGroup => {
    const tabs = tabGroup.querySelectorAll('.tier-tab');
    const panelContainer = tabGroup.nextElementSibling;
    if (!panelContainer) return;
 
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const tier = tab.dataset.tier;
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        panelContainer.querySelectorAll('.tier-panel').forEach(p => p.classList.remove('active'));
        const panel = panelContainer.querySelector('.tier-panel.' + tier);
        if (panel) panel.classList.add('active');
      });
    });
  });
}
 
/* ── Toggle Hints and Answers ─────────────────────────────── */
function initToggles() {
  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      const target = document.getElementById(targetId);
      if (!target) return;
      const isOpen = target.style.display === 'block';
      target.style.display = isOpen ? 'none' : 'block';
      btn.textContent = isOpen ? btn.dataset.closed : btn.dataset.open;
    });
  });
}

/* ── Swap Toggles ─────────────────────────────────────────── */
function initSwapToggles() {
  document.querySelectorAll('.swap-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const showId = btn.dataset.show;
      const hideId = btn.dataset.hide;
      const showEl = document.getElementById(showId);
      const hideEl = document.getElementById(hideId);
      const isSwapped = btn.dataset.swapped === 'true';

      if (!isSwapped) {
        if (hideEl) hideEl.style.display = 'none';
        if (showEl) showEl.style.display = 'block';
        btn.textContent = btn.dataset.labelBack;
        btn.dataset.swapped = 'true';
      } else {
        if (showEl) showEl.style.display = 'none';
        if (hideEl) hideEl.style.display = 'block';
        btn.textContent = btn.dataset.labelSwap;
        btn.dataset.swapped = 'false';
      }
    });
  });
}

/* ── Quiz Buttons ─────────────────────────────────────────── */
function initQuiz() {
  document.querySelectorAll('.quiz-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const quizId = btn.dataset.quiz;
      const correct = btn.dataset.correct === 'true';
      const feedbackEl = document.getElementById('quiz-feedback-' + quizId);
 
      document.querySelectorAll(`.quiz-btn[data-quiz="${quizId}"]`).forEach(b => {
        b.classList.remove('correct', 'wrong');
      });
 
      btn.classList.add(correct ? 'correct' : 'wrong');
 
      if (feedbackEl) {
        feedbackEl.textContent = correct
          ? btn.dataset.feedbackCorrect || 'Correct!'
          : btn.dataset.feedbackWrong || 'Not quite — try again.';
      }
    });
  });
}
 
/* ── Broken Robot Lab ─────────────────────────────────────── */
function initBugLab() {
  document.querySelectorAll('.bug-lab').forEach(lab => {
    const labId = lab.dataset.lab;
    const bugLines = lab.querySelectorAll('.bug-line');
    const dots = lab.querySelectorAll('.bug-dot');
    const progressLabel = lab.querySelector('.bug-progress-count');
    const successBanner = lab.querySelector('.success-banner');
    let foundCount = 0;
    const totalBugs = bugLines.length;
 
    bugLines.forEach(line => {
      line.querySelector('.line-code').addEventListener('click', () => {
        if (line.classList.contains('found')) return;
 
        const bugNum = line.dataset.bug;
        const reveal = lab.querySelector(`.bug-reveal[data-bug="${bugNum}"]`);
 
        line.classList.add('found');
        if (reveal) reveal.style.display = 'block';
 
        foundCount++;
        if (dots[foundCount - 1]) dots[foundCount - 1].classList.add('found');
        if (progressLabel) progressLabel.textContent = foundCount + ' / ' + totalBugs;
 
        setTimeout(() => {
          line.classList.add('fixed');
          if (dots[foundCount - 1]) dots[foundCount - 1].classList.add('fixed');
        }, 700);
 
        if (foundCount === totalBugs && successBanner) {
          setTimeout(() => { successBanner.style.display = 'block'; }, 900);
        }
      });
    });
  });
}
 
/* ── Init All ─────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initPage();
  initSectionNav();
  initTierTabs();
  initToggles();
  initSwapToggles();
  initQuiz();
  initBugLab();
});