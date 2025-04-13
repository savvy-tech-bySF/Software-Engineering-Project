import './App.css'
import Dashboard from './Components/Dashboard.jsx';
import ForgotPassword from './Components/ForgotPassword.jsx';
import Login from './Components/Login.jsx';
import HorizontalNavbar from './Components/HorizontalNavbar.jsx';
import Registration from './Components/Registration.jsx';
import FeedbackPage from './Components/FeedBack.jsx';
import { BrowserRouter, Route, Routes } from "react-router-dom";

function MyApp() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Registration />} />
        <Route path="/forgot" element={<ForgotPassword />} />
        
        {/* Protected routes with navbar */}
        <Route path="/dashboard" element={
          <>
            <HorizontalNavbar />
            <Dashboard />
          </>
        } />
        <Route path="/feedback" element={
          <>
            <HorizontalNavbar />
            <FeedbackPage />
          </>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default MyApp