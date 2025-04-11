import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '@/services/api';
import API from '@/services/axiosInstance';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('As palavras-passe não coincidem');
      return;
    }

    try {
        const response = await registerUser({
            username: formData.username,
            email: formData.email,
            password: formData.password,
            password2: formData.confirmPassword,
        });

        console.log('Registo bem-sucedido!', response.data);
        navigate('/login');
    } catch (err) {
        console.error('Erro no registo:', err);

        const errors = err?.response?.data;

        if (errors?.username) {
            setError('O nome de utilizador já existe.');
        } else if (errors?.email) {
            setError('O email já está registado.');
        }
        else if (errors?.password) {
            setError('A password não é válida.');
        } else if (errors?.non_field_errors) {
            setError('Erro: ', errors.non_field_errors[0]);
        } else {
            setError('Erro ao registar. Tente novamente.');
        }
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Lado Esquerdo */}
      <div className="w-1/2 bg-[#01497C] flex justify-center items-center">
        <h1
          onClick={() => navigate('/')}
          className="text-white text-4xl font-extrabold cursor-pointer hover:underline"
        >
          Amel.IA
        </h1>
      </div>

      {/* Lado Direito */}
      <div className="w-1/2 bg-white dark:bg-[#242424] flex justify-center items-center">
        <div className="w-[80%] max-w-md">
          <h2 className="text-black dark:text-white text-2xl font-bold mb-2">Criar Conta</h2>
          <p className="text-gray-700 dark:text-gray-400 mb-6">
            Regista-te para aceder ao assistente jurídico
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              name="username"
              placeholder="Nome de utilizador"
              value={formData.username}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-100 dark:bg-[#3d3d3d] border border-transparent rounded-md text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#01497C] focus:ring-offset-0"
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-100 dark:bg-[#3d3d3d] border border-transparent rounded-md text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#01497C] focus:ring-offset-0"
              required
            />
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 pr-12 bg-gray-100 dark:bg-[#3d3d3d] border border-transparent rounded-md text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#01497C] focus:ring-offset-0"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white"
              >
                {showPassword ? (
                  <EyeIcon className="h-5 w-5" />
                ) : (
                  <EyeSlashIcon className="h-5 w-5" />
                )}
              </button>
            </div>
            <input
              type={showPassword ? 'text' : 'password'}
              name="confirmPassword"
              placeholder="Confirmar Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-100 dark:bg-[#3d3d3d] border border-transparent rounded-md text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#01497C] focus:ring-offset-0"
              required
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}

            <button
              type="submit"
              className="w-full py-3 rounded-md transition-colors bg-[#01497C] text-white hover:bg-[#2A6F97]"
            >
              Registar
            </button>
          </form>

          <div className="mt-6 text-sm text-gray-700 dark:text-gray-400">
            Já tens conta?{' '}
            <span
              onClick={() => navigate('/login')}
              className="text-[#01497C] dark:text-blue-300 underline cursor-pointer"
            >
              Inicia Sessão
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
