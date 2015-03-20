$(document).ready(function(){


	var is_keyboard = false;
	var initial_screen_size = window.innerHeight;


	var size = $(window).width() + "px " + $(window).height() + "px";

	$('.ui-body-c').css ({
		'background-size' : size
        
    	});


function updateViews() {

	$('#content').css({
	        position: 'relative',
                left: ($(window).width() - $('#content').outerWidth()) / 1.4,
                top:'20px'
        });
}


     $(window).resize(function(){
        
		$('#content').css({
			position: 'relative',
			//display: 'inline',//mostramos el elemento
			left: ($(window).width() - $('#content').outerWidth()) / 1.4,
			top: ($(window).height() - 39 - $('#content').outerHeight()) / 2
		});

		is_keyboard = (window.innerHeight < initial_screen_size);
		if (is_keyboard){
	 		updateViews();
		}

    });

// Ejecutamos la función
$(window).resize();
 

});
