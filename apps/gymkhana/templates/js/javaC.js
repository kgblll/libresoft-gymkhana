$(document).ready(function(){

	
	$(window).resize(function(){
		
		var heightBlockA = $('.ui-block-a #blockA').height();
		var heightBlockB = $('.ui-block-b #blockB').height();


		if (heightBlockA >= heightBlockB){
			$('.ui-block-a #blockA').css({
				height: heightBlockB,
				position :'absolute',
				top : '134px',
				'overflow-y': 'scroll'
			});
		}else{
			$('.ui-block-a #blockA').css({
				height: '77%',
				top : '120px',
				position : 'fixed',
				'overflow-y' : 'auto'
			});
			
		}
	});
	
$(window).resize();

    

});

