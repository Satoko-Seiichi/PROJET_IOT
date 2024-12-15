import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <div className="hero-section">
        <h1 className="hero-title">IoT Temperature Monitoring</h1>
        <p className="hero-description">
        Cette application vous permet de surveiller la température et l'humidité
        collectées par le capteur DHT11 en temps réel. Vous pouvez également
        saisir des données manuellement et les visualiser instantanément.
        Pour utiliser le capteur DHT11, connectez-le correctement à votre ESP8266,
        et assurez-vous que l'API fonctionne pour récupérer les données.
      <div className="home-buttons">
        <a href="#table" className="home-button">Table des Données</a>
        <a href="#about" className="home-button">À Propos</a>
      </div>
        </p>
      </div>
    </div>
  );
}

export default Home;
