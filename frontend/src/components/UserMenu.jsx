import React, { useState, useEffect, useRef } from 'react';
import { Bars3Icon } from '@heroicons/react/24/solid';
import ThemeToggle from './ThemeToggle';
import { useNavigate } from 'react-router-dom';

const UserMenu = () => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [username, setUsername] = useState('');
  const menuRef = useRef();

  useEffect(() => {
    const storedUser = localStorage.getItem('username');
    if (storedUser) setUsername(storedUser);

    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('username');
    navigate('/');
  };

  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      <button onClick={() => setIsOpen(!isOpen)} className="bg-gray-300 dark:bg-gray-700 p-2 rounded-full">
        <Bars3Icon className="h-5 w-5 text-black dark:text-white" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 origin-top-right bg-white dark:bg-[#2a2a2a] border border-gray-300 dark:border-gray-700 rounded-md shadow-lg z-50">
          <div className="px-4 py-3 text-sm font-semibold text-gray-700 dark:text-white border-b dark:border-gray-600">
            {username || 'Utilizador'}
          </div>
          <div className="p-2">
            <ThemeToggle />
          </div>
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-100 dark:hover:bg-red-700 dark:text-red-400 rounded-md"
          >
            Terminar Sessão
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
