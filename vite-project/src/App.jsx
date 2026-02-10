import { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Detection from './components/Detection';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(true);

  if (!user) {
    return (
      <div className="auth-container">
        <div className="auth-box">
          <h1>Object Detection</h1>
          <p className="subtitle">Upload images to detect objects</p>
          
          <div className="tabs">
            <button 
              className={showLogin ? 'active' : ''} 
              onClick={() => setShowLogin(true)}
            >
              Login
            </button>
            <button 
              className={!showLogin ? 'active' : ''} 
              onClick={() => setShowLogin(false)}
            >
              Register
            </button>
          </div>

          {showLogin ? (
            <Login onSuccess={setUser} />
          ) : (
            <Register onSuccess={() => setShowLogin(true)} />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <nav className="navbar">
        <h2>Object Detection</h2>
        <div className="user-info">
          <span>{user.email}</span>
          <button onClick={() => setUser(null)}>Logout</button>
        </div>
      </nav>

      <div className="content">
        <Detection />
      </div>
    </div>
  );
}

export default App;