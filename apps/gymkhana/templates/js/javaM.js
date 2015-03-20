$(document).ready(function(){
	
	$(window).resize(function(){
	
		var height = $(window).height();
		var width = $(window).width();
		var newHeight = $('mobile #wrapper').height();
                var top = newHeight / 2;

		
		if (height < width){
		// Horizontal screen

			$('.mobile #wrapper').css({
				top: top/1.5,
				'transform' : 'scale(1.5)',
				'-moz-transform': 'scale(1.5)',
				'-webkit-transform': 'scale(1.5)',
				'-o-transform': 'scale(1.5)',
				'-ms-transform' : 'scale(1.5)',
				width:'40%'	
			});
			
			$('mobile .ui-footer').css({
				'position': 'absolute',
				bottom : -newHeight/1.5
			});
			
			$('mobile nav.slide-menu-left a').css({
				'font-size': '28px'
			});

		}
		else{
		// Vertical screen

			$('mobile #wrapper').css({
				top: top + 50,
				'-moz-transform': 'scale(2)',
				'-webkit-transform': 'scale(2)',
				'-o-transform': 'scale(2)',
				'-ms-transform' : 'scale(2)',
				'transform' : 'scale(2)',
				width:'40%',
				//'margin-top' : '140px'
			});

			$('mobile .ui-footer').css({
                                'position': 'absolute',
                                bottom : -newHeight
                        });
			
			$('mobile nav.slide-menu-left a').css({
				'font-size': '48px'
			});
		
		}
	
	
	});
	
$(window).resize();

/////////////////

// Slide the menu

    
	var slideLeft = document.querySelector( ".toggle-slide-left" );
 	slideLeft.addEventListener( "click", function(){
	        $("nav").toggleClass("show-menu");

	});

	var closeMenu = document.querySelector( ".close-menu" );
	closeMenu.addEventListener( "click", function(){
        	$("nav").toggleClass("show-menu");
	});


});

