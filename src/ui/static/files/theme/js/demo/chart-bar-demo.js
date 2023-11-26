// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';



// Bar Chart Example
var ctx = document.getElementById("myBarChart").getContext("2d");
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: chartData.time, // Menggunakan waktu dari data
    datasets: chartData.data.map(function(item) {
      return {
        label: item.label,
        backgroundColor: item.backgroundColor,
        data: item.data
      };
    })
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 6
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          min: 0,
          // Sesuaikan max sesuai dengan nilai maksimum yang mungkin
          maxTicksLimit: 5,
          padding: 10,
          callback: function(value) {
            return value;
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: true
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: true,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': ' + tooltipItem.yLabel;
        }
      }
    },
  }
});

function chartDatabar(suppliedData)
{
  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: suppliedData,
    options: {
      barValueSpacing: 20,
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
          }
        }]
      }
    }
  });
  
}

function fetchBars() {
  $.ajax({
    url: "get_bars", // Replace with the actual API endpoint
    method: 'GET',
    success: function(res) {
      // Assuming the server returns an array of data points
      chartDatabar(res)
    },
    error: function(error) {
      console.error('Error fetching data:', error);
      
    }
  });
}

alert('leo')

setInterval(fetchBars(), 1500);