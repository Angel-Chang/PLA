
$(document).ready(function() {
  var today = new Date();
  $('#startTime1').datetimepicker({
     format:"YYYY-MM-DD",
     locale: 'zh-tw'
  });

  $('#endTime1').datetimepicker({
     format:"YYYY-MM-DD",
     locale: 'zh-tw'
  });

} );