function wrapText(textareaId, prefix, suffix) {
    const textarea = document.getElementById(textareaId);
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);

    textarea.value = text.slice(0, start) + prefix + selectedText + suffix + text.slice(end);
    textarea.focus();
    textarea.setSelectionRange(start + prefix.length, end + prefix.length);
}

function toggleEmojiPicker() {
    const picker = document.getElementById('emoji-picker');
    picker.style.display = picker.style.display === 'none' || picker.style.display === '' ? 'block' : 'none';
}

function showCategory(category) {
    const categories = document.querySelectorAll('.emoji-category');
    categories.forEach(cat => {
        cat.classList.remove('active');
        if (cat.id === category) {
            cat.classList.add('active');
        }
    });
}

function insertEmoji(emoji) {
    const textarea = document.getElementById('message');
    textarea.value += emoji;
    toggleEmojiPicker();  // Fecha o emoji picker após a seleção
}

// Oculta o emoji picker se o usuário clicar fora dele
document.addEventListener('click', function(event) {
    const picker = document.getElementById('emoji-picker');
    const button = event.target.closest('button');
    if (!picker.contains(event.target) && (!button || !button.classList.contains('btn-outline-secondary'))) {
        picker.style.display = 'none';
    }
});