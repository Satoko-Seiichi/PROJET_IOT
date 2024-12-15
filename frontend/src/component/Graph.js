import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'; // Add PointElement
import './Graph.css';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement); // Register PointElement

function Graph() {
  const [graphData, setGraphData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch the temperature data (you might need to fetch time series data)
    const fetchGraphData = async () => {
      try {
        const response = await fetch('http://your-esp8266-ip/api/getGraphData'); // Replace with your actual API endpoint
        const result = await response.json();
        setGraphData(result);
      } catch (error) {
        console.error('Error fetching graph data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchGraphData();

    const interval = setInterval(() => {
      fetchGraphData();
    }, 10000); // Refresh graph data every 10 seconds

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  const chartData = {
    labels: graphData.map(entry => entry.time), // Time data for x-axis
    datasets: [
      {
        label: 'Temperature (°C)',
        data: graphData.map(entry => entry.temperature), // Temperature data for y-axis
        fill: false,
        borderColor: '#0071e3',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Temperature over Time',
      },
    },
  };

  return (
    <div className="graph">
      <h2>Temperature Graph</h2>
      {isLoading ? (
        <p>Loading graph...</p>
      ) : (
        <Line data={chartData} options={options} />
      )}
    </div>
  );
}

export default Graph;
