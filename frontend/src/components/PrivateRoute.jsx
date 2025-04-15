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
