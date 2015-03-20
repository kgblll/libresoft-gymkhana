$(document).ready(function(){

    var principal = "";
    var settings = "";
    var id;

    
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

    
     $(window).resize(function(){
     
     
     	var var2 = $(window).height() - 39 - 84 -110;		// 34 footer y 84 header
	$('#mapholder').css({
		width:$(window).outerWidth()-40,
		height:var2
	});
		

	$('#contentM').css({
		position:'relative',
		top:($(window).height() - 39 - 84 - 264 - 100) / 2		// #contentM = 264
	});
		
     });

	function GetDistance(Olat, Olon, Dlat, Dlon)
        {

		var x1=new google.maps.LatLng(Olat, Olon);
		var x2=new google.maps.LatLng(Dlat,Dlon);
		var distancia = google.maps.geometry.spherical.computeDistanceBetween(x1, x2);

		return distancia;
        }

	function showPosition(position)
	{
	  	///// Posicion del usuario
		var lat=position.coords.latitude;
		var lon=position.coords.longitude;
		$('#latitude').val(lat);
		$('#longitude').val(lon);
                $('#latitude2').val(lat);
                $('#longitude2').val(lon);

		var cnv = $('#mapholder').text();
		if (cnv != ""){
			clearInterval(id);
		}

		var type =  $('#type_challenge').text();
		if (type == 3){

			var Dlat = $('#Dlatitude').text();
			var Dlon = $('#Dlongitude').text();
			var distance_ch = $('#distance').text();
			var distance = GetDistance(lat, lon, Dlat, Dlon);
			var meters = distance.toString();
			$('#meters').html(meters.slice(0,5));
			if (distance < distance_ch){
				alert("JQ¡Ha alcanzado su destino!");
				$('#dist_difference').val(distance);
				$('form#ub').submit(); 

			}
		}
		
	}

        function showError(error) {
                // the current position could not be located
                alert("No se pudo encontrar su posición.");
		$('#challenge').hide();
		$('#reload').css('display', 'block');
		clearInterval(id);

 	}       

	function Posicion()
	{
		if (navigator.geolocation)
		{
			navigator.geolocation.getCurrentPosition(showPosition, showError);
		}
		else{alert("Geolocation is not supported by this browser.");}
	}


    function loadImage(url)
    {
        var $img = $("<img>");
        $img.attr("src", url);
        $img[0].onload = function()
        {
                var canvas = $("canvas")[0];
                var context = canvas.getContext("2d");
                // Ajustamos los limites de la imagen al canvas
                context.drawImage(this, 0, 0, canvas.width, canvas.height);
        }
        $img[0].onerror = function()
        {
                alert("Error al cargar la imagen!");
        }
    }


// Ejecutamos la función
$(window).resize();
Posicion();
id = setInterval(Posicion, 7000);
 
//Para el menu de settings
$("#opcionesC").click(function() {	hide("C");  });
$("#exitSettingsC").click(function() {	show("C");  });
$("#opcionesU").click(function() {	hide("U");  });		
$("#exitSettingsU").click(function() {	show("U");  });
$("#opcionesM").click(function() {	hide("M");  });
$("#exitSettingsM").click(function() {	show("M");  });


//Photo
var takePicture = document.querySelector("#take-picture");

takePicture.onchange = function (event) {
	// Get a reference to the taken picture or chosen file
	var files = event.target.files,
	file;
	if (files && files.length > 0) {
		file = files[0];
		var reader = new FileReader();
                reader.onload = function() { loadImage(reader.result); };
                reader.readAsDataURL(file);
        }
};


});

