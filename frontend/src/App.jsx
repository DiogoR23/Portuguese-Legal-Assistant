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