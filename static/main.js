const modal = document.getElementById('custom-modal');
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
window.onclick = (e) => { if (e.target === modal) closeModal(); };

document.getElementById('modal-confirm').onclick = async () => {
    if (!formToSubmit) return;

    try {
        const response = await fetch('/delete', {
            method: 'POST',
            body: new FormData(formToSubmit)
        });
        
        if (response.ok) location.reload();
        else alert('Server error');
    } catch (err) {
        alert('Network error');
    }
    closeModal();
};