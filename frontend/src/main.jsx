import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App'
import AuthPage from './pages/AuthPage';
import ChatPage from './pages/ChatPage';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<AuthPage />} />
        <Route path='/chat' element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)

