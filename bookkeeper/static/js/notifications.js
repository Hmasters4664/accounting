function executeQuery() {
  $.ajax({
    url: NOTIFICATIONS,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like
      var num = data.length;
      $('#num').text(num);
      var link = "/pending";
      if (num > 5) {
        num = 5;
      }
      $('#notificationinfo').html('');
      var holder1 = "mess__item";
      var holder2 = "image img-cir img-40";
      var holder3 = "images/icon/avatar-04.jpg";
      var holder4 = "content";
      var holder5 = "time";
      for (i = 0; i < num; i++) {
        $('#notificationinfo').append(
       "<a href=" + link +">" +
        "<div class="+ holder1 +">" +
            "<div class=" + holder2 +">" +
                "<img src="+ holder3 +"/>" +
            "</div>" +
            "<div class="+ holder4 +">" +
            "<h6>" + data[i].asset_name + "</h6>" +
                "<p>" + data[i].asset_status + "</p>" +
            "<span class=" + holder5 +">" + data[i].acquisition_date + "</span>" +
            "</div>" +
        "</div>"+
        "</a>");
      };
    },
    error: function(error) {
                console.log(error);
                }
  });
  setTimeout(executeQuery, 300000); // you could choose not to continue on failure...
}

$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  setTimeout(executeQuery, 300);
});