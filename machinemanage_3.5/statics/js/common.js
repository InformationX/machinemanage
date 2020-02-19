//获取一个月以前的日期
function one_month_ago(){
  let date = new Date()
  date.setMonth(date.getMonth()-1)
  let year = date.getFullYear()
  let month = date.getMonth() + 1
  let day = date.getDate()
  if(month < 10){
    month = '0' + month
  }
  if(day < 10){
    day = '0' + day
  }
  return year + '-' + month + '-' + day
}

//获取今天日期
function getToday(){
	let date = new Date()
	let year = date.getFullYear()
	let month = date.getMonth() + 1
	let day = date.getDate()
  let hours = date.getHours()
  let minutes = date.getMinutes()
  let seconds = date.getSeconds()
  if(month < 10){
    month = '0' + month
  }
  if(day < 10){
    day = '0' + day
  }
  if(hours < 10){
    hours = '0' + hours
  }
  if(minutes < 10){
    minutes = '0' + minutes
  }
  if(seconds < 10){
    seconds = '0' + seconds
  }
	//return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds
  return year + '-' + month + '-' + day
}

//验证输入选项或选择选项是否为空
function vde_is_null(id_list){
  for(let i = 0;i < id_list.length;i++){
    id = id_list[i]
    value = $('#' + id).val()
    tagName = $('#' + id)[0].tagName
    if(value == ''){
      if(tagName == 'INPUT'){
        $('#' + id).focus()
        layer.tips('该选项输入不能为空!', $('#' + id), {
          tips: [3, 'red']
        });
      }else{
        layer.tips('请选择该选项!', $('#' + id).parent(), {
          tips: [3, 'red']
        });
      }
      return false
    }
  }
  return true
}

//获取所有位置
function get_all_pos_data(){
  var str = ''
  $.ajax({
    url:'/nstd/baseinfo/get_all_pos_data',
    type:'get',
    dataType:'json',
    success:function(data){
      str = '<option value="">请选择存放位置:</option>'
      for(let i=0;i<data.data.length;i++){
        str += '<option value="'+ data.data[i].p_code +'">' + data.data[i].p_code + '</option>'
      }
      $('#a_action_loc').html(str)
      $('#a_loc_cd').html(str)
      $('.pos_class').html(str)
      form.render('select')
    }
  });
  return str
}

//获取所有部门
function get_all_depart(depart_id){
  var str = ''
  $.ajax({
    url:'/nstd/baseinfo/search_depart',
    type:'get',
    dataType:'json',
    success:function(data){
      depart_list = data.depart_list
      str = '<option value="">请选择部门:</option>'
      for(let i=0;i<depart_list.length;i++){
        //str += '<option value="'+ depart_list[i].id +'">' + depart_list[i].d_name + '</option>'
        str += '<option>' + depart_list[i].d_name + '</option>'
      }
      $('#' + depart_id).html(str)
      $('.depart_class').html(str)
      form.render('select')
      return str
    }
  });
  return str
}

//显示或隐藏下拉框选项
function show_hid_slide(obj){
  let hidLen = 0
  let ddLen = $(obj).next().next().find('dd').length
  let value = $(obj).val()
  if(value != ''){
    $(obj).next().next().find('dd').each(function(){
      let text = $(this).text()
      if(text.indexOf(value) == -1){
        $(this).addClass('hid')
        hidLen ++
      }else{
        $(this).removeClass('hid')
        hidLen --
      }
    })
    if(hidLen == ddLen){
      $(obj).next().next().addClass('hid')
    }else{
      $(obj).next().next().removeClass('hid')
    }
  }else{
    $(obj).next().next().removeClass('hid')
    $(obj).next().next().find('dd').each(function(){
      $(this).removeClass('hid')
    })
  }
}

function dd_mouseover(obj){
  if(!$(obj).hasClass('check-this')){
    $(obj).addClass('bgf2f')
  }
}

function dd_mouseout(obj){
  if($(obj).hasClass('bgf2f')){
    $(obj).removeClass('bgf2f')
  }
}

function dd_click(obj){
  $(obj).siblings().each(function(){
    if($(this).hasClass('check-this')){
      $(this).removeClass('check-this')
    }
  })
  if(!$(obj).hasClass('check-this')){
    $(obj).addClass('check-this')
  }
  text = $(obj).text()
  value = $(obj).attr('lay-value')
  if(value != ''){
    let input = $(obj).parent().prev().prev()
    $(input).attr('lay-value',value)
    $(input).val(text)
    $(obj).parent().addClass('hid')
  }
}

//显示自定义下拉框
function showSlide(obj){
  $(obj).next().removeClass('icon1').addClass('icon2')
  $(obj).next().next().removeClass('hid')

  show_hid_slide(obj)
}
//隐藏自定义下拉框
function hideSlide(obj){
  setTimeout(function(){
    $(obj).next().removeClass('icon2').addClass('icon1')
    $(obj).next().next().addClass('hid')
  },200)
}

//重新加载下拉框选项
function reloadSlide(obj){
  let value = $(obj).val()
  let idName = $(obj).attr('id')

  if(idName == 'a_supplier' || idName == 'a_action_supplier'){
    url = '/nstd/baseinfo/search_supplier'
  }else if(idName == 'a_category'){
    url = '/nstd/baseinfo/search_category'
  }else if(idName == 'a_action_user'){
    url = '/nstd/baseinfo/search_action_user'
  }else if(idName == 'a_action_charge'){
    url = '/nstd/baseinfo/search_action_charge'
  }else if(idName == 'a_action_depart'){
    url = '/nstd/baseinfo/search_depart'
  }else if(idName == 'a_client'){
    url = '/nstd/baseinfo/search_client'
  }

  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function(data){
      data_list = data.data_list
      str = ''
      for(let i=0;i<data_list.length;i++){
        let id = data_list[i].id
        let name = data_list[i].name
        if(name == value){
          str += '<dd lay-value="'+ id +'" class="dd check-this" onmouseover="dd_mouseover(this)" onmouseout="dd_mouseout(this)" onclick="dd_click(this)">'+ name +'</dd>'
        }else{
          str += '<dd lay-value="'+ id +'" class="dd" onmouseover="dd_mouseover(this)" onmouseout="dd_mouseout(this)" onclick="dd_click(this)">'+ name +'</dd>'
        }
      }
      $('#' + idName).next().next().html(str)
    }
  })
}

//根据输入数据搜索下拉框
function searchDown(obj){
  show_hid_slide(obj)
  let value = $(obj).val()
  let keyCode = window.event.keyCode
  if(keyCode == 13){
    let idName = $(obj).attr('id')
    if(idName == 'a_supplier' || idName == 'a_action_supplier'){
      url = '/nstd/baseinfo/add_supplier'
      data = {a_supplier:value}
    }else if(idName == 'a_category'){
      url = '/nstd/baseinfo/add_category'
      data = {a_category:value}
    }else if(idName == 'a_action_user'){
      url = '/nstd/baseinfo/add_action_user'
      data = {u_name:value}
    }else if(idName == 'a_action_charge'){
      url = '/nstd/baseinfo/add_action_charge',
      data = {c_name:value}
    }else if(idName == 'a_action_depart'){
      url = '/nstd/baseinfo/add_depart'
      data = {d_id:0,d_name:value}
    }else if(idName == 'a_client'){
      url = '/nstd/baseinfo/add_client'
      data = {c_name:value}
    }

    if(value != ''){
      //验证输入项是否已在下拉列表内
      let flag = false  //默认输入选项不在下拉列表内
      $(obj).next().next().find('dd').each(function(){
        let this_text = $(this).text().trim()
        if(value == this_text){
          flag = true
        }
      });
      if(!flag){
        layer.confirm('您确定要添加：' + value + '吗？',{title:'温馨提示',icon:3},
          function(index, layero){
            $.ajax({
              url: url,
              data: data,
              type: 'get',
              dataType: 'json',
              success: function(data){
                if(data.result){
                  layer.msg('添加成功',{icon:1})
                  reloadSlide(obj)
                }else{
                  layer.alert('添加失败',{title:'温馨提示',icon:2})
                }
              },
              error: function(xmlHq,status,errorThrow){
                console.log(errorThrow)
              }
            });
          },
          function(index){
            layer.msg('操作取消')
          }
        );
      }else{
        layer.alert(value + '不能重复录入!',{title:'温馨提示',icon:7})
      }
    }
  }
}