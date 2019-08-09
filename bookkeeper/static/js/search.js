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
                var colour = "white"
                console.log(data[i].asset_is_rejected)
                if (data[i].asset_is_rejected ){
                colour = "pink"}
                $('#searchBody').append(
                    "<tr>" +
                    "<td bgcolor="+ colour +">" + data[i].acquisition_date + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_name + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].description + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_type + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_barcode + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_serial_number + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_location + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_status + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_owner + "</td>" +
                    "<td bgcolor="+ colour +">" + data[i].asset_user + "</td>" +
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

