// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
function chartData(suppliedData)
{
  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: suppliedData["attack_types"],
      datasets: [{
        data: suppliedData["attack_counts"],
        backgroundColor: [  '#36b9cc','#1cc88a','#4e73df',],
        hoverBackgroundColor: [  '#2c9faf','#17a673','#2e59d9',],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
  });
}

function fetchDataAndUpdateChart() {
  $.ajax({
    url: "get_stats", 
    method: 'GET',
    success: function(res) {
      
      chartData(res)
    },
    error: function(error) {
      console.error('Error fetching data:', error);
      
    }
  });
}

setInterval(fetchDataAndUpdateChart(), 1500);
