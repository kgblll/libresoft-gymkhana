"use strict";

function Gymkhana()
{
	var principal = "";
	var settings = "";
	var $img = $("<img>");
	var canvas = $("canvas")[0];
	var context = canvas.getContext("2d");
    
    function setVar(add){
    	principal = "#principal" + add;
		settings = "#settings" + add;
    }

    
    function hide(option){
    	setVar(option);
    	var footer = $(principal);
		footer.fadeOut("100", function(){
			var set = $(settings);
			set.fadeIn("100");
		});
    }
    
    function show(option){
    	setVar(option);
    	var footer = $(settings);
		footer.fadeOut("100", function(){
			var set = $(principal);
			set.fadeIn("100");
		});
    
    }
    

    function loadImage(url)
	{
		$img.attr("src", url);
		$img[0].onload = function()
		{
			// Ajustamos los limites de la imagen al canvas
			context.drawImage(this, 0, 0, canvas.width, canvas.height);
		}
		$img[0].onerror = function()
		{
			alert("Error al cargar la imagen!");
		}
	}

    


	this.start = function()
	{

		$("#opcionesC").click(function() {		hide("C");  });
		$("#exitSettingsC").click(function() {	show("C");	});
		$("#opcionesU").click(function() {		hide("U");  });		
		$("#exitSettingsU").click(function() {	show("U");	});
		$("#opcionesM").click(function() {		hide("M");	});
		$("#exitSettingsM").click(function() {	show("M");	});
		
		$("#send").click(function() {
			window.open("eventoU.html", "_self");
		});

		
		
		
		var takePicture = document.querySelector("#take-picture");

		takePicture.onchange = function (event) {
			// Get a reference to the taken picture or chosen file
			var files = event.target.files,
				file;
			if (files && files.length > 0) {
				file = files[0];
				var reader = new FileReader();		// Para leer los datos del file (imagen)
		        reader.onload = function() { loadImage(reader.result); };	// cuando se haya cargado la imagen
		        reader.readAsDataURL(file);   //Lee el contenido del archivo en una cadena URL datos. Se puede utilizar esto como la dirección URL para la carga de una imagen.  
			}
		};


		
	};

}


$(function() {
	window.app = new Gymkhana();
	window.app.start();
});

