$(document).ready( function () {
var table =    $('#myTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": USERS_LIST_JSON_URL
    });

$('#myTable').on( 'click', 'tr', function () {

    var id = table.row( this ).data()[0]
    url = "update/"+ id + '/'
    $('#myTable').modalForm({
    formURL: url
    });

} );


} );

