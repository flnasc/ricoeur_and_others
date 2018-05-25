///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// .js file for interactive visualizatoins for Paul Ridcoeur's Social Network, a branch of Ricoeur and the Other.
// Ricoeur and the Other is a part of Digital Ricoeur project
// 
// This is an interactive visualization effort of Paul Ricoeur's intellectual peers, as referred to by Ricoeur
// in his vast primary literature as corpora.
//
// by Do Yeun Kim
//
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

var width = 1600,
    height = 900,
    padding = 80,
    l_set = [];
const l_default = 20;

// Read in the .csv file
// Print out an error message if the file is unreadable.
// Otherwise, save the CSV file into l_set then call visualize function
function initialize() {
    
    // Read in the csv file for line graph
    // Similarly, check for error then initialize the graph
    d3.csv("./data/lineAVG.csv", type, function(error, data) {
        l_set = data;
        if (error) {
            console.log(error);
            window.alert("Cannot read in the file.");
        }
        // console.log(l_set);
        initLine();
    });
}

// Displays the 8x5 matrix of the top 40 thinkers
// Also when the user clicks on "Top 20" button, collapse the matrix and call initLine.
function openCustom() {
    var customDiv = document.getElementById("lineCustomize");
    var displayStatus = customDiv.style.display;
    if (document.getElementById("lineDefault").checked) {
        customDiv.style.display = "none"; 
        initLine();
    }
    else {
        if(displayStatus=="none") {
            customDiv.style.display = "table";
        } else {
            customDiv.style.display = "none";
        }
    }
}

// Clear the customization matrix of checks
// All thinker checkboxes share the class "customCheck"
function clearCustom() {
    var i = 0;
    while (document.getElementsByClassName("customCheck")[i]) {
        document.getElementsByClassName("customCheck")[i].checked = false; 
        i++;
    }
}

// Select all of customization matrix
// All thinker checkboxes share the class "customCheck"
function selectAllCustom() {
    var i = 0;
    while (document.getElementsByClassName("customCheck")[i]) {
        document.getElementsByClassName("customCheck")[i].checked = true; 
        i++;
    }
}

var thinkers_sh = [];
// As of now, we are using a predfined color scheme with 20 colors.
// We might need to define our own color scheme if we want to show more than 20 thinkers
var l_x = d3.scaleTime().range([padding, width - padding]),
    l_y = d3.scaleLinear().range([height - padding, padding]),
    l_z = d3.scaleOrdinal(d3.schemeCategory20);

// Using d3 library's timeParse function to parse years 
var parseYear = d3.timeParse("%Y");

// Draw line
var line = d3.line().
    x(function(d) {return l_x(d.year);}).
    y(function(d) {return l_y(d.freq);});

/// Initialize line
function initLine() {
    // Create thinkers, which is a map that allows us to access individual frequencies,
    // mapped onto each thinker and year
    var thinkers = l_set.columns.slice(2).map(function(id) {
        return {
            id: id,
            values: l_set.map(function(d) {
                return {year: d.year, freq: d[id]};
            })
        };
    });
    //console.log(thinkers);
    //console.log(thinkers[0]);
    var customSize = document.getElementsByClassName("customThinkers").length;

    for (var i = 0; i < customSize; i++) {
        var rankedName = (i + 1).toString() + ". " + thinkers[i].id;
        // console.log(rankedName);
        document.getElementsByClassName("customThinkers")[i].innerHTML = rankedName;
    }

    // This part allows us to alternate between top 20 and custom of sort
    var show;
    if (document.getElementById("lineDefault").checked) {
        d3.select("#l_graph").remove();
        show = l_default;
        // console.log("Drawing default lines");

        // Empty thinkers_sh
        thinkers_sh = [];
        for (var i = 0; i < show; i++) {
            thinkers_sh[i] = thinkers[i]; 
        }
    } else {
        d3.select("#l_graph").remove();
        // console.log("Drawing custom lines");

        // Empty thinkers_sh
        thinkers_sh = [];
        for (var i = 0; i < customSize; i++) {
            if (document.getElementsByClassName("customCheck")[i].checked) {
                thinkers_sh.push(thinkers[i]); 
            }
        }
    }

    // define the domain for the axes
    l_x.domain(d3.extent(l_set, function(d) {return d.year;}));
    l_y.domain([
        d3.min(thinkers_sh, function(c) {return d3.min(c.values, function(d) {return d.freq;}); }),
        d3.max(thinkers_sh, function(c) {return d3.max(c.values, function(d) {return d.freq;}); })
    ]);
    l_z.domain(thinkers_sh.map(function(c) {return c.id;}));

    // console.log(thinkers_sh);
    drawLineChart();

}


// This function actually draws the line graph
function drawLineChart() {


    // The line graph will be appended to div of class "l_DIV"
    var linegraph = d3.select("#l_DIV").
        append("svg").
        attr("class", "graph").
        attr("width", width + padding).
        attr("height", height).
        attr("id", "l_graph");

    var g = linegraph.append("g");

    // Define axes for lin graph
    var l_xAxis = d3.axisBottom(l_x);
    var l_yAxis = d3.axisLeft(l_y);
    // Draw the axes
    g.append("g").
        attr("class", "x axis").
        attr("transform", "translate(0" + "," + (height - padding) + ")").
        call(l_xAxis);
    g.append("g").
        attr("class", "y axis").
        attr("transform", "translate(" + padding + ",0)").
        call(l_yAxis);

   // Label the axes     
    g.append("text").
        attr("transform", "translate(" + (width/2) + "," + (height - padding/2) + ")").
        attr("font-weight", "bold").
        text("Years");
    g.append("text").
        attr("transform", "rotate(-90)").
        attr("y", padding / 3).
        attr("x", 0 - height / 2).
        attr("dy", "1em").
        attr("font-weight", "bold").
        style("text-anchor", "middle").
        text("Frequency");

    // Each thinker
    var thinker = g.selectAll(".thinker").
        data(thinkers_sh).
        enter().
        append("g").
        attr("class", "thinker");

    // For each thinker, draw a line using the values 
    // Here, values defined in initLine function as thinkers was created
    thinker.append("path").
        attr("class", "line").
        attr("id", function(d) { return d.id; }).
        attr("d", function(d) {
            return line(d.values); }).
        style("stroke", function(d) { return l_z(d.id); }).
        on("mouseover", function(d, i) {
            // When the user hovers over a line, display the appropriate name at the top center of the graph
            thinker.append("text").
                datum(function(d, i) { 
                    // Don't use this part right now, but we will want to use this in the future
                }).
                attr("transform", "translate("+ (width/2) + "," + padding + ")").
                attr("x", 3).
                attr("dy", "0.35em").
                style("font", "20px sans-serif").
                style("text-anchor", "middle").
                text(this.id).
                attr("id", "bigName");

        }).
        on("mouseout", function(d) {
            // Clear the name at the top center of the graph
            thinker.select("#bigName").remove();
        }).
        on("click", function(d, i) {
            window.open("https://digitalricoeur.org/search/" + thinkers_sh[i].id);
        });


    // Variables used to display the "legend"
    var fontSize = 15;
    var extraMargin = 2;
    // Append the name of the thinker as the legend at the upper right corner of the graph, with some margin between
    thinker.append("text").
        datum(function(d) {return {id: d.id, value: d.values[d.values.length - 1]};}).
        attr("transform", function(d, i) {return "translate(" + l_x(d.value.year) + "," + (padding + i * (fontSize + extraMargin)) +")";}).
        attr("x", fontSize).
        attr("dy", "0.35em").
        style("font", fontSize + "px sans-serif").
        style("font-weight", "bold").
        style("fill", "black").
        text(function(d) {return d.id;}).
        on("mouseover", function(d) {
            this.style.fill = "red";
        }).    
        on("mouseout", function(d) {
            this.style.fill = "black"
        }).
        on("click", function(d) {
            window.open("https://digitalricoeur.org/search/" + d.id);
        });
  
    // Append circles of appropriate color to the legend 
    var legendOffset = 10;
    var radius = 5;
    thinker.append("circle").
            datum(function(d) {return {id: d.id, value: d.values[d.values.length - 1]};}).
            attr("transform", function(d, i) {return "translate(" + l_x(d.value.year) + "," + (padding + i * (fontSize + extraMargin)) + ")";}).
            attr("cx", legendOffset).
            attr("r", radius).
            attr("fill", function(d, i) { return l_z(d.id);});
    
}

// When the csv file is read, all elements are read in as string
// Here, we parse for date and convert the frequencies to numbers
function type (d, _, columns) {
    // Parse years into year format provided by d3 library
    d.year = parseYear(d.year);
    var n = columns.length;
    for (var i = 1; i < n; ++i) {
        c = columns[i];
        d[c] = +d[c];
    }
    return d;
}

initialize();
