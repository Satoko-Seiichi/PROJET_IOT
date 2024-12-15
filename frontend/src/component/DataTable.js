// DataTable.js
import React, { useState, useEffect } from 'react';
import './DataTable.css';

function DataTable() {
  const [data, setData] = useState([]);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [newData, setNewData] = useState({
    time: '',
    temperature: '',
    humidity: ''
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://your-esp8266-ip/api/getData'); // Replace with your actual API endpoint
        const result = await response.json();
        setData(result);
        setHistory(prevHistory => [result, ...prevHistory]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Here, you would send the data to the API for posting
    // Example:
    try {
      const response = await fetch('http://your-esp8266-ip/api/postData', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newData)
      });
      const result = await response.json();
      setData(result); // Update the data with the newly posted data
    } catch (error) {
      console.error('Error posting data:', error);
    }
  };

  return (
    <div className="data-table">
      <h2>Data Table</h2>
      {isLoading ? (
        <p>Loading data...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Temperature (°C)</th>
              <th>Humidity (%)</th>
            </tr>
          </thead>
          <tbody>
            {data && data.time && (
              <tr>
                <td>{data.time}</td>
                <td>{data.temperature}</td>
                <td>{data.humidity}</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
      <h3>Post New Data</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="time"
          value={newData.time}
          onChange={handleChange}
          placeholder="Time"
        />
        <input
          type="number"
          name="temperature"
          value={newData.temperature}
          onChange={handleChange}
          placeholder="Temperature"
        />
        <input
          type="number"
          name="humidity"
          value={newData.humidity}
          onChange={handleChange}
          placeholder="Humidity"
        />
        <button type="submit">Post Data</button>
      </form>
      <button onClick={() => setData(history[history.length - 1])}>Show Latest Data</button>
      <button onClick={() => setHistory([])}>Clear History</button>
      <h3>History</h3>
      <ul>
        {history.map((entry, index) => (
          <li key={index}>
            {entry.time}: Temp: {entry.temperature}°C, Humidity: {entry.humidity}%
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DataTable;
