/*
LayoutWithTheme.jsx

This component serves as a layout wrapper for the application.
It uses React Router's Outlet to render child routes.
It can be used to apply a consistent theme or layout structure across different pages.
It is a placeholder for now, but can be extended in the future to include theme providers or other layout components.
*/

import { Outlet } from 'react-router-dom';

const LayoutWithTheme = () => {
  return <Outlet />;
};

export default LayoutWithTheme;