import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({email: '', password: ''});
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Por favor preencha todos os campos obrigatórios.')
      return;
    }

    console.log('Login Válido!', formData)
  }

  return (
    <>
      <div className="min-h-screen flex">
        <div className="w-1/2 bg-[#dbe7df] dark:bg-[#1e2a22] flex justify-center items-center">
          
          <h1
            onClick={() => navigate('/')}
            className="text-green-900 dark:text-white text-4xl font-extrabold cursor-pointer hover:underline"
          >
            Amel.IA
          </h1>
        </div>

        <div className="w-1/2 bg-[#f4f4f4] dark:bg-[#1f1f1f] flex justify-center items-center">
          <div className="w-[80%] max-w-md">
            <h2 className="text-gray-900 dark:text-white text-2xl font-bold mb-2">Iniciar Sessão</h2>
            <p className="text-gray-800 dark:text-gray-400 mb-6">Bem-vindo ao teu assistente jurídico</p>

            <form className="space-y-4" onSubmit={handleSubmit}>
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 bg-white dark:bg-transparent border border-green-800 rounded-md text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              />
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-3 pr-12 bg-white dark:bg-transparent border border-green-800 rounded-md text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-green-800 dark:text-green-400"
                >
                {showPassword ? <EyeIcon className="h-5 w-5" /> : <EyeSlashIcon className="h-5 w-5" />}
                </button>
              </div>

              <div className="text-sm text-gray-800 dark:text-gray-400">
                Esqueceste-te da Password?{' '}
                <span
                  className="text-green-800 dark:text-green-400 underline cursor-pointer"
                  onClick={() => alert('Página de recuperação ainda não implementada')}
                >
                  Altera-a Aqui.
                </span>
              </div>

              {error && <p className='text-red-600 text-sm'>{error}</p>}

              <button
                type="submit"
                className="w-full bg-green-800 text-white py-3 rounded-md hover:bg-green-900 transition"
              >
                Entrar
              </button>
            </form>

            <div className="mt-6 text-sm text-gray-800 dark:text-gray-400">
              Caso não tenha conta,{' '}
              <span
                onClick={() => navigate('/register')}
                className="text-green-800 dark:text-green-400 underline cursor-pointer"
              >
                Regista-te Aqui.
              </span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginPage;
