$(document).ready(function(){

     $(window).resize(function(){
        
		var middleHeight = $(window).height() - $('.ui-footer').height() - $('.ui-header').height();
		$('#medio').css({
			'margin-top': '10%',
			'margin-bottom':'10%',
			height: middleHeight,
			top:-5
		});
		
		var marginMedio = 2*parseInt($('#medio').css('margin'));
		
		var textHeight = $('#text').height();
		var topText = 2*parseInt($('#text').css('margin-top'));
		var leftText = 3*parseInt($('#text').css('margin-left'));
		
		var buttonHeight = $('#start').height();
		var topButton = 2*parseInt($('#start').css('margin-top'));
		
		
		
		var imageHeight = middleHeight - textHeight - buttonHeight - marginMedio - topText - topButton;
		var imageWidth = $(window).width() - leftText;

		
		
		if (imageHeight > imageWidth){
			$('#image').height(imageWidth);
			$('#image').width(imageWidth);
		}else{
			$('#image').height(imageHeight);
			$('#image').width(imageHeight);
		}
		
		$('.ui-btn-up-c').css({
			left: ($(window).width() - $('.ui-btn-up-c').outerWidth()) / 2.5
		});

        
    });


$(window).resize();
 
});
