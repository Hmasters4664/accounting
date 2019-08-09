$(function() {
    $('#txtSearch').keyup(function() {
        $.ajax({
            url: LOCATION_LIST_JSON_URL,
           data: {'search': document.getElementById('txtSearch').value,},
            type: 'GET',
            dataType: "json",
            success: function(data) {

                //data = JSON.parse(data[0]);
                //console.log(data[0].asset_name);
                $('#searchBody').html('');
                for (i in data){
                $('#searchBody').append(
                    "<tr>" +
                    "<td>" + data[i].city + "</td>" +
                    "<td>" + data[i].province + "</td>" +
                    "<td>" + data[i].country + "</td>" +
                    "<td>" + data[i].building + "</td>" +
                    "<td>" + data[i].floor + "</td>" +
                    "<td>" + data[i].adress + "</td>" +
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
