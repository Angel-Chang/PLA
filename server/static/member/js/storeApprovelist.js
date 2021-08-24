
var $table1 = $('#table1')

$(function() {
  $table1.bootstrapTable({
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
    sortable: true,   //是否启用排序
    sortOrder: "asc",   //排序方式
    clickToSelect: false,  //是否启用点击选中行
    uniqueId: "store_id",   //每一行的唯一标识，一般为主键列
    classes:"table table-hover table-sm table-bordered text-center table-striped",
    theadClasses: "thead-dark",
    columns: [{field: 'store_id', title: '店家ID', visible: false},
              {field: 'member_id', title: '會員ID', formatter: idFormatter}, 
              {field: 'store_name', title: '店家名稱'}, 
              {field: 'area', title: '區域'}, 
              {field: 'tel', title: '電話'}, 
              {field: 'address', title: '地址'}, 
              {field: 'created_date', title: '註冊時間'}, 
              {field: 'is_approved', title: '確認狀態', formatter: stateFormatter}]
  })

  function idFormatter(value, row, index) {
    return [
      '<button type="button" class="showstore btn btn-sm btn-white border-0 text-blue"' +
      'data-id=' + row.store_id ,
      ' ">' + value +'</button>'
    ].join('');

  }

  function stateFormatter(value, row, index) {
    ptype = row.permission_type
    if (value == '1') {          // 鎖定
      return '<span class="text-primary">已確認</span>';
    } else {
      return '<span class="text-danger">尚未確認</span>';
    }
  }

  $('#table1 tbody').on('click','tr td .showstore', function() {
    
    var button = $(this);
    var idx = button.data('id');

    var rowdata = $table1.bootstrapTable('getRowByUniqueId', idx);

    var store_id = rowdata.store_id;
    var url = "/member/storeDetail?store_id="+store_id;
    location.href = url;

  })

  $("#btnQuery").on("click", function() {
    var startTime1 = $("#startTime1").val();
    var endTime1 = $("#endTime1").val();
    var args = $("#args").val();
    var para = {'startTime1':startTime1, 
                'endTime1':endTime1,
                'args':args};
    var url = "/member/storeApprovelist/";

    $.ajax({
      type: 'GET',
      url: url, 
      data: para,
      dataType: 'json',
      success: function(data_get){
        var rs1 = data_get['rs1'];
        $table1.bootstrapTable('load',rs1);
        $table1.bootstrapTable('refresh');
      }
    })
  })
})
