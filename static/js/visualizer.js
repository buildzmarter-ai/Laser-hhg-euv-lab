function renderHeatmap(data, selector) {
    const margin = {top: 10, right: 10, bottom: 10, left: 10},
          width = 400 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

    const svg = d3.select(selector).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const colorScale = d3.scaleSequential(d3.interpolateViridis)
        .domain([d3.min(data.flat()), d3.max(data.flat())]);

    const cellSize = width / data.length;

    svg.selectAll("rect")
        .data(data.flat())
      .enter().append("rect")
        .attr("x", (d, i) => (i % data.length) * cellSize)
        .attr("y", (d, i) => Math.floor(i / data.length) * cellSize)
        .attr("width", cellSize)
        .attr("height", cellSize)
        .style("fill", d => colorScale(d));
}

export function updateLithoHeatmap(data) {
    const container = d3.select("#heatmap-container");
    container.selectAll("*").remove(); // Clear previous simulation

    const margin = {top: 10, right: 10, bottom: 10, left: 10};
    const width = 500 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // 1. Create the SVG and set dimensions immediately
    const svg = container.append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    // 2. Append the group and move it
    const g = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // 3. Mapping development rate
    const colorScale = d3.scaleSequential(d3.interpolateInferno)
        .domain([d3.min(data.flat()), d3.max(data.flat())]);

    const n = data.length;
    const cellSize = width / n;

    // 4. Draw the cells onto the GROUP (g), not the svg
    g.selectAll("rect")
        .data(data.flat())
        .enter().append("rect")
        .attr("x", (d, i) => (i % n) * cellSize)
        .attr("y", (d, i) => Math.floor(i / n) * cellSize)
        .attr("width", cellSize)
        .attr("height", cellSize)
        .style("fill", d => colorScale(d));
        
    // Mapping development rate to a high-contrast lithography color scale
    const colorScale = d3.scaleSequential(d3.interpolateInferno)
        .domain([d3.min(data.flat()), d3.max(data.flat())]);

    const n = data.length;
    const cellSize = width / n;

    // Use Canvas for better performance if n > 256, but for now SVG is fine
    svg.selectAll("rect")
        .data(data.flat())
        .enter().append("rect")
        .attr("x", (d, i) => (i % n) * cellSize)
        .attr("y", (d, i) => Math.floor(i / n) * cellSize)
        .attr("width", cellSize)
        .attr("height", cellSize)
        .style("fill", d => colorScale(d));
}