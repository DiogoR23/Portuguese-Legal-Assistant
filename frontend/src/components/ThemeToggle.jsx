import React, { useEffect, useState } from 'react';
import { MoonIcon, SunIcon } from '@heroicons/react/24/solid';

const ThemeToggle = ({ floating = false }) => {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark' ||
      (!localStorage.getItem('theme') &&
        window.matchMedia('(prefers-color-scheme: dark)').matches);
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const toggleTheme = () => setDarkMode(!darkMode);

  return (
    <button
      onClick={toggleTheme}
      className={`relative inline-flex h-[20px] w-[36px] items-center rounded-full transition-colors
        ${darkMode ? 'bg-[#01497C]' : 'bg-gray-300'} 
        ${floating ? 'fixed top-4 right-4 z-50' : ''}`}
      aria-label="Alternar tema"
    >
      <span
        className={`inline-block h-[16px] w-[16px] transform rounded-full transition-transform 
          ${darkMode ? 'translate-x-[16px] bg-white' : 'translate-x-[4px] bg-gray-800'}`}
      >
        {darkMode ? (
          <MoonIcon className="h-3.5 w-3.5 text-[#01497C] mx-auto mt-[1px]" />
        ) : (
          <SunIcon className="h-3.5 w-3.5 text-white mx-auto mt-[1px]" />
        )}
      </span>
    </button>
  );
};

export default ThemeToggle;
