const options = {
  responsive: true
};

// Make donut chart of number of songs created per performer.
let ctx_donut = $("#producer_song_donutChart").get(0).getContext("2d");

$.get("/producer-frequency.json", function (data) {
  let myDonutChart = new Chart(ctx_donut, {
                                          type: 'doughnut',
                                          data: data,
                                          options: options
                                        });
  // bottom legend
  // $('#producer_song_donutLegend').html(myDonutChart.generateLegend());
});

// Make line chart of number of songs created over time, 
// performer agnostic.
let ctx_line = $("#producer_song_lineChart").get(0).getContext("2d");

$.get("/producer-productivity.json", function (data) {
  let myLineChart = Chart.Line(ctx_line, {
                                data: data,
                                options: options
                            });
  // $("#producer_song_lineLegend").html(myLineChart.generateLegend());
});