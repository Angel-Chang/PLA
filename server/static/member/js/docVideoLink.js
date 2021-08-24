$(function() {

  $("#btnQuery").on("click", function() {
    var member_id = $("#member_id").val();
    if (member_id == '') {
      alert('請輸入會員ID！')
    } else {
      if(!/^[0-9]+$/.test(member_id)) {
        alert('會員ID格式錯誤，請重新輸入！')
      } else  {    
        var para = {'member_id':member_id};
        var url = "/member/docVideoLink/";

        $.ajax({
          type: 'GET',
          url: url, 
          data: para,
          dataType: 'json',
          success: function(data_get){
            var error = data_get['error'];
            if (error == '')
            {
              var data = data_get['data'];
              var doc_id = data.doc_id;
              var doc_name = data.doc_name;
              var title = data.clinic + '/' + data.title;
              var account = data.account;
              var nick_name = data.nick_name;
              var sex = data.sex;
              var email = data.email;
              var skill = data.skill;
              var experience = data.experience;
              var room_url = data.room_url;
              
              var doc_id_obj = document.getElementById("src_doc_id");
              doc_id_obj.value = doc_id;
              document.getElementById("doc_name").innerHTML= doc_name;
              document.getElementById("title").innerHTML= title;
              document.getElementById("account").innerHTML= account;
              document.getElementById("nick_name").innerHTML= nick_name;
              document.getElementById("sex").innerHTML= sex;
              document.getElementById("email").innerHTML= email;
              document.getElementById("experience").innerHTML= experience;
              var room_url_obj = document.getElementById("room_url");
              room_url_obj.value = room_url;
  
              document.getElementById('div_detail').style.display="block";
            }
            else
            {
              document.getElementById('div_detail').style.display="none";
              alert(error);
            }

          },
          error: function (data_get) {
            var msg = data_get['error']
            alert(msg);
          }
        })
      }
    }
  })

  // 更新醫生視訊連結
  $("#btnUpdate").on('click', function() {
    var doc_id = $("#src_doc_id").val();
    var room = $("#room_url").val();
    // call ajax 傳送資料
    var url = "/member/updateDocVideoLink/";
    var token = $('input[name=csrfmiddlewaretoken]').val();    
    var para = {
      'csrfmiddlewaretoken':token,
      'doc_id':doc_id,
      'room':room};

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
