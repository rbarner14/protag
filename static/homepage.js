// Request json from the server and execute callback when reponse is received.

d3.json('/data.json', makeForceGraph);

function makeForceGraph(data){

  // In this case, data is coming from the server, and is
  // the proper format for this visualization. In general, a force layout
  // requires two data arrays. The first array, here named `nodes`,
  // contains the object that are the focal point of the visualization.
  // The second array, called `links` below, identifies all the links
  // between the nodes. (The more mathematical term is "edges.")

  let dataNodes = data.nodes;
  let links = data.paths;

  // Define the dimensions of the visualization.

  $container = $("#svg_container");
  const width = $container.width();
  const height = 600;

  ////////////////////////////////////////////////////////////////////////////////
  // D3 Visualization //

  // We start off by creating an SVG container to hold the visualization. 
  // We only need to specify the dimensions for this container.

  let svg = d3.select('#svg_container')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

  // Now we create a forceSimulation object and add several forces to
  // this simulation.

  let force = d3.forceSimulation(d3.values(dataNodes))
        .force("link", d3.forceLink(links).distance(150))
        .force("center", d3.forceCenter(width / 2, height/ 2))
        .force("charge", d3.forceManyBody().strength(-100))
        .on("tick", tick);


  // Add lines to the SVG to visualize links.

  let link = svg.selectAll(".link")
      .data(links)
      .enter()
          .append("line")
          .attr("class", "link");

  // Add groups to the SVG to visualize the node data.
  
  let node = svg.selectAll(".node")
      .data(force.nodes())
      .enter()
          .append("g")
          .attr("class", "node")
          .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

  let color = d3.scaleOrdinal(d3.schemeCategory10);

  node.append("circle") // Appends a circle SVG element to each ".node" element
      .attr("r", 15)
      .style("fill", function (d) {
        return color(d.parent);
      });

  node.append("text").text(function (d) { // Appends a text SVG element to each ".node" element
    return d.name;
  });

  function tick() {
    link.attr("x1", function (d) {
          return d.source.x;
        })
        .attr("y1", function (d) {
          return d.source.y;
        })
        .attr("x2", function (d) {
          return d.target.x;
        })
        .attr("y2", function (d) {
          return d.target.y;
        });

    node.attr("transform", function (d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  }

  function dragstarted(d) {
    if (!d3.event.active) {
      force.alphaTarget(0.3).restart();
    }
  }
      
  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
      
  function dragended(d) {
    if (!d3.event.active) {
      force.alphaTarget(0);
    }

    d.fx = null;
    d.fy = null;
  }
}
