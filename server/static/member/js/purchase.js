
$(document).ready(function () {
  getPara();

  function getPara(){
    let url = new URL(location.href);
    let params = url.searchParams;
    var group = params.get("group");
    $("#group").val(group);
    var staff = params.get("staff");
    $("#staff").val(staff);
  }

  // get city
  // $('#inputCountry').change(function(){
  //   var country_id = $('#inputCountry').val();
  //   var para = {'country_id':country_id}
  //   var url = "/member/get_city_data"

  //   $.ajax({
  //     type: 'GET',
  //     url: url, 
  //     data: para,
  //     dataType: 'json',
  //     success: function(data_get){
  //       var citys = data_get['citys']
  //       $.each(citys, function (i, item)
  //       {
  //           $('#inputCity').append($('<option></option>').val(item.id).text(item.city_name));
  //       });
  //     },
  //     error: function () {
  //       $('#inputCity').empty().append($('<option></option>').val('').text('==選擇縣市=='));
  //       alert('查詢異常，請通知工程師處理。')
  //     }
  //   })
  // })

  // // get city
  // $('#inputCity').change(function(){
  //   var city_id = $('#inputCity').val();
  //   var para = {'city_id':city_id}
  //   var url = "/member/get_area_data"

  //   $.ajax({
  //     type: 'GET',
  //     url: url, 
  //     data: para,
  //     dataType: 'json',
  //     success: function(data_get){
  //       var areas = data_get['areas']
  //       $.each(areas, function (i, item)
  //       {
  //           $('#inputZip').append($('<option></option>').val(item.id).text(item.area_name));
  //       });
  //     },
  //     error: function () {
  //       $('#inputZip').empty().append($('<option></option>').val('').text('==選擇區域=='));
  //       alert('查詢異常，請通知工程師處理。')
  //     }
  //   })
  // })

  // 新增購買資訊(old)
  // $("#btnSave").on('click', function() {
  //   var group = $("#group").val();
  //   var staff = $("#staff").val();
  //   var buyer_name = $("#inputName").val();
  //   var phone = $("#inputPhone").val();
  //   var country = $("#inputCountry").val();
  //   var city = $("#inputCity").val();
  //   var area = $("#inputZip").val();
  //   var address = $("#inputAdress").val();
  //   var email = $("#inputEmail").val();
  //   var memo = $("#inputMemo").val();
  //   var amount = 258;
  //   檢查欄位是否有缺
  //   if (buyer_name == '') {
  //     alert("請輸入姓名!!");
  //   } else {
  //     if (phone == '' ) {
  //       alert("請輸入行動電話!!");
  //     } else {
  //       if (country == ''||city == ''||area == '') {
  //         alert("請選擇地區!!");
  //       } else {
  //         if (address=='') {
  //           alert("請輸入詳細地址!!");
  //         } else {
  //           var url = "/member/purchase/";

  //           var token = $('input[name=csrfmiddlewaretoken]').val();
        
  //           var para = {
  //             'csrfmiddlewaretoken':token,
  //             'group':group,
  //             'staff':staff,
  //             'buyer_name':buyer_name,
  //             'phone':phone,
  //             'country':country,
  //             'city':city,
  //             'area':area,
  //             'address':address,
  //             'email':email,
  //             'memo':memo,
  //             'amount':amount};
        
  //           $.ajax({
  //             url: url, 
  //             data: para,
  //             type: 'POST',
  //             dataType: 'json',
  //             success: function(data_get){
  //               var msg = data_get['msg']
  //               alert(msg);
  //             },
  //             error: function (data_get) {
  //               var msg = data_get['msg']
  //               alert('fail~');
  //             }
  //           });
  //         }
          
  //       }
  //     }
  //   }
  // })

  $("#btnSave").on('click', function() {
    var group = $("#group").val();
    var staff = $("#staff").val();
    var buyer_name = $("#inputName").val();
    var phone = $("#inputPhone").val();
    var account = $("#inputAccount").val();
    var password = $("#inputPwd").val();
    var email = $("#inputEmail").val();
    var memo = $("#inputMemo").val();
    //var amount = 258;
    // 檢查欄位是否有缺
    if (buyer_name == '') {
      alert("請輸入姓名!!");
    } else if (phone == '' ) {
      alert("請輸入行動電話!!");
    } else if (account == '') {
      alert("請輸入帳號!!");
    } else if (password=='') {
      alert("請輸入密碼!!");
    } else if (email=='') {
      alert("請輸入電子郵箱!!");
    } else {
      var url = "/member/purchase/";

      var token = $('input[name=csrfmiddlewaretoken]').val();
  
      var para = {
        'csrfmiddlewaretoken':token,
        'group':group,
        'staff':staff,
        'game_id':'1',
        'buyer_name':buyer_name,
        'phone':phone,
        'account':account,
        'password':password,
        'email':email,
        'memo':memo};
  
      $.ajax({
        url: url, 
        data: para,
        type: 'POST',
        dataType: 'json',
        success: function(data_get){
          var msg = data_get['msg']
          if (msg == '') {
            $("#web").val(data_get['web']);
            $("#MN").val(data_get['MN']);
            $("#OrderInfo").val(data_get['OrderInfo']);
            $("#Td").val(data_get['Td']);
            $("#sna").val(data_get['sna']);
            $("#sdt").val(data_get['sdt']);
            $("#email").val(data_get['email']);
            $("#note1").val(data_get['note1']);
            $("#note2").val(data_get['note2']);
            $("#Card_Type").val(data_get['Card_Type']);
            $("#Country_Type").val(data_get['Country_Type']);
            $("#Term").val(data_get['Term']);
            $("#CargoFlag").val(data_get['CargoFlag']);
            $("#StoreID").val(data_get['StoreID']);
            $("#StoreName").val(data_get['StoreName']);
            $("#BuyerCid").val(data_get['BuyerCid']);
            $("#DonationCode").val(data_get['DonationCode']);
            $("#Carrier_ID").val(data_get['Carrier_ID']);
            $("#ChkValue").val(data_get['ChkValue']);
            var action_url = data_get['url']
            document.orderform.action=action_url;
            document.orderform.submit();
          } else {
            alert(msg);
          }
        },
        error: function (data_get) {
          var msg = data_get['msg']
          alert(msg);
        }
      });
    }
  })
})

$("#btnEnterGame").on('click', function() {
  window.location.href="http://game.anygame989.com/";
})