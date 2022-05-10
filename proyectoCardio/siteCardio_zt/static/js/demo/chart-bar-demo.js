// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: hta_dmt2_tag,
    datasets: [{
      label: "SI: ",
      borderSkipped: "right",
      backgroundColor: "rgb(70,255,99)",
      borderColor: "rgba(59,59,59,0.50)",
      data: hta_dmt2_si_values,
    },{
      label: "NO: ",
      backgroundColor: "rgb(255,40,145)",
      borderColor: "rgba(59,59,59,0.50)",
      data: hta_dmt2_no_values,
    }],
  },
  options: {
    tooltips: {
      mode: 'label',
      callbacks: {
          label: function(tooltipItem, data) {
              var corporation = data.datasets[tooltipItem.datasetIndex].label;
              var valor = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
              var total = 0;
              for (var i = 0; i < data.datasets.length; i++)
                  total += data.datasets[i].data[tooltipItem.index];
              if (tooltipItem.datasetIndex != data.datasets.length - 1) {
                  return corporation + " : " + valor.toFixed(0).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
              } else {
                  return [corporation + " : " + valor.toFixed(0).replace(/(\d)(?=(\d{3})+\.)/g, '$1,'), "Total : " + total];
              }
          }
      }
    },
    scales: {
      xAxes: [{
        stacked: true,
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        stacked: true,
        ticks: {
          stepSize: 500
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: true
    }
  }
});
