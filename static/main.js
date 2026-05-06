// Theme toggle
const DARK_ICON  = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
const LIGHT_ICON = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z"/></svg>`;

let dark = localStorage.getItem('theme') === 'dark';
const themeBtn = document.getElementById('theme-btn');

function applyTheme() {
  document.body.setAttribute('data-theme', dark ? 'dark' : '');
  themeBtn.innerHTML = dark ? DARK_ICON : LIGHT_ICON;
  localStorage.setItem('theme', dark ? 'dark' : 'light');
}

function toggleTheme() { dark = !dark; applyTheme(); }

applyTheme();

// Auto-submit when file picked via label
document.getElementById('file-input').addEventListener('change', () => {
  document.getElementById('upload-form').submit();
});

// Delete confirmation modal
const modal = document.getElementById('modal');
let formToSubmit = null;

document.addEventListener('submit', (e) => {
  if (e.target.classList.contains('delete-form')) {
    e.preventDefault();
    formToSubmit = e.target;
    modal.style.display = 'flex';
  }
});

const closeModal = () => { modal.style.display = 'none'; formToSubmit = null; };
document.getElementById('modal-cancel').onclick = closeModal;
window.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

document.getElementById('modal-confirm').onclick = async () => {
  if (!formToSubmit) return;
  closeModal();
  try {
    const res = await fetch('/delete', { method: 'POST', body: new FormData(formToSubmit) });
    if (res.ok) location.reload();
    else alert('Server error while deleting');
  } catch {
    alert('Network error');
  }
};

// Drag & drop upload
const overlay = document.getElementById('drop-overlay');
const fileInput = document.getElementById('file-input');
const uploadForm = document.getElementById('upload-form');
let dragCounter = 0;

document.addEventListener('dragenter', (e) => { e.preventDefault(); dragCounter++; overlay.classList.add('active'); });
document.addEventListener('dragover',  (e) => { e.preventDefault(); });
document.addEventListener('dragleave', ()  => { if (--dragCounter === 0) overlay.classList.remove('active'); });
document.addEventListener('drop', (e) => {
  e.preventDefault();
  overlay.classList.remove('active');
  dragCounter = 0;
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    uploadForm.submit();
  }
});