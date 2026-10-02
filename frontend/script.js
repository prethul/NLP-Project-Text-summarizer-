const input = document.getElementById('textInput');
const counter = document.getElementById('counter');
const clearBtn = document.getElementById('clearBtn');
const summarizeBtn = document.getElementById('summarizeBtn');
const copyBtn = document.getElementById('copyBtn');
const emptyState = document.getElementById('emptyState');
const summaryContent = document.getElementById('summaryContent');
const outputMeta = document.getElementById('outputMeta');
const summaryWords = document.getElementById('summaryWords');

function updateCounter() {
  const text = input.value;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  counter.textContent = `${text.length.toLocaleString()} characters · ${words.toLocaleString()} words`;
}

input.addEventListener('input', updateCounter);
clearBtn.addEventListener('click', () => {
  input.value = '';
  updateCounter();
  summaryContent.hidden = true;
  outputMeta.hidden = true;
  emptyState.hidden = false;
  copyBtn.disabled = true;
  input.focus();
});

summarizeBtn.addEventListener('click', async () => {
  const text = input.value.trim();
  if (!text) { input.focus(); return; }
  summarizeBtn.disabled = true;
  summarizeBtn.classList.add('loading');
  summarizeBtn.querySelector('.btn-label').textContent = 'Summarizing';
  try {
    const response = await fetch('/api/summarize', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Unable to summarize this text.');
    summaryContent.textContent = data.summary;
    summaryContent.hidden = false;
    emptyState.hidden = true;
    outputMeta.hidden = false;
    copyBtn.disabled = false;
    summaryWords.textContent = `${data.summary.trim().split(/\s+/).length} words`;
    document.getElementById('outputPanel').scrollIntoView({behavior:'smooth', block:'nearest'});
  } catch (error) {
    alert(error.message);
  } finally {
    summarizeBtn.disabled = false;
    summarizeBtn.classList.remove('loading');
    summarizeBtn.querySelector('.btn-label').textContent = 'Summarize text';
  }
});

copyBtn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(summaryContent.textContent);
  const original = copyBtn.innerHTML;
  copyBtn.innerHTML = 'Copied <span>✓</span>';
  setTimeout(() => { copyBtn.innerHTML = original; }, 1400);
});

updateCounter();
