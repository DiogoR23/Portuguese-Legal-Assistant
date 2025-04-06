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
    <Router>
      <Routes>
        <Routes element={<LayoutWithTheme showFloatingToggle={true} />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/chat" element={<PrivateRoute><ChatPage /></PrivateRoute>} />
      </Routes>
    </Router>
  );
}

export default App;