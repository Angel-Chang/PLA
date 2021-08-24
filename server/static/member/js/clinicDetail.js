$(function() {
  getPara();

  function getPara(){
    let url = new URL(location.href);
    let params = url.searchParams;
    var clinic_id = params.get("clinic_id");
    $("#src_clinic_id").val(clinic_id)
  }

  // 確認申請
  $("#btnApprove").on('click', function() {
    var clinic_id = $("#src_clinic_id").val();
    // call ajax 傳送資料
    var url = "/member/approveClinic/";
    var token = $('input[name=csrfmiddlewaretoken]').val();    
    var para = {
      'csrfmiddlewaretoken':token,
      'clinic_id':clinic_id};
  
    $.ajax({
      url: url, 
      data: para,
      type: 'POST',
      dataType: 'json',
      success: function(data_get){
        var msg = data_get['msg']
        alert(msg);
      },
      error: function (data_get) {
        var msg = data_get['msg']
        alert(msg);
      }
    });
  })
})