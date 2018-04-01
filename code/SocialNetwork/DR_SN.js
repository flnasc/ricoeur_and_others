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
var dataset = [], 
    barFiltered = [],
    lineFiltered = [],
    startYear = Number.MAX_SAFE_INTEGER,
    endYear = Number.MIN_SAFE_INTEGER;

// Read in the .csv file
// Right now this reads in one file, but maybe we should expand it to read in all .csv files?
// Print out an error message if the file is unreadable.
// Otherwise, save the CSV file into dataset then call visualize function
function initialize() {

    d3.csv("./data/summary.csv", function(error, data) {
        dataset = data;
        if (error) {
            console.log(error);
            window.alert("Cannot read in the file.");
        }
        else {
            console.log(dataset);
        
            // Safety check that we are correctly reading in the file
            for (i = 0; i < dataset.length; i++) {
                if (dataset[i].Year < startYear) {
                    startYear = dataset[i].Year;
                }   
                if (dataset[i].Year > endYear) {
                    endYear = dataset[i].Year;
                }
            }

            // Display the date range we are currently working on
            document.getElementById("startYear").value = startYear;
            document.getElementById("endYear").value = endYear;
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
            filterBar();
            barGraph();
        }
    });
}

// Update date range for the bar graph
// This function grabs the date range provided by the user, re-filters the dataset, 
// and updates the visualization
function grabDate() {
    startYear = parseInt(document.getElementById("startYear").value);
    endYear = parseInt(document.getElementById("endYear").value);

    console.log(startYear);
    console.log(endYear);
    
    filterBar();
    d3.select("svg").remove();
    barGraph();
}


// The main function
// Set dimension of the SVG, create the element, then draw the graph
//
function barGraph(){

    // Set dimensions for the visualization
    var width = 1000;
    var height = 600;
    var padding = 80;
    var barPad = 1;
    var barWidth = (width - 2 * padding) / barFiltered.length - barPad;

    // Create svg frame for visualization given the attributes above
    var svg = d3.select("body").
        append("svg").
        attr("width", width).
        attr("height", height);

    // Set scales for x-axis and y-axis to afford dynamic scaling
    var xScale = d3.scaleBand().
        domain(d3.range(barFiltered.length)).
        rangeRound([padding, width - padding]);
    var yScale = d3.scaleLinear().
        domain([0,d3.max(barFiltered, function(d, i) {
            return barFiltered[i].Frequency;
       })]).
        range([height - padding, padding]);
    
    // Create the bar graph
    svg.selectAll("rect").
        data(barFiltered).
        enter().
        append("rect").
        attr("x", function(d,i) {
            return (padding + i * ((width - 2 * padding) / barFiltered.length));}).
        attr("y", function(d, i) {
            return height - (yScale(0) - yScale(barFiltered[i].Frequency) + padding)}).
        attr("width", barWidth).
        attr("height", function(d, i) {
            return yScale(0) - yScale(barFiltered[i].Frequency)}).
        attr("fill", "#191970");
   
    // Add frequency to the bar  
    var textSize = barWidth/3;
    svg.selectAll("text.labels").
        data(barFiltered).
        enter().
        append("text").
        text(function(d, i) {
            return barFiltered[i].Frequency;}).
        attr("x", function(d, i) {
            return (barWidth/2 + padding + i * ((width - 2 * padding) / barFiltered.length));}).
        attr("y", function(d, i){ 
            return (height - (yScale(0) - yScale(barFiltered[i].Frequency)) - padding)}).
        attr("font-family", "arial").
        attr("font-size", textSize + "px").
        attr("fill", "red").
        style("text-anchor", "middle").
        attr("class", "labels");

    // Define the axes
    var xAxis = d3.axisBottom(xScale).
                    tickFormat(function(d, i) {
                        return barFiltered[i].Thinker;});
    var yAxis = d3.axisLeft(yScale);

    // Draw the axes
    svg.append("g").
        attr("class", "x axis").
        attr("transform", "translate(0 "+ (height - padding) + ")").
        call(xAxis).
        attr("font-weight", "bold").
        selectAll(".tick text").
        call(wrapLabel, barWidth);
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

// Function that wraps long names so that the labels do not overlap
// The code was taken from Mike Bostok's code, found here:
// https://bl.ocks.org/mbostock/7555321
function wrapLabel(text, barWidth) {
    text.each(function() {
        var text = d3.select(this),
            // words is a reversed array of the split string where the string is split 
            // based on the regex \s+ which turns each continuous empty space with 
            // empty string
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            dy = parseFloat(text.attr("dy")),
            // Define tspan for adjusting of location for the label
            tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
        // Fetch the words from the label one by one
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            // If the length of the tspan is greater than barWidth, i.e. if the name is too long
            // remove the last word from the current line and create a new line for this word
            if (tspan.node().getComputedTextLength() > barWidth) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
            }
        }
    });
}
// Helper function for sort
// Borrowed from https://stackoverflow.com/questions/979256/sorting-an-array-of-javascript-objects
var sort_by = function(field, reverse, primer) {
    
    // Check for primer and see what additional steps must be made
    var key = primer ?
        function(x) {return primer(x[field])} :
        function(x) {return x[field]};
    
    // Determines whether the directionality is reversed (1 or -1)    
    reverse = !reverse ? 1 : -1;

    // sort using reverse
        return function (a,b) {
        return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
    }

}

// This function filters dataset to better accomodate for data being visualized
// First, the dataset is filtered by the year range
// Then, the frequency at which the thinker is refered to in Ricoeur's work
// is summed up for each thinker so that we don't display multiple occasions for
// each thinker
function filterBar() {

    // Create temporary arrays to process
    dateFilter = [];
    // This method allows for creating an independent copy of dataset
    // Makes a copy of dataset as temp
    let temp = dataset.slice(0);  
    console.log(temp);
    // dataset is now independent of temp, and will not refer to temp
    // i.e. modifying temp will no longer modify dataset
    temp = dataset.map(o => Object.assign({}, o));

    // If the datum falls into the date range, add it to the temporary arry
    for (var i = 0; i < temp.length; i++) {     
        if (parseInt(startYear) <= parseInt(temp[i].Year) && parseInt(temp[i].Year) <= parseInt(endYear)) {
            dateFilter.push(temp[i]);
        }
    }
    // Sort the temporary array to make summation easier
    dateFilter.sort(sort_by('Thinker'), false, function(a) {return a});

    // Initialize variables for summation
    sum = 0;
    bfLen = 0;
    // Reset barFiltered 
    barFiltered.length = 0;

    // Iterate through temp and look for redundancy in thinkers
    for (var i = 0; i < dateFilter.length; i++) {
        // Add initial item
        if (!i) {
            barFiltered.push(dateFilter[i]);
            bfLen++;
        } 
        // If the current thinker is different from the previous one, 
        // add the entry to the barFiltered array
        else if (dateFilter[i].Thinker != dateFilter[i - 1].Thinker) {
            barFiltered.push(dateFilter[i]);
            barFiltered[bfLen].Frequency = parseInt(dateFilter[i].Frequency);
            bfLen++;
        } 
        // If the current thinker has just been added to the array
        // sum up frequency
        else {
            sum = parseInt(barFiltered[bfLen - 1].Frequency) + parseInt(dateFilter[i].Frequency)
            barFiltered[bfLen - 1].Frequency = sum;
        }
    }
    console.log(barFiltered);

}

initialize();
