import React, { useState } from 'react';
import './Navbar.css';

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h1 className="navbar-logo">IoT Monitor</h1>
        <button className="menu-button" onClick={toggleMenu}>
          ☰
        </button>
      </div>

      {/* Overlay Menu */}
      <div className={`overlay ${menuOpen ? 'show' : ''}`}>
        <ul className="overlay-menu">
          <li>
            <a href="#home" onClick={closeMenu}>Home</a>
          </li>
          <li>
            <a href="#graph" onClick={closeMenu}>Graph</a>
          </li>
          <li>
            <a href="#table" onClick={closeMenu}>Data Table</a>
          </li>
          <li>
            <a href="#postdata" onClick={closeMenu}>Poster</a>
          </li>
          <li>
            <a href="#about" onClick={closeMenu}>A propos</a>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
