function rnd(n, m){
    return Math.floor(Math.random()*(m-n+1)+n)
}
var rotateFn = function (angles, txt){
	$('#rotate').stopRotate();
	$('#rotate').rotate({
		angle:0,
		animateTo:angles+1800,
		duration:8000,
		callback:function (){
			alert(txt);
		}
	})
};
function lottery(item){
	var angle = rnd(3,57)
	switch (item) {
		case 2:
		angle += 30;
			rotateFn(angle, '10积分');
			break;
		case 4:
			angle += 90;
			rotateFn(angle, '0.8元现金');
			break;
		case 3:
			angle += 150;
			rotateFn(angle, '50积分');
			break;
		case 5:
			angle += -150;
			rotateFn(angle, '2元现金');
			break;
		case 1:
			angle += -90;
			rotateFn(angle, '谢谢参与');
			break;
		case 6:
			angle += -30;
			rotateFn(angle, 'iPhone');
			break;
	}
}
$(function (){
	var rotateTimeOut = function (){
        $('#rotate').rotate({
            angle:0,
            animateTo:2160,
            duration:8000,
            callback:function (){
                
            }
        });
    };
    var bRotate = false;
    $('.pointer').click(function (){
		$.ajax({
			url: get_lottery_url,
			dataType:"json",
			type:"post",
			success:function(ret){
				if(ret.code==-1){
					alert("请先登录！")
					window.location.href = ret.url;
				}
				else if(ret.code==0){
					var itemid = ret.itemid
					itemid = parseInt(itemid)
					lottery(itemid);
				}
				else{
					alert(ret.res_msg);
				}
			},
			error:function(){
				alert('网络超时，请检查您的网络设置！');
			}
        });
    });


});
