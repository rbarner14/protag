const options = {
  responsive: true
};

// Make donut chart of number of songs created per producer.
let ctx_donut = $("#performer_song_donutChart").get(0).getContext("2d");

$.get("/performer-frequency.json", function (data) {
  let myDonutChart = new Chart(ctx_donut, {
                                          type: 'doughnut',
                                          data: data,
                                          options: options
                                        });
  // $('#performer_song_donutLegend').html(myDonutChart.generateLegend());
});