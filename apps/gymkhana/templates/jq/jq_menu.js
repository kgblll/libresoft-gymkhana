$(document).ready(function(){

     $(window).resize(function(){

        $('#menu').css({
			//position:'absolute',left: ($(window).width())/2,top: ($(window).height())/3
			//margin: 0, padding: ($(window).height())/4
			//position: 'absolute',
			//height:'0%', 
			//top: ($(window).height())/3.5,
			//left: ($(window).width())/5
			left: ($(window).width() - $('#menu').outerWidth()*2) / 2,
			top: ($(window).height() - $('.ui-footer').height()*2 - $('#menu').outerHeight()) / 2
		});
		

		
        
    });

// Ejecutamos la función
$(window).resize();
 
});
