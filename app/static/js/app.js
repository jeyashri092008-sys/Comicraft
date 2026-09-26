function handlePdfDownload(path) {
    setTimeout(() => { window.location.href = `/export-success?pdf_path=${encodeURIComponent(path)}`; }, 1000);
}
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("comicForm");
    const btn = document.getElementById("generateBtn");
    if (form && btn) {
        form.addEventListener("submit", () => {
            btn.disabled = true;
            btn.innerText = "Generating Comic (please wait)...";
        });
    }
});
