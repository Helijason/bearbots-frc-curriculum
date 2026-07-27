/* ── Step builder ─────────────────────────────────────────── */
function sbToggle(id) {
  const step = document.getElementById(id);
  if (!step) return;
  step.classList.toggle('open');
}
