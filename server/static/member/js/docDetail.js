$(function() {
  getPara();

  function getPara(){
    let url = new URL(location.href);
    let params = url.searchParams;
    var doc_id = params.get("doc_id");
    $("#src_doc_id").val(doc_id)
  }

  // 確認申請
  $("#btnApprove").on('click', function() {
    var doc_id = $("#src_doc_id").val();
    // call ajax 傳送資料
    var url = "/member/approveDoctor/";
    var token = $('input[name=csrfmiddlewaretoken]').val();    
    var para = {
      'csrfmiddlewaretoken':token,
      'doc_id':doc_id};
  
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