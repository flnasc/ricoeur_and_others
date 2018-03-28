////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// .js file for interactive visualization fo Paul Ridcoeur's Social Network, a branch of Ricoeur and the Other.
// Ricoeur and the Other is a part of Digital Ricoeur project
// 
// This is an interactive visualization effort of Paul Ricoeur's intellectual peers, as referred to by Ricoeur
// in his vast primary literature as corpora.
//
// by Do Yeun Kim
//
//
//

// Initialize the array for dataset
var dataset = [];

// Read in the .csv file
// Right now this reads in one file, but maybe we should expand it to read in all .csv files?
// Print out an error message if the file is unreadable.
// Otherwise, save the CSV file into dataset then call visualize function
d3.csv("./data/summary.csv", function(error, data) {
    dataset = data;
    if (error) {
        console.log(error);
        window.alert("Cannot read in the file.");
    }
    else {
        console.log(data);

        // Safety check that we are correctly reading in the file
        for (i = 0; i < dataset.length; i++) {
            console.log(dataset[i]);
        }
        // Call on the visualization function
    
        // Sort dataset 
        // Right now I need to manually trigger them here, but I will add drop-down menu
        // // Z to A 
        // dataset.sort(sort_by('Thinker', true, function(a) {return a}));
        // // A to Z
        // dataset.sort(sort_by('Thinker', false, function(a) {return a}));
        // // Descending order 
        // dataset.sort(sort_by('Frequency', true, parseInt));
        // // Ascending order
        // dataset.sort(sort_by('Frequency', flase, parseInt));
        barGraph();
    }
});


// The main function
// Set dimension of the SVG, create the element, then draw the graph
//
function barGraph(){

    // Set dimensions for the visualization
    var width = 1000;
    var height = 600;
    var padding = 80;
    var barPad = 1;
    var barWidth = (width - 2 * padding) / dataset.length - barPad;

    // Create svg frame for visualization given the attributes above
    var svg = d3.select("body").
        append("svg").
        attr("width", width).
        attr("height", height);

    // Set scales for x-axis and y-axis to afford dynamic scaling
    var xScale = d3.scaleBand().
        domain(d3.range(dataset.length)).
        rangeRound([padding, width - padding]);
    var yScale = d3.scaleLinear().
        domain([0,d3.max(dataset, function(d, i) {
            return dataset[i].Frequency;
       })]).
        range([height - padding, padding]);
    
    // Create the bar graph
    svg.selectAll("rect").
        data(dataset).
        enter().
        append("rect").
        attr("x", function(d,i) {
            return (padding + i * ((width - 2 * padding) / dataset.length));}).
        attr("y", function(d, i) {
            return height - (yScale(0) - yScale(dataset[i].Frequency) + padding)}).
        attr("width", barWidth).
        attr("height", function(d, i) {
            return yScale(0) - yScale(dataset[i].Frequency)}).
        attr("fill", "#191970");
   
    // Add frequency to the bar  
    var textSize = barWidth/3;
    svg.selectAll("text.labels").
        data(dataset).
        enter().
        append("text").
        text(function(d, i) {
            return dataset[i].Frequency;}).
        attr("x", function(d, i) {
            return (barWidth/2 + padding + i * ((width - 2 * padding) / dataset.length));}).
        attr("y", function(d, i){ 
            return (height - (yScale(0) - yScale(dataset[i].Frequency)) - padding)}).
        attr("font-family", "arial").
        attr("font-size", textSize + "px").
        attr("fill", "red").
        style("text-anchor", "middle").
        attr("class", "labels")

    // Define the axes
    var xAxis = d3.axisBottom(xScale).
        tickFormat(function(d, i) {
            return dataset[i].Thinker;});
    var yAxis = d3.axisLeft(yScale);

    // Draw the axes
    svg.append("g").
        attr("class", "x axis").
        attr("transform", "translate(0 "+ (height - padding) + ")").
        call(xAxis).
        attr("font-weight", "bold");
    svg.append("g").
        attr("class", "y axis").
        attr("transform", "translate(" + padding + ",0)").
        call(yAxis);

    // Add the labels to the axes
    svg.append("text").
        attr("transform", "translate(" + (width/2) + "," + (height - padding/2) + ")").
        attr("font-weight", "bold").
        style("text-anchor", "middle").
        text("Thinkers");
    svg.append("text").
        attr("transform", "rotate(-90)").
        attr("y", padding / 3).
        attr("x", 0 - height / 2).
        attr("dy", "1em").
        attr("font-weight", "bold").
        style("text-anchor", "middle").
        text("Frequency");

}

// Helper function for sort
// Borrowed from https://stackoverflow.com/questions/979256/sorting-an-array-of-javascript-objects
var sort_by = function(field, reverse, primer) {
    var key = primer ?
        function(x) {return primer(x[field])} :
        function(x) {return x[field]};
    
    reverse = !reverse ? 1 : -1;

    return function (a,b) {
        return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
    }

}

