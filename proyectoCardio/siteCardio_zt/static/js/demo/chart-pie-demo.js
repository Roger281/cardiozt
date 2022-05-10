// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example

var ctx = document.getElementById("totalGenero");
var ctx2 = document.getElementById("totalMuertos");
var ctx3 = document.getElementById("totalEdades");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: total_genero_tag,
    datasets: [{
      data: total_genero,
      backgroundColor: ['#4682ff', '#ff6271'],
    }],
  },
});
var myPieChart1 = new Chart(ctx2, {
  type: 'pie',
  data: {
    labels: total_muertos_genero_tag,
    datasets: [{
      data: total_muertos_genero,
      backgroundColor: ['#4682ff', '#ff6271'],
    }],
  },
});
var myPieChart3 = new Chart(ctx3, {
  type: 'pie',
  data: {
    labels: edades_tag,
    datasets: [{
      data: edades_values,
      backgroundColor: ['#77ff72', '#4682ff', '#ff6271'],
    }],
  },
});
