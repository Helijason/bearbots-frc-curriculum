// copyCode: copies the clean result payload (no line numbers, no removed lines).
function copyCode(btn){
  var win = btn.closest('.code-window');
  var code = win.getAttribute('data-code') || '';
  navigator.clipboard.writeText(code).then(function(){
    btn.textContent = 'Copied';
    btn.classList.add('copied');
    setTimeout(function(){ btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1200);
  });
}