var $table = $('#table1')

$(function() {

  $table.bootstrapTable({
    striped: true,                      //是否显示行间隔色
    cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    pagination: true,   //是否显示分页（*）
    pageNumber:1,   //初始化加载第一页，默认第一页
    pageSize: 10,   //每页的记录行数（*）
    pageList: [10, 20, 30, 40, 50, 60, 70, 80, 90], //可供选择的每页的行数（*）
    paginationParts: ['pageList', 'pageInfoShort', 'pageSize'],
    paginationHAlign: "right",
    paginationDetailHAlign: "left",
    smartDisplay: false,
    paginationShowPageGo: false,
    sortable: false,   //是否启用排序
    sortOrder: "asc",   //排序方式
    clickToSelect: false,  //是否启用点击选中行
    uniqueId: "id",   //每一行的唯一标识，一般为主键列
    classes:"table table-hover table-sm table-bordered text-center table-striped",
    theadClasses: "thead-dark",
    columns: [{field: 'id', title: 'ID', visible: false}, 
              {field: 'group', title: '群組'}, 
              {field: 'staff', title: '網紅'}, 
              {field: 'count', title: '成功下載次數'}, 
              {field: 'amount', title: '下載金額'}]
  })

  // get staff
  $('#inGroup').change(function(){
    var group_id = $('#inGroup').val();
    var para = {'group_id':group_id}
    var url = "/member/getStaffInfo"

    $.ajax({
      type: 'GET',
      url: url, 
      data: para,
      dataType: 'json',
      success: function(data_get){
        var staffs = data_get['staffs']
        $.each(staffs, function (i, item)
        {
            $('#inStaff').append($('<option></option>').val(item.id).text(item.nick_name));
        });
      },
      error: function () {
        $('#inStaff').empty().append($('<option></option>').val('').text('==選擇網紅=='));
        alert('查詢異常，請通知工程師處理。')
      }
    })
  })

  $("#btnQuery").on('click', function() {
    var group = $("#inGroup").val();
    var staff = $("#inStaff").val();
    var para = {'group':group, 'staff':staff}
    var url = "/member/report1"
    
    $.ajax({
      type: 'GET',
      url: url, 
      data: para,
      dataType: 'json',
      success: function(data_get){
        var rs1 = data_get['rs1'];
        $table.bootstrapTable('load',rs1);
        $table.bootstrapTable('refresh');
      },
      error: function () {
        $table.bootstrapTable('destroy');
        alert('查詢異常，請通知工程師處理。')
      }
    })
  })

})
