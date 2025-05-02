/*
PrivateRoute.jsx

This component checks if the user is authenticated before allowing access to certain routes.
If the user is authenticated, it renders the child components (Outlet).
If not, it redirects the user to the login page.
It uses the `useEffect` hook to make an API call to check authentication status.
It uses the `useState` hook to manage the authentication state.
It uses the `Navigate` component from react-router-dom to redirect the user.

It is important to note that this component should be used in conjunction with a router (e.g., BrowserRouter) and should be wrapped around the routes that require authentication.
This component is part of a larger application that uses React and react-router-dom for routing.

This component is responsible for protecting certain routes in the application.
*/

import { Navigate, Outlet } from 'react-router-dom';
import { useEffect, useState } from 'react';
import API from '@/services/axiosInstance';

const PrivateRoute = () => {
  const [authChecked, setAuthChecked] = useState(false);
  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await API.get('users/protected/');
        setIsValid(true);
      } catch (err) {
        console.error("Não autenticado:", err);
        setIsValid(false);
      } finally {
        setAuthChecked(true);
      }
    };

    checkAuth();
  }, []);

  if (!authChecked) return null;

  return isValid ? <Outlet /> : <Navigate to={"/login"} replace />
};

export default PrivateRoute;
