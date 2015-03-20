$(document).ready(function(){

     $(window).resize(function(){

		
		//alert($(window).height());
		//alert($('#contentt').outerHeight());
		

	
		if ($(window).height() < $('#content').outerHeight()){
			$('#content').css({
				position: 'relative',
				left: ($(window).width() - $('#content').outerWidth()) / 2,
			//	top: $(".ui-header").height()/2
			});
		
		}
		else{
		
			$('#content').css({
				position: 'relative',
				left: ($(window).width() - $('#content').outerWidth()) / 2,
				top: ($(window).height() - $(".ui-footer").height() - $('#content').outerHeight()) / 2
			});
		}

		
		

    });
    

// Ejecutamos la función
$(window).resize();
 
});
