import axios from 'axios';

// Définissez l'URL de base pour l'API
const api = axios.create({
  baseURL: 'http://localhost:8000/api/json', // Remplacez par l'URL de votre backend Django
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
