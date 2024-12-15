import React from 'react';
import Navbar from './component/Navbar';
import Home from './component/Home';
import Graph from './component/Graph';
import DataTable from './component/DataTable';
import About from './component/About';
import './App.css';
import PostData from './component/PostData';

function App() {
  return (
    <div>
      <Navbar />
      <div id="home">
        <Home />
      </div>
      <div id="graph">
        <Graph />
      </div>
      <div id="table">
        <DataTable />
      </div>
      <div id="postdata">
        <PostData />
      </div>
      <div id="about">
        <About />
      </div>
    </div>
  );
}

export default App;
