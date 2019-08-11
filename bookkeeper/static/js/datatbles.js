$(document).ready( function () {
    $('#myTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": USERS_LIST_JSON_URL
    });
} );