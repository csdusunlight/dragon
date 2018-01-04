$(function() {
	var data = '<table width="100%"><thead><tr><th width="15%">项目</th><th width="15%">投资时间</th>' +
		'<th width="15%">投资金额</th><th width="15%">状态<th width="25%">备注</th><th width="15%">修改</th></tr></thead><tbody>' +
		'[results]<tr><td>{project}</td><td>{invest_date}</td><td>{invest_amount}</td><td>{state_desc}</td><td>{remark}</td><td class="change" data-id="{id}" data-state="{audit_state}"></td></tr>[/results]' +
		'</tbody></table>';

	var passData = '<table width="100%"><thead><tr><th width="20%">项目</th><th width="20%">投资时间</th>' +
		'<th width="20%">投资金额</th><th width="15%">状态<th width="25%">备注</th></tr></thead><tbody>' +
		'[results]<tr><td>{project}</td><td>{invest_date}</td><td>{invest_amount}</td><td>{state_desc}</td><td>{remark}</td></tr>[/results]' +
		'</tbody></table>';

	var auditData = '<table width="100%"><thead><tr><th width="15%">项目</th><th width="15%">投资时间</th>' +
		'<th width="15%">投资金额</th><th width="15%">状态<th width="25%">备注</th><th width="15%">修改</th></tr></thead><tbody>' +
		'[results]<tr><td>{project}</td><td>{invest_date}</td><td>{invest_amount}</td><td>{state_desc}</td><td>{remark}</td><td><a>修改</a>丨<a>删除</a></td></tr>[/results]' +
		'</tbody></table>';

	var refuseData = '<table width="100%"><thead><tr><th width="20%">项目</th><th width="20%">投资时间</th>' +
		'<th width="20%">投资金额</th><th width="15%">状态<th width="25%">备注</th></tr></thead><tbody>' +
		'[results]<tr><td>{project}</td><td>{invest_date}</td><td>{invest_amount}</td><td>{state_desc}</td><td>{remark}</td></tr>[/results]' +
		'</tbody></table>';

	function pagecallback() {
		console.log("这是一个回调函数");
		$(".change").each(function() {
			if($(this).attr("data-state") == 1) {
				$(this).html("<a class='lChange'>修改</a>丨<a class='delete'>删除</a>");
			} else {
				$(this).html("<a>------</a>");
			}
		});
	}
	var url = "/restapi/investlog/";
	$("#pagedata").ajaxPage({
		url: url,
		pageId: $("#page"),
		pageSize: 6,
		run: true,
		content: data,
		complete: pagecallback,
	});

	$(".oprateBox>li").click(function() {
		var index = $(this).index();
		console.log(index);
		$(this).addClass("active").siblings().removeClass("active");
		if(index == 0) {
			var pdata = data;
			var dataUrl = url;
		} else if(index == 1) {
			var pdata = passData;
			var dataUrl = url + "?audit_state=0";
		} else if(index == 2) {
			var pdata = auditData;
			var dataUrl = url + "?audit_state=1";
		} else if(index == 3) {
			var pdata = refuseData;
			var dataUrl = url + "?audit_state=2";
		}
		$("#page").empty();
		$("#pagedata").ajaxPage({
			url: dataUrl,
			pageId: $("#page"),
			pageSize: 6,
			run: true,
			content: pdata,
			complete: pagecallback,
		});
	});

	/*************修改模态框*************/
	var id;
	$(".contentBox").on('click', '.lChange', function() {
		$(".dataBox").empty();
		$(".cMsk").show();
		id = $(this).parent().attr("data-id"); //获取当前tr的id
		$.ajax({
			url: '/restapi/investlog/',
			type: 'GET', //GET 
			async: true, //或false,是否异步
			timeout: 5000, //超时时间
			dataType: 'json', //返回的数据格式：json/xml/html/script/jsonp/text
			success: function(data, textStatus, jqXHR) {
				console.log("数据：", data.results);
				for(let i in data.results) {
					str_html = '<table style="width:100%;">' +
						'<tr><td class="td1">项目</td><td class="t2"><input type="text" value="' + data.results[i].project + '" disabled="disabled" style="width:200px;" /></td></tr>' +
						'<tr><td class="td1">投资日期</td class="t2"><td><input type="date" class="date" value="' + data.results[i].invest_date + '" style="width:222px;" /></td></tr>' +
						'<tr><td class="td1">投资金额</td class="t2"><td><input type="text" class="amount" value="' + data.results[i].invest_amount + '" style="width:200px;" /></td></tr>' +
						'<tr><td class="td1">备注</td><td class="t2"><input type="text" value="' + data.results[i].remark + '"  style="width:200px;"/></td></tr>' +
						'</table>';
				}
				$(".dataBox").append(str_html);

			},
			error: function(xhr, textStatus) {
				console.log('错误:' + xhr.responseText);
			}
		});

	});

	$(".cancel").click(function() {
		$(".cMsk").hide();
	});

	//数据修改
	$(".submit").click(function() {
		console.log("当前修改数据的id：", id);
		if(!$(".date").val() || !$(".amount").val()) {
			alert("输入框不能为空！");
		}
		$.ajax({
			type: "put",
			url: '/restapi/investlog/' + id + '/',
			async: true,
			timeout: 5000,
			data: {
				"invest_amount": $(".amount").val(),
				"invest_date": $(".date").val()
			},
			dataType: 'json',
			success: function(ret) {
				console.log(ret);
				alert("修改成功")
				$(".cMsk").hide();
			},
			error: function(xhr) {
				console.log(xhr.responseText);
			}
		});

	});

	//删除模态框出现
	var parents;
	$(".contentBox").on("click", '.delete', function() {
		$(".dMsk").show();
		parents = $(this).parent().parent(); //获取当 tr标签
		console.log(parents);
		id = $(this).parent().attr("data-id");
	});

	$("#delete").click(function() {
		console.log("当前节点" + parents);
		console.log("当前ID", id);
		$.ajax({
			url: '/restapi/investlog/' + id + '/',
			type: 'delete', //方式
			async: true, //或false,是否异步
			timeout: 5000, //超时时间
			dataType: 'json', //返回的数据格式：json/xml/html/script/jsonp/text
			success: function(data, textStatus, jqXHR) {
				parents.remove();
				console.log("删除成功");
				$(".dMsk").hide();
			},
			error: function(xhr, textStatus) {
				console.log('错误:' + xhr.responseText);

			}

		});
	});

	//删除模态框消失
	$("#cancel1").click(function() {
		$(".dMsk").hide();
	});

});