// var idButton = d3.select("#identity-btn");
// idButton.on("click", handleClick);

// function handleClick() {
//     d3.event.preventDefault();
//     // console.log("hello");
//     d3.json("/").then(data => {
//         console.log(data)
//     })
// }

// // from app.py
// var tableData = data;

// // get table references
// var tbody = d3.select("tbody");

// function buildTable(data) {
//   // First, clear out any existing data
//   tbody.html("");

//   // Next, loop through each object in the data
//   // and append a row and cells for each value in the row
//   data.forEach((dataRow) => {
//     // Append a row to the table body
//     var row = tbody.append("tr");

//     // Loop through each field in the dataRow and add
//     // each value as a table cell (td)
//     Object.values(dataRow).forEach((val) => {
//       var cell = row.append("td");
//         cell.text(val);
//       }
//     );
//   });
// }

// function handleClick() {

//   // Prevent the form from refreshing the page
//   d3.event.preventDefault();
