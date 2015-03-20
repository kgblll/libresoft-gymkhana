"use strict";

function Gymkhana()
{

    


$( "form" ).submit(function( event ) {
//	event.preventDefault();
    var password = $('#password').val();
    var passwordC = $('#passwordC').val();
    if (password != passwordC){
	$('p').html("Las contraseñas no coinciden.").css("color", "red");
    }
	
});

	this.start = function()
	{
	
	};


}



$(function() {
	window.app = new Gymkhana();
	window.app.start();

});


