// Confirmation dialog box
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


// Drag and drop
const overlay = document.getElementById("global-drop-overlay");
const fileInput = document.getElementById("file");
const uploadForm = document.getElementById("upload-form");

let dragCounter = 0;

document.addEventListener("dragenter", (e) => {
    e.preventDefault();
    dragCounter++;
    overlay.classList.add("active");
});

document.addEventListener("dragover", (e) => {
    e.preventDefault();
});

document.addEventListener("dragleave", () => {
    dragCounter--;
    if (dragCounter === 0) {
        overlay.classList.remove("active");
    }
});

document.addEventListener("drop", (e) => {
    e.preventDefault();

    overlay.classList.remove("active");
    dragCounter = 0;

    const files = e.dataTransfer.files;

    if (files.length > 0) {
        fileInput.files = files;
        uploadForm.submit();
    }
});
