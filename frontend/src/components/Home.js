import React, { useEffect, useState } from "react";
import api from "../services/api"; // Importez votre service API
import "./Home.css"; // Styles CSS pour le composant

const Home = () => {
  const [data, setData] = useState({ temperature: null, humidity: null });

  // Fonction pour récupérer les données
  const fetchData = async () => {
    try {
      const response = await api.get("/api/dht11/"); // Remplacez par l'URL de votre endpoint
      const latestData = response.data[response.data.length - 1]; // Dernière donnée
      setData({
        temperature: latestData.temp,
        humidity: latestData.humidity,
      });
    } catch (error) {
      console.error("Erreur lors de la récupération des données :", error);
    }
  };

  // Appeler fetchData au montage du composant et toutes les 5 secondes
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Met à jour toutes les 5 secondes
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      {/* Menu à gauche */}
      <div className="sidebar">
        <h1>TEMP&HUMD</h1>
        <button className="menu-button">Login</button>
        <button className="menu-button">Logout</button>
      </div>

      {/* Contenu principal */}
      <div className="content">
        <div className="chart-container">
          <div className="chart-card">
            <h3>Temperature</h3>
            <div className="chart">
              <p>
                {data.temperature !== null
                  ? `${data.temperature}°C`
                  : "Loading..."}
              </p>
            </div>
          </div>
          <div className="chart-card">
            <h3>Humidity</h3>
            <div className="chart">
              <p>
                {data.humidity !== null
                  ? `${data.humidity}%`
                  : "Loading..."}
              </p>
            </div>
          </div>
        </div>
        <div className="data-display">
          <div className="data-card">
            <h3>Temperature</h3>
            <p>
              {data.temperature !== null
                ? `${data.temperature}`
                : "Loading..."}
            </p>
          </div>
          <div className="data-card">
            <h3>Humidity</h3>
            <p>
              {data.humidity !== null
                ? `${data.humidity}`
                : "Loading..."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
