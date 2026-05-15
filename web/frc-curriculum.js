/* ============================================================
   FRC Programming Curriculum — Shared JavaScript
   ============================================================ */

/* ── Section Navigation ───────────────────────────────────── */
function initSectionNav() {
  const btns = document.querySelectorAll('.section-nav-btn');
  const sections = document.querySelectorAll('.lesson-section');

  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.section;
      btns.forEach(b => b.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));
      btn.classList.add('active');
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
  initSectionNav();
  initTierTabs();
  initToggles();
  initQuiz();
  initBugLab();
});
