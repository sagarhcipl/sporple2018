// The base endpoint to receive data from. See update_url()
var URL_BASE = "/stats/csv";

// Update graph in response to inputs
d3.select("#stat-type").on("input", make_graph);
d3.select("#stat-data").on("input", make_graph);

var margin = {top: 20, right: 50, bottom: 100, left: 100};
var width = 1000 - margin.left - margin.right;
var height = 600 - margin.top - margin.bottom;

var x = d3.time.scale().range([0, width]);
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(5);
var y = d3.scale.linear()
    .range([height, 0]);
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var parseDate = d3.time.format("%Y-%b-%d").parse;

var valueline = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.count); })

var svg = d3.select("body")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

// x axis
svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .text("Time")
      .attr("dy", "3em")
      .attr("text-align", "center")
      .attr("x", width / 2 - margin.right - margin.left);

// y axis
svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("dy", "-3em")
    .text("Count");

/*
// Update the time displayed (XX:XX) next to the time slider
function update_slider(time) {
  var dateObj = new Date();
  dateObj.setHours(Math.floor(time/60));
  dateObj.setMinutes(time % 60);
  d3.select("#prettyTime")
    .text(dateObj.toTimeString().substring(0, 5));
}
*/
// Return url to recieve csv data with query filled in from input fields
function update_url() {
  return URL_BASE +
        "?type=" + document.getElementById("stat-type").value +
        "&data=" + document.getElementById("stat-data").value;
}

function make_graph() {
  //update_slider(+document.getElementById("time").value);
  url = update_url();
  
  // Get the data
  d3.csv(url, function(error, data) {
    // convert to values
    data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.count = +d.count;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    svg.selectAll("g.y.axis")
        .call(yAxis);

    svg.selectAll("g.x.axis")
        .call(xAxis);

    // Add the valueline path.
    svg.selectAll("path.line").remove();
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));
  });

/*
  source: http://www.datasciencebytes.com/bytes/2015/03/07/a-d3js-plot-powered-by-a-sql-database/
  d3.csv(url, type, function(error, data) {
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    svg.selectAll("g.y.axis")
      .call(yAxis);

    // create a line
    var line = d3.svg.line()
      .x(function(d,i) {
        console.log(d.x);
        return x(d.x);
      })
      .y(function(d,i) {
        console.log(d.y);
        return y(d.y);
      });
/*
    var bars = svg.selectAll(".bar")
      .data(data, function(d) { return d.etd; });

    bars.transition(1000)
      .attr("y", function(d) { return  y(d.count); } )
      .attr("height", function(d) { return height - y(d.count); } );

    bars.enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.etd); })
      .attr("width", x(1 - 2 * binMargin))
      .attr("y", height)
      .attr("height", 0)
      .transition(1000)
        .attr("y", function(d) { return y(d.count); })
        .attr("height", function(d) { return height - y(d.count); });

    bars.exit()
      .transition(1000)
        .attr("y", height)
        .attr("height", 0)
      .remove();
  });
*/
}

make_graph();
