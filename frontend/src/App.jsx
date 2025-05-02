/*
App.jsx

This file contains the main application component for the chat application.
It sets up the routing for the application using React Router.
It includes public routes for the home, register, and login pages, and a private route for the chat page.
The private route is protected by the PrivateRoute component, which checks if the user is authenticated before allowing access to the chat page.
The application uses a layout component (LayoutWithTheme) to provide a consistent look and feel across all pages.
The application is built using React and React Router.
The application is structured to sperate public and private routes.
The public routes are accessible to all users, while the Private routes are only accessible to authenticated users.
*/

import React from "react";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute";
import ChatPage from "./pages/ChatPage";
import LayoutWithTheme from "./layouts/LayoutWithTheme";

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route element={<LayoutWithTheme />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Route>
      {/* Private Route */}
      <Route element={<PrivateRoute />}>
        <Route element={<LayoutWithTheme />}>
          <Route path="/chat" element={<ChatPage />} />
        </Route>
      </Route>
    </Routes>
  )
}


export default App;