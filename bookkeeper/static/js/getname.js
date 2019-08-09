function getName() {
  $.ajax({
    url: USERNAME,
    type: 'GET',
    dataType: "json",
    success: function(data) {
      // do something with the return value here if you like
        $('#name').text(data);

    },
    error: function(error) {
                console.log(error);
                }
  });
 // you could choose not to continue on failure...
}

$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  getName();
});