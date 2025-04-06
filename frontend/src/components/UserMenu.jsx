import React, { useState, useEffect, useRef } from 'react';
import { UserCircleIcon, ArrowRightStartOnRectangleIcon, HomeIcon } from '@heroicons/react/24/solid';
import ThemeToggle from './ThemeToggle';
import { useNavigate } from 'react-router-dom';

const UserMenu = ({ onLogout }) => {
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
    if (onLogout) onLogout();
    navigate('/');
  };

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-1 rounded-full hover:opacity-80 transition"
      >
        <UserCircleIcon className="h-9 w-9 text-gray-800 dark:text-white" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-[#2a2a2a] border border-gray-300 dark:border-gray-700 rounded-md shadow-lg z-50">
          <div className="px-4 py-3 text-sm font-semibold text-gray-700 dark:text-white border-b dark:border-gray-600">
            {username || 'Utilizador'}
          </div>

          <button
            onClick={() => navigate('/')}  
            className='w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700'
            title='Página Inicial'
          >
            <HomeIcon className="h-5 w-5 inline-block mr-2" />
            Página Inicial
          </button>
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-100 dark:hover:bg-red-700 dark:text-red-400"
          >
            <ArrowRightStartOnRectangleIcon className="h-5 w-5 inline-block mr-2" />
            Terminar Sessão
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
