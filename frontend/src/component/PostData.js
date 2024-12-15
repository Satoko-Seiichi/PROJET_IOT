import React, { useState } from 'react';
import axios from 'axios'; // To make API requests

function PostData() {
  const [temperature, setTemperature] = useState('');
  const [humidity, setHumidity] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const postData = {
      temperature: parseFloat(temperature),
      humidity: parseFloat(humidity),
    };

    try {
      // Assuming the API is set up to receive POST requests at this endpoint
      const response = await axios.post('http://yourapi.com/api/data', postData);
      console.log(response.data);
      alert('Data posted successfully!');
    } catch (error) {
      console.error('Error posting data:', error);
      alert('Error posting data.');
    }
  };

  return (
    <div className="post-data">
      <h2>Post Data Manually</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="temperature">Temperature (°C):</label>
          <input
            type="number"
            id="temperature"
            value={temperature}
            onChange={(e) => setTemperature(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="humidity">Humidity (%):</label>
          <input
            type="number"
            id="humidity"
            value={humidity}
            onChange={(e) => setHumidity(e.target.value)}
            required
          />
        </div>
        <button type="submit">Post Data</button>
      </form>
    </div>
  );
}

export default PostData;
