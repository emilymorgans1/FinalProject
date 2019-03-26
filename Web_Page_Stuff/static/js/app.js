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
$(function () {
    // when the submit for is clicked
    $('#submit').on('click', function (event) {
        event.preventDefault();

        form_info = $('#upload-file')[0];
        // lets take the whole tak=ble and sned it over to flask
        form_data = new FormData(form_info);
        var file = $('#img_file').val();
        
        $.ajax({
            type: 'POST',
            url: '/uploadfile',
            data: form_data,
            contentType: false,
            dataType: 'json',
            cache: false,
            processData: false
        }).then(function (res) {
            // after the prediction the results are sent as 'res'
            // you an now use 'res' to build your table as you wish
            // console.log(res);
            // success: function (res) {
                var table = '<table>';
                $.each( res.predictions, function( key, value ) {
                  table += '<tr><td>' + value.label + '</td><td>' + value.translation + '</td></tr>';
                });
                    table += '</table>';
                $('.myelement').html(table);
            
        });
    });
});

