import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import ThemeToggle from '@/components/ThemeToggle';
import { useNavigate } from 'react-router-dom';


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

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
        setError('As palavras-passe não coincidem');
        return;
        }

        console.log('Registo válido!', formData);
    };

    return (
        <>
        <div className="min-h-screen flex">
            {/* Lado esquerdo */}
            <div className="w-1/2 bg-[#dbe7df] dark:bg-[#1e2a22] flex justify-center items-center">
            <h1
                onClick={() => navigate('/')}
                className="text-green-900 dark:text-white text-4xl font-extrabold cursor-pointer hover:underline"
            >
                Amel.IA
            </h1>
            </div>

            {/* Lado direito */}
            <div className="w-1/2 bg-[#f4f4f4] dark:bg-[#1f1f1f] flex justify-center items-center">
            <div className="w-[80%] max-w-md">
                <h2 className="text-gray-900 dark:text-white text-2xl font-bold mb-2">Criar Conta</h2>
                <p className="text-gray-800 dark:text-gray-400 mb-6">Regista-te para aceder ao assistente jurídico</p>

                <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="text"
                    name="username"
                    placeholder="Nome de utilizador"
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-white dark:bg-transparent border border-green-800 rounded-md text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                    required
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-white dark:bg-transparent border border-green-800 rounded-md text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                    required
                />

                {/* Password */}
                <div className="relative">
                    <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-4 py-3 pr-12 bg-white dark:bg-transparent border border-green-800 rounded-md text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                    required
                    />
                    <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-green-800 dark:text-green-400"
                    >
                    {showPassword ? <EyeIcon className="h-5 w-5" /> : <EyeSlashIcon className="h-5 w-5" />}
                    </button>
                </div>

                {/* Confirmar Password */}
                <input
                    type={showPassword ? 'text' : 'password'}
                    name="confirmPassword"
                    placeholder="Confirmar Password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-white dark:bg-transparent border border-green-800 rounded-md text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                    required
                />

                {error && <p className="text-red-600 text-sm">{error}</p>}

                <button
                    type="submit"
                    className="w-full bg-green-800 text-white py-3 rounded-md hover:bg-green-900 transition"
                >
                    Registar
                </button>
                </form>

                <div className="mt-6 text-sm text-gray-800 dark:text-gray-400">
                    Já tens conta?{' '}
                    <span
                        onClick={() => navigate('/login')}
                        className="text-green-800 dark:text-green-400 underline cursor-pointer"
                    >
                        Inicia Sessão
                    </span>
                </div>
            </div>
            </div>
        </div>
        </>
    );
};

export default RegisterPage;
