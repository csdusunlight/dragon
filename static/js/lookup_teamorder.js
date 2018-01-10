$(function() {
	var data = '<table width="100%"><thead><tr><th width="15%">项目</th><th width="15%">投资时间</th>' +
		'<th width="15%">投资金额</th><th width="15%">状态<th width="25%">备注</th><th width="15%">操作</th></tr></thead><tbody>' +
		'[results]<tr><td>{project_title}</td><td class="date1">{invest_date}</td><td class="amount1">{invest_amount}</td><td>{state_desc}</td><td class="remark1">{remark}</td><td class="change" data-id="{id}" data-state="{audit_state}"></td></tr>[/results]' +
		'</tbody></table>';

	var passData = '<table width="100%"><thead><tr><th width="20%">项目</th><th width="20%">投资时间</th>' +
		'<th width="20%">投资金额</th><th width="15%">状态<th width="15%">备注</th><th width="10%">操作</th></tr></thead><tbody>' +
		'[results]<tr><td>{project_title}</td><td>{invest_date}</td><td>{invest_amount}</td><td>{state_desc}</td><td>{remark}</td><td><a data-id="{id}" class="look">查看</a></td></tr>[/results]' +
		'</tbody></table>';

	var auditData = '<table width="100%"><thead><tr><th width="15%">项目</th><th width="15%">投资时间</th>' +
		'<th width="15%">投资金额</th><th width="15%">状态<th width="25%">备注</th><th width="15%">操作</th></tr></thead><tbody>' +
		'[results]<tr><td>{project_title}</td><td class="date2">{invest_date}</td><td class="amount2">{invest_amount}</td><td>{state_desc}</td><td class="remark2">{remark}</td><td><a data-id="{id}" class="aChange">修改</a>丨<a data-id="{id}" class="aDelete">删除</a></td></tr>[/results]' +
		'</tbody></table>';

	var refuseData = '<table width="100%"><thead><tr><th width="20%">项目</th><th width="20%">投资时间</th>' +
		'<th width="20%">投资金额</th><th width="15%">状态<th width="25%">备注</th></tr></thead><tbody>' +
		'[results]<tr><td>{project_title}</td><td>{invest_date}</td><td>{invest_amount}</td><td>{state_desc}</td><td>{remark}</td></tr>[/results]' +
		'</tbody></table>';

	function pagecallback() {
		console.log("这是一个回调函数");
		$(".change").each(function() {
			if($(this).attr("data-state") == 1) {
				$(this).html("<a class='lChange'>修改</a>丨<a class='delete'>删除</a>");
			} else if ($(this).attr("data-state") == 0) {
				$(this).html("<a class='look'>查看</a>");
			}else{
				$(this).html("<a>------</a>");
			}
		});
	}
	var url = "/restapi/investlog/?page={page}&pageSize={pageSize}";
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
			var dataUrl = '/restapi/investlog/?page={page}&pageSize={pageSize}';
		} else if(index == 1) {
			var pdata = passData;
			var dataUrl = url + "&audit_state=0";
		} else if(index == 2) {
			var pdata = auditData;
			var dataUrl = url + "&audit_state=1";
		} else if(index == 3) {
			var pdata = refuseData;
			var dataUrl = url + "&audit_state=2";
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
	var parent_dom;
	$(".contentBox").on('click', '.lChange', function() {
		parent_dom = $(this).parent().parent();
		console.log(parent_dom);
		$(".dataBox").empty();
		$(".cMsk").show();
		id = $(this).parent().attr("data-id"); //获取当前tr的id
		$.ajax({
			url: '/restapi/investlog/' + id + '/',
			type: 'GET', //GET 
			async: true, //或false,是否异步
			timeout: 5000, //超时时间
			dataType: 'json', //返回的数据格式：json/xml/html/script/jsonp/text
			success: function(ret) {
				console.log(ret);
				var str_html;
				for(let i in ret) {
					str_html = '<table style="width:100%;">' +
						'<tr><td class="td1">项目</td><td class="t2"><input type="text" value="' + ret.project_title + '"  disabled="disabled" style="width:200px;" /></td></tr>' +
						'<tr><td class="td1">投资日期</td class="t2"><td><input type="date" class="date" value="' + ret.invest_date + '" style="width:222px;" /></td></tr>' +
						'<tr><td class="td1">投资金额</td class="t2"><td><input type="text" class="amount" value="' + ret.invest_amount + '" style="width:200px;" /></td></tr>' +
						'<tr><td class="td1">备注</td><td class="t2"><input type="text" class="remark" value="' + ret.remark + '"  style="width:200px;"/></td></tr>' +
						'</table>';
				}
				$(".dataBox").append(str_html);

			},
			error: function(xhr, textStatus) {
				console.log('错误:' + xhr.responseText);
			}
		});

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
				"invest_date": $(".date").val(),
				"remark": $(".remark").val()
			},
			dataType: 'json',
			success: function(ret) {
				alert("修改成功")
				$(".cMsk").hide();
				console.log(ret);
				$(parent_dom).find(".date1").text(ret.invest_date);
				$(parent_dom).find(".amount1").text(ret.invest_amount);
				$(parent_dom).find(".remark1").text(ret.invest_remark);
			},
			error: function(xhr) {
				console.log(xhr.responseText);
			}
		});

	});
	$(".cancel").click(function() {
		$(".cMsk").hide();
	});
	//删除模态框出现
	var parents;
	$(".contentBox").on("click", '.delete', function() {
		$(".dMsk").show();
		parents = $(this).parent().parent(); //获取当 tr标签
		console.log(parents);
		id = $(this).parent().attr("data-id"); //获取id
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

	//		window.location.reload(); 
	/*********审核中状态修改**********/
	$(".contentBox").on('click', '.aChange', function() {
		parent_dom = $(this).parent().parent();
		$(".aDataBox").empty();
		$(".aMsk").show();
		id = id = $(this).attr("data-id");
		console.log('未审核修改id', id);
		$.ajax({
			url: '/restapi/investlog/' + id + '/',
			type: 'GET', //GET 
			async: true, //或false,是否异步
			timeout: 5000, //超时时间
			dataType: 'json', //返回的数据格式：json/xml/html/script/jsonp/text
			success: function(ret) {
				console.log("数据：", ret);
				var str_html;
				for(let i in ret) {
					str_html = '<table style="width:100%;">' +
						'<tr><td class="td1">项目</td><td class="t2"><input type="text" value="' + ret.project + '" disabled="disabled" style="width:200px;" /></td></tr>' +
						'<tr><td class="td1">投资日期</td class="t2"><td><input type="date" class="date" value="' + ret.invest_date + '" style="width:222px;" /></td></tr>' +
						'<tr><td class="td1">投资金额</td class="t2"><td><input type="text" class="amount" value="' + ret.invest_amount + '" style="width:200px;" /></td></tr>' +
						'<tr><td class="td1">备注</td><td class="t2"><input type="text" class="beizhu" value="' + ret.remark + '"  style="width:200px;"/></td></tr>' +
						'</table>';
				}
				$(".aDataBox").append(str_html);

			},
			error: function(xhr, textStatus) {
				console.log('错误:' + xhr.responseText);
			}
		});

	});
	$(".cSubmit").click(function() {
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
				"invest_date": $(".date").val(),
				"remark": $(".beizhu").val()
			},
			dataType: 'json',
			success: function(ret) {
				alert("修改成功")
				$(".aMsk").hide();
				$(parent_dom).find(".date2").text(ret.invest_date);
				$(parent_dom).find(".amount2").text(ret.invest_amount);
				$(parent_dom).find(".remark2").text(ret.invest_remark);
			},
			error: function(xhr) {
				console.log(xhr.responseText);
			}
		});
	});

	/*********审核中状态删除**********/
	$(".contentBox").on('click', '.aDelete', function() {
		id = $(this).attr("data-id");
		console.log('未审核删除id', id);
		$(".aMsk").show();
		$.ajax({
			url: '/restapi/investlog/' + id + '/',
			type: 'delete', //方式
			async: true, //或false,是否异步
			timeout: 5000, //超时时间
			dataType: 'json', //返回的数据格式：json/xml/html/script/jsonp/text
			success: function(data, textStatus, jqXHR) {
				$(this).parent().parent().remove();
				console.log("删除成功");
				$(".aMsk").hide();
			},
			error: function(xhr, textStatus) {
				console.log('错误:' + xhr.responseText);
			}

		});

	});

	$(".cCancel").click(function() {
		$(".aMsk").hide();
	});

	/***********已通过查看**********/
	$(".contentBox").on('click', '.look', function() {
//		$(".lookMsk").show();
		$(".lookData").empty();
		var id = $(this).attr("data-id");
		$.ajax({
			//				url: '/restapi/backlog/?investlog=2',
			url: '/restapi/backlog/?investlog=' + id,
			type: "get", //提交方式post
			async: true, //是否同步
			timeout: 5000, //超出时间
			dataType: 'json', //返回数据格式Json
			success: function(data) {
//				console.log(data.results.length);
				if(data.results.length == 0) {
					console.log(1)
					alert("暂无数据");
				} else {
					console.log(2)
					$(".lookMsk").show();
					for(var i in data.results) {
						str_html = '<p class="backtime">回款时间：' + data.results[i].back_date + '</p>' +
							'<p class="backamount">回款金额：' + data.results[i].back_amount + '元</p>'
					}
					$(".lookData").append(str_html);
				}

			},
			error: function(xhr, textStatus) {
				console.log('错误:' + xhr.responseText);
			}
		});
	});
	$(".close").click(function() {
		$(".lookMsk").hide();
	})
});