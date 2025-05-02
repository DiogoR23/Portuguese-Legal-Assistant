/*
LoginPage.jsx

This component represents the login page of the application. It allows users to enter their email and password to access the system. The component also handles error display and toggling between showing and hiding the password.
It uses React hooks for state management and the Heroicons library for icons. The login functionality is handled by the `loginUser` function from the API services, which sends the login request to the backend. Upon successful login, the user is redirected to the chat page, and their tokens are stored in local storage for authentication purposes.
*/

import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '@/services/api';


const LoginPage = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Por favor preencha todos os campos obrigatórios.');
      return;
    }

    try {
      const response = await loginUser(formData);
      const { access_token, refresh_token, username } = response.data;
      localStorage.setItem('access', access_token);
      localStorage.setItem('refresh', refresh_token);
      localStorage.setItem('username', username);
      navigate("/chat");
    } catch (err) {
      const backendError = err.response?.data;

      if (backendError?.detail) {
        setError(backendError.detail);
      } else if (backendError?.non_field_errors) {
        setError(backendError.non_field_errors[0]);
      } else {
        setError('Erro ao fazer login. Verifica as credenciais.');
      }

      console.error('Erro no login:', backendError || err);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Lado esquerdo */}
      <div className="w-1/2 bg-[#01497C] flex justify-center items-center">
        <h1
          onClick={() => window.location.href = '/'}
          className="text-white text-4xl font-extrabold cursor-pointer hover:underline"
        >
          Amel.IA
        </h1>
      </div>

      {/* Lado direito */}
      <div className="w-1/2 bg-white dark:bg-[#242424] flex justify-center items-center">
        <div className="w-[80%] max-w-md">
          <h2 className="text-black dark:text-white text-2xl font-bold mb-2">Iniciar Sessão</h2>
          <p className="text-gray-700 dark:text-gray-400 mb-6">Bem-vindo ao teu assistente jurídico</p>

          <form className="space-y-4" onSubmit={handleSubmit}>
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-3 bg-gray-100 dark:bg-[#3d3d3d] border border-transparent rounded-md text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#01497C] focus:ring-offset-0"
            />

            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 pr-12 bg-gray-100 dark:bg-[#3d3d3d] border border-transparent rounded-md text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#01497C] focus:ring-offset-0"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-700 dark:text-white hover:text-gray-500 dark:hover:text-gray-300"
              >
                {showPassword ? <EyeIcon className="h-5 w-5" /> : <EyeSlashIcon className="h-5 w-5" />}
              </button>
            </div>

            <div className="text-sm text-gray-700 dark:text-gray-400">
              Esqueceste-te da Password?{' '}
              <span
                className="text-[#01497C] dark:text-blue-300 underline cursor-pointer"
                onClick={() => alert('Página de recuperação ainda não implementada')}
              >
                Altera-a Aqui.
              </span>
            </div>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <button
              type="submit"
              className="w-full bg-[#01497C] hover:bg-[#2A6F97] text-white py-3 rounded-md transition-colors"
            >
              Entrar
            </button>
          </form>

          <div className="mt-6 text-sm text-gray-700 dark:text-gray-400">
            Caso não tenha conta,{' '}
            <span
              onClick={() => navigate('/register')}
              className="text-[#01497C] dark:text-blue-300 underline cursor-pointer"
            >
              Regista-te Aqui.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
