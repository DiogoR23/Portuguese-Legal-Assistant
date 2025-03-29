import React from 'react';
import { Outlet } from 'react-router-dom';
import ThemeToggle from '@/components/ThemeToggle';

const LayoutWithTheme = () => {
  return (
    <>
      <ThemeToggle />
      <Outlet />
    </>
  );
};

export default LayoutWithTheme;
