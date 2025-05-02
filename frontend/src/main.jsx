/*
main.jsx

This file is the entry point for the React application. It renders the App component inside a BrowserRouter, which enables routing in the application.
It import React, ReactDOM, and the BrowserRouter from react-router-dom. The App component is imported from the App.js file.
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);