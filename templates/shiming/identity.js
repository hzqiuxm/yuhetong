//function dele(dom){
//	$(dom).parents("li").remove();
//	//alert($(dom).attr("id"));
//};

//function upl(){
//	$('#scan').append('<li><span class="title">文件一</span><span><a href="javascript:void(0);">删除</a>|<a href="javascript:void(0);">重传</a></span></li>');
//};

$(function(){
	$(".link").click(function(){
		$(this).parents("li").remove();
	})

	/*$(".upl").click(function(){
		$("#scan").append('<li><span class="title">文件一</span><span><a class="link" href="javascript:void(0);">删除</a>|<a href="javascript:void(0);">重传</a></span></li>');
		$(".link").click(function(){
		$(this).parents("li").remove();
		})
	})*/

	$(".upl").click(function(){
		var $a = $(this).parent().siblings("ul");
        $a.append('<li><span class="title">文件</span><span><a class="link" href="javascript:void(0);">删除</a>|<a href="javascript:void(0);">重传</a></span></li>');
        $(".link").click(function(){
            $(this).parents("li").remove();
        })
		//$(this).parent().prevUntil("ul").append('<li><span class="title">文件一</span><span><a class="link" href="javascript:void(0);">删除</a>|<a href="javascript:void(0);">重传</a></span></li>');
	})

    //$("#phone_num").keydown(function(){
        /*alert("keyi")*/

   $(".phone_num").focusin(function(){
        document.getElementById("prompt").style.display="inline";
        document.getElementById("ok").style.display="none";
        document.getElementById("no").style.display="none";
        })

    $(".phone_num").focusout(function(){
        var b = $("#phone_num").val();
        document.getElementById("prompt").style.display="none";
        document.getElementById("ok").style.display="none";
        document.getElementById("no").style.display="none";
        if( !!b.match(/^0{0,1}(13[0-9]|15[7-9]|153|156|18[7-9])[0-9]{8}$/) ){
                //document.getElementById("prompt").style.display="none";
            document.getElementById("ok").style.display="inline";
        }
        else{
                //document.getElementById("prompt").style.display="none";
            document.getElementById("no").style.display="inline";
            document.getElementById("prompt").style.display="inline";
        }
    })







})


/*$(function(){
	$("#upl").click(function(){
		alert("你的操作");
	})
});*/




















