"use strict";

function Play()
{
    //var version = "v1.3";
    var usuario;
    var gymkhana;

    
    
    function validarDatos (login, password)
    {     
      //  window.alert("Enviariamos: " + login + " + " + password);
        return true;
    }

	this.start = function()
	{
		
		$("#id").click(function() {
			usuario = $(this).text()
			//alert(usuario);
			window.open("gymkhanas.html","_self")
			
			
		
		});
		
		$("#g").click(function() {
			gymkhana = $(this).text()
			//alert(usuario + " " + gymkhana);		// usuario es undefinido -> porque vuelve ha crear play
			window.open("inicio_g.html","_self")
			
			
		
		});
		
		$("#registrar").click(function() {
			//window.alert("uuuuuuuuuu");
			// recopilar datos introducidos
			
            window.open("registrar.html","_self")
            
		
		});
		//.focus();
		
		//$("#app header").append(version);        // no lo va a hacer porque no tenemos header (en comentarios)

	};

}


$(function() {
	window.app = new Play();
	window.app.start();
});
