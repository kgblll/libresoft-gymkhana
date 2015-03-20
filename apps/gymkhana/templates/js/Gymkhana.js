"use strict";

function Gymkhana()
{

    function validarDatos (login, password)
    {     
      //  window.alert("Enviariamos: " + login + " + " + password);
      //console.log("hola");
      /*
      var dataString = 'name1=' + name + '&email1=' + email + '&password1=' + password + '&contact1=' + contact;
      $.ajax({
		type: "POST",
		url: "ajaxjs.php",
		data: dataString,
		cache: false,
		success: function(html) {
			alert(html);
		}
	  });*/
      
      
        return true;
    }

	this.start = function()
	{
	
		$('form').submit(function(event){
			var login = $('#new-login').val();
			var password = $('#new-password').val();
			var usuario = validarDatos(login, password);
			//alert(usuario);
			window.open('menu.html', '_self');
});

/*	
		$("#enter").click(function() {
			//window.alert("uuuuuuuuuu");
			// recopilar datos introducidos
			var login = $('#new-login').val();
            var password = $('#new-password').val();
        //    window.alert(login + " + " + password);
        //    window.alert(password);
            var usuario = validarDatos(login, password);
        //    window.alert(usuario);
            window.open("menu.html","_self")
            
		
		});

*/
		$("#registrar").click(function() {
			//window.alert("uuuuuuuuuu");
			// recopilar datos introducidos
			
            window.open("registrar.html","_self")
            
		
		});

	};

}


$(function() {
	window.app = new Gymkhana();
	window.app.start();
});


jQuery(document).ready(function() {

    });

