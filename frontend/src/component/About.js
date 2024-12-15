import React from 'react';
import './About.css';

function About() {
  return (
    <div className="about">
      <div className="about-container">
        <h1>À propos du projet</h1>
        <p>
          Le capteur DHT11 est un capteur de température et d'humidité économique et facile à utiliser.
          Il est idéal pour des projets IoT (Internet des objets) grâce à sa simplicité et sa compatibilité
          avec des plateformes comme Arduino et ESP8266.
        </p>
        <p>
          Pour utiliser le DHT11, connectez les broches VCC, GND et DATA à votre microcontrôleur.
          Vous pouvez lire les données à l'aide de bibliothèques prêtes pour les protocoles courants.
        </p>
        <h2>Remerciements</h2>
        <p>
          Ce projet a été créé avec passion par <strong>Youness</strong>, qui a mis tout en œuvre
          pour offrir une solution simple et élégante pour le suivi de température et d'humidité.
        </p>
        <p className="dedication">
          "Merci à tous ceux qui soutiennent mes efforts et ma créativité."
        </p>
        <h3>Copyright</h3>
        <p>© 2024 Youness. Tous droits réservés.</p>
      </div>
    </div>
  );
}

export default About;
