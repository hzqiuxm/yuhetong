$(function(){
	// body...
	$(".serviceType").change(function(){
		var va=$(this).children('option:selected').val();
			/*for(var i=1;i<=4;i++){
				if(i==va){

				}
			}*/
		if(va==1){
			$(".qyzl").css('display','none');
			$(".zscq").css('display','none');
			$(".gsjy").css('display','none');
			$(".ldrs").css('display','inline');
		}
		else if(va==2){
			$(".zscq").css('display','none');
			$(".gsjy").css('display','none');
			$(".ldrs").css('display','none');
			$(".qyzl").css('display','inline');
		}
		else if(va==3){
			$(".qyzl").css('display','none');
			$(".gsjy").css('display','none');
			$(".ldrs").css('display','none');
			$(".zscq").css('display','inline');
		}
		else {
			$(".qyzl").css('display','none');
			$(".zscq").css('display','none');
			$(".ldrs").css('display','none');
			$(".gsjy").css('display','inline');
		}
	})

	$(".page_num").click(function(){
		//this.style.color = 'black';
     	//this.style.cursor = 'default';     default 默认鼠标
     	//$(this).removeClass("page_num");
     	//$(this).addClass("page_num_click");
     	$(".page_num_click").removeClass("page_num_click").addClass("page_num");
     	$(this).removeClass('page_num').addClass('page_num_click');
     	//$(this).nextAll().removeClass('page_num_click');
     	//$(this).nextAll().addClass('page_num');
		$(this).bind("click",function(){return false;});
		//$(this).replaceWith("<span></span>");
		//var a=$(this).attr("value");
		//$(this).replaceWith('<span>'+$(this).attr("value")+'</span>');
	})





	








})