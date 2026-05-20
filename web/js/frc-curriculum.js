/* ============================================================
   FRC Programming Curriculum — Shared JavaScript
   ============================================================ */
 
/* ── Page Population ──────────────────────────────────────── */
function initPage() {
  const lessonId = document.body.dataset.lesson;
  const lesson   = lessonId && SITE_CONFIG.lessons ? SITE_CONFIG.lessons[lessonId] : null;
 
  // WIP
  if (SITE_CONFIG.workInProgress) document.body.classList.add('wip');
 
  // Site name — all .logo elements (header + footer)
  document.querySelectorAll('.logo').forEach(el => {
    const badge = el.querySelector('.wip-badge');
    el.textContent = SITE_CONFIG.siteName;
    if (badge) el.appendChild(badge);
  });
 
  // Page <title>
  if (lesson) {
    document.title = `Lesson ${lesson.lesson} — ${lesson.title} | ${SITE_CONFIG.siteName}`;
  } else {
    document.title = SITE_CONFIG.siteName;
  }
 
  if (!lesson) return;
 
  const labelText = `Module ${lesson.module} - Lesson ${lesson.lesson}`;
 
  // lesson-label (header + footer)
  document.querySelectorAll('.lesson-label').forEach(el => el.textContent = labelText);
 
  // lesson-meta
  document.querySelectorAll('.lesson-meta').forEach(el => el.textContent = labelText);
 
  // lesson-title
  document.querySelectorAll('.lesson-title').forEach(el => el.textContent = lesson.title);
 
  // lesson-subtitle
  document.querySelectorAll('.lesson-subtitle').forEach(el => el.textContent = lesson.subtitle);
 
  // prev/next nav links — all .site-nav elements (header + footer)
  document.querySelectorAll('.site-nav').forEach(nav => {
    nav.innerHTML = '<a href="index.html">All lessons</a>';
 
    if (lesson.prev) {
      const p = SITE_CONFIG.lessons[lesson.prev];
      const a = document.createElement('a');
      a.href = p.filename;
      a.innerHTML = `&larr; Lesson ${p.lesson}`;
      nav.insertBefore(a, nav.firstChild);
    }
 
    if (lesson.next) {
      const n = SITE_CONFIG.lessons[lesson.next];
      const a = document.createElement('a');
      a.href = n.filename;
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
  initQuiz();
  initBugLab();
});