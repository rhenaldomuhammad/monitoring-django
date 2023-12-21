// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';





function chartDatabar(suppliedData)
{
 
  
}

function fetchBars() {
  $.ajax({
    url: "get_bars", // Replace with the actual API endpoint
    method: 'GET',
    success: function(res) {
      // console.log(res.chart_data.data)
      // Assuming the server returns an array of data points
      let ctx = document.getElementById("myBarChart")
      let myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: res.chart_data.time,
          datasets: res.chart_data.data
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
    },
    error: function(error) {
      console.error('Error fetching data:', error);
      
    }
  });
}

// alert('leo')

setInterval(fetchBars(), 1500);

