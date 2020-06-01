$(function() {

$.ajax({
  url: '/api/get_data',
  type: 'GET',
  async: true,
  statusCode: {
    200: function(msg) {
      console.log("Success");
      console.log(msg);
      var datapoints = msg.data;
      console.log(datapoints);
      var dataparsed = [];

      datapoints.forEach((item, i) => {
        dataparsed.push(item['ppm'])
      });

      var ctx = document.getElementById('myChart').getContext('2d');
      var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [1,2,3,4,5],
    datasets: [{
        data: dataparsed,
        label: "PPM device 1",
        borderColor: "#3e95cd",
        fill: false
      }]
  },
  options: {
    title: {
      display: true,
      text: 'PPM'
    },
    responsive: false
  }
});


    },
    500: function(msq) {
      console.log("Internal Server Error");
      alert("Server Error. Please try again later.");
    }
  }
});
});
