/*
ConversationItemMenu.jsx

This component renders a context menu for conversation items.
It includes options to rename or delete the conversation.
It uses the Heroicons library for icons and React hooks for managing state and effects.
It listens for clicks outside the menu to close it.
Props:
- top: The top position of the menu.
- left: The left position of the menu.
- onRename: Function to call when the rename option is clicked.
- onDelete: Function to call whenr the delete option is clicked.
- closeMenu: Function to call to close the menu.
*/

import React, { useEffect, useRef } from 'react';
import { TrashIcon, PencilSquareIcon } from '@heroicons/react/24/outline';

const ConversationItemMenu = ({ top, left, onRename, onDelete, closeMenu }) => {
  const menuRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        closeMenu();
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [closeMenu]);

  return (
    <div
      ref={menuRef}
      className="fixed z-50 w-44 bg-white dark:bg-[#2a2a2a] border border-gray-300 dark:border-gray-700 rounded-md shadow-lg"
      style={{ top: `${top}px`, left: `${left}px` }}
    >
      <button
        onClick={onRename}
        className="w-full flex items-center gap-2 px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700"
      >
        <PencilSquareIcon className="h-5 w-5 inline-block mr-2" />
        Mudar Nome
      </button>
      <button
        onClick={onDelete}
        className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-red-500/20"
      >
        <TrashIcon className="h-5 w-5 inline-block mr-2" />
        Eliminar
      </button>
    </div>
  );
};

export default ConversationItemMenu;
