const API_URL = 'http://localhost:8000';

export const api = {
  async register(email, password) {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    return res.json();
  },

  async login(email, password) {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async detectImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const res = await fetch(`${API_URL}/detect`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      throw new Error('Detection failed');
    }
    return res.json();
  },

  getImageUrl(path) {
    return `${API_URL}/${path}`;
  }
};