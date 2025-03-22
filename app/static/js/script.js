document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const html = document.documentElement;

    toggleButton.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        html.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');

        toggleButton.innerHTML = currentTheme === 'dark' ?
            '<i class="fa-solid fa-moon"></i>' :
            '<i class="fa-solid fa-sun"></i>';
    });
});
