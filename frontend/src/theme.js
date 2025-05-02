/*
theme.js

This file is responsible for setting the theme of the application based on the user's preference.
It checks the local storage for a saved theme and applies it. If no theme is saved, it checks the user's system preference for dark mode.
If the user prefers dark mode, it applies the dark theme. Otherwise, it applies the light theme.
The theme is applied by adding the 'dark' class to the document's root element.
The 'dark' class is used in the CSS to apply dark mode styles.
*/

(function () {
    const theme = localStorage.getItem('theme');

    if (
        theme == 'dark' ||
        (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
})();