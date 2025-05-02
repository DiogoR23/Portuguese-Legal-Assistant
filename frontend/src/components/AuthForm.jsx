/*
AuthForm.jsx


This component is responsible for rendering the authentication form (login or register) and managing the form state, including validation and sending data to the API.

It uses the `useState` hook to manage the form data, loading state, and error messages. The `handleChange` function updates the form data as the user types, while the `handleSubmit` function handles form submission, including API calls for login and registration.
It also handles the response from the API, storing the access and refresh tokens in local storage upon successful authentication. The component conditionally renders the form fields based on whether the user is logging in or registering.
This file is part of the Chat Application project.
*/


import React, { useState } from 'react';
import { loginUser, registerUser } from '../services/api';

const AuthForm = ({ isLogin }) => {
  const [formData, setFormData] = useState({ email: '', username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const response = await loginUser({ email: formData.email, password: formData.password });
        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
      } else {
        await registerUser(formData);
        const response = await loginUser({ email: formData.email, password: formData.password });
        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
      }
      window.location.href = '/chat';
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao autenticar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {!isLogin && (
        <input
          type="text"
          name="username"
          placeholder="Nome de utilizador"
          value={formData.username}
          onChange={handleChange}
          className="w-full px-4 py-2 border rounded bg-gray-50 dark:bg-gray-700 dark:text-white"
          required
        />
      )}
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        className="w-full px-4 py-2 border rounded bg-gray-50 dark:bg-gray-700 dark:text-white"
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Palavra-passe"
        value={formData.password}
        onChange={handleChange}
        className="w-full px-4 py-2 border rounded bg-gray-50 dark:bg-gray-700 dark:text-white"
        required
      />
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded transition"
        disabled={loading}
      >
        {loading ? 'A carregar...' : isLogin ? 'Entrar' : 'Registar'}
      </button>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
};

export default AuthForm;
