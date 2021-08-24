$(function() {
  getPara();

  function getPara(){
    let url = new URL(location.href);
    let params = url.searchParams;
    var store_id = params.get("store_id");
    $("#src_store_id").val(store_id)
  }

  // 確認申請
  $("#btnApprove").on('click', function() {
    var store_id = $("#src_store_id").val();
    // call ajax 傳送資料
    var url = "/member/approveStore/";
    var token = $('input[name=csrfmiddlewaretoken]').val();    
    var para = {
      'csrfmiddlewaretoken':token,
      'store_id':store_id};
  
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