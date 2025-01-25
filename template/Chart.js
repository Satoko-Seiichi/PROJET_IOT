var ctx = document.getElementById('graphique-temp').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'La valeur de Températeur',
            data: dataValues,
            backgroundColor: 'rgba(0, 123, 255, 0.2)',
            borderColor: 'rgb(0, 0, 255)',
            borderWidth: 2,
            pointStyle: 'circle',
            pointRadius: 3,
            pointBorderColor: 'blue'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false, // Adjust height automatically
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    callback: function (value) {
                        return value + '°';
                    }
                }
            }],
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'hour',
                    displayFormats: {
                        hour: 'HH:mm'
                    }
                },
                ticks: {
                    autoSkip: true,
                    maxRotation: 45,
                    minRotation: 0
                }
            }]
        }
    }
});
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            console.error("Failed to fetch data from API:", response.statusText);
            return null;
        }
        const data = await response.json();
        console.log("Data fetched successfully:", data);
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}

async function loadCharts() {
    const data = await fetchData("{% url 'json' %}"); // Replace with the correct URL
    if (!data) {
        console.error("No data available to render charts");
        return;
    }

    // Extract temperature and humidity data
    const labels = data.labels || [];
    const tempData = data.temperature || [];
    const humData = data.humidity || [];

    if (labels.length === 0 || tempData.length === 0 || humData.length === 0) {
        console.error("Incomplete data received:", data);
        return;
    }

    // Log the chart data
    console.log("Labels:", labels);
    console.log("Temperature Data:", tempData);
    console.log("Humidity Data:", humData);

    // Create the charts
    createChart(document.getElementById('chart1-temp'), 'Température', tempData, 'rgba(255, 99, 132, 1)');
    createChart(document.getElementById('chart1-hum'), 'Humidité', humData, 'rgba(54, 162, 235, 1)');
    createChart(document.getElementById('chart2-temp'), 'Température', tempData, 'rgba(255, 206, 86, 1)');
    createChart(document.getElementById('chart2-hum'), 'Humidité', humData, 'rgba(75, 192, 192, 1)');
}

function createChart(ctx, label, data, color) {
    if (!ctx) {
        console.error("Canvas context not found for chart:", label);
        return;
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: color,
                borderColor: color,
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Load charts on page load
loadCharts();
