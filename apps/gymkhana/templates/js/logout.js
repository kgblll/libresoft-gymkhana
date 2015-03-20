function Logout()
{
    var version = "v1.3";

    function setStatus(message)
    {
        $("#app>footer").text(message);
    }
    
	this.start = function()
	{
		
		//alert("nos salimos");
		$("a.boton").click(function(){

			
		
		
		
		});
		//.focus();
		
		//$("#app header").append(version);        // no lo va a hacer porque no tenemos header (en comentarios)
		
		setStatus("ready esto es el pie de página");
	};

}


$(function() {
	window.app = new Logout();
	window.app.start();
});


jQuery(document).ready(function() {
 //   alert('Window height: ' + jQuery(window).height()); // returns the height of    the viewport
 //   alert('Window width: ' + jQuery(window).width()); // returns the width of the    viewport
//    alert('Document height: ' + jQuery(document).height()); // returns the height    of the document
//    alert('Document width: ' + jQuery(document).width()); // returns the width of    the document
    });




//$(handler);
