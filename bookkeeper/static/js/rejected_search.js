$(function() {
    $('#txtSearch').keyup(function() {
        $.ajax({
            url: USERS_LIST_JSON_URL,
           data: {'search': document.getElementById('txtSearch').value,},
            type: 'GET',
            dataType: "json",
            success: function(data) {

                //data = JSON.parse(data[0]);
                //console.log(data[0].asset_name);
                $('#searchBody').html('');
                for (i in data){
                var link = "asset/" +  data[i].asset_id;
                $('#searchBody').append(
                    "<tr>" +
                    "<td>" + data[i].acquisition_date + "</td>" +
                    "<td>" + data[i].asset_name + "</td>" +
                    "<td>" + data[i].description + "</td>" +
                    "<td>" + data[i].rejection_reason + "</td>" +
                    "<td>" + data[i].asset_barcode + "</td>" +
                    "<td>" + data[i].asset_serial_number + "</td>" +
                    '<td>' + "<a href=" + link + ">" + 'Edit' + "</a>" + '</td>' +
                    "</tr>");
                    //console.log(data);
                };
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

