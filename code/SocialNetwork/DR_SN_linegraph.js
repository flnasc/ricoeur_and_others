////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// .js file for interactive linegraph for Paul Ricoeur's Social Network, a branch of Ricoeur and the Other.
// Ricoeur and the Other is a part of Digital Ricoeur project
//
// This is an interactive visualization efforts of Paul Ricoeur's intellectual peers, as referred to by Ricoeur
// in his vast primary literature as corpora
//
// by Do Yeun Kim
//
//

// Initialize the array for dataset
var lineData = [],
    width = 1000,
    height = 600,
    padding = 80,
    linegraph = d3.select(".linegraphDIV").
        append("svg").
        attr("class", "graph").
        attr("width", width).
        attr("height", height);
var g = linegraph.append("g").attr("transform", "translate(" + padding + "," + padding + ")");

var x = d3.scaleBand().rangeRound([padding, width - padding]),
    y = d3.scaleLinear().range([height - padding, padding]),
    z = d3.scaleOrdinal(d3.schemeCategory20);

var line = d3.line().
    curve(d3.curveBasis).
    x(function(d) {return x(d.year);}).
    y(function(d) {return y(d.freq);});  

// Read in the .csv file
d3.csv("./data/lineGraph.csv", type, function(error, data) {
    lineData = data;
    if (error) {
        console.log(error);
        window.alert("Cannot read in the file.");
    }
    else {
        console.log(lineData);

        var Thinkers = lineData.columns.slice(2).map(function(id) {
            return {
                id: id,
                values: lineData.map(function(d) {
                    return {year: d.Year, freq : d[id]};
                    
                })
            };
        });

        x.domain(d3.extent(lineData, function(d) { return d.Year; }));

        var ymin = d3.min(Thinkers, function(c) { return d3.min(c.values, function(d) { return d.freq; }); }),
            ymax = d3.max(Thinkers, function(c) { return d3.max(c.values, function(d) { return d.freq; }); })
        y.domain([ymin, ymax]);
        console.log(ymax);

        z.domain(Thinkers.map(function(c) { return c.id; }));
        

        g.append("g").
            attr("class", "axis axis--x").
            attr("transofrm", "translate(0," + height + ")").
            call(d3.axisBottom(x));

        g.append("g").
            attr("class", "axis axis--y").
            call(d3.axisLeft(y)).
            append("text").
            attr("transform", "rotate(-90)").
            attr("y", 6).
            attr("dy", "0.71em").
            attr("fill", "black").
            text("Frequency");

        var thinker = g.selectAll(".thinker").
            data(Thinkers).
            enter().
            append("g").
            attr("class", "thinker");

        thinker.append("path").
            attr("class", "line").
            attr("d", function(d) { return line(parseInt(d.values)); }).
            style("stroke", function(d) {return z(d.id); });

        thinker.append("text").
                datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; }).
                attr("transform", function(d) { return "translate(" + x(d.value.year) + "," + y(d.value.freq) + ")"; }).
                attr("x", 3).
                attr("dy", "0.35em").
                style("font", "10px sans-serif").
                text(function(d) { return d.id; });

    }
});

function type(d, _, columns) {

    for (var i = 1, n = columns.length, c; i < n; i++) {
        d[c = columns[i]] = +d[c];
    }
    return d;
}

