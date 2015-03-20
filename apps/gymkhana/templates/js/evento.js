var i = 0;
var done = 0;

configurate();

function newMessage(num){


	$('#smsC').replaceWith("<span id='smsC' class='pink'>" + num + "</span>");
        $('#smsU').replaceWith("<span id='smsU' class='pink'>" + num + "</span>")
        $('#smsM').replaceWith("<span id='smsM' class='pink'>" + num + "</span>")
        $('#smsSM').replaceWith("<span id='smsSM' class='pink'>" + num + "</span>")


        var audioElement = document.createElement('audio');
        audioElement.setAttribute('src', '/gymkhana/templates/audio/tone.mp3');
        audioElement.setAttribute('autoplay', 'autoplay');
        audioElement.play();
        

        $(".pink").animate({'opacity':'0.5'}, 1000).animate({'opacity':'1' });
        $(".pink").animate({'opacity':'0.5'}, 1000).animate({'opacity':'1' });

}



function createXMLHttpRequest() {
	// Obtencion del objeto XMLHttpRequest que nos permitira ejecutar
	// peticiones HTTP asincronamente desde JavaScript:
  	var http_request = false;
	if (window.XMLHttpRequest) { // Mozilla, Safari, ...
	  	http_request = new XMLHttpRequest();
	}else if (window.ActiveXObject) { // IE
	  	http_request = new ActiveXObject("Microsoft.XMLHTTP");
	}
	return http_request;
}


function configurate() {
	// Al cargar la pagina configuramos al cliente para que
	// cada X segundos recargue la web por si hubiera nuevas respuestas 
	// de los equipos.
	// setTimeOut se ejecutaria una unica vez pasado el tiempo indicado:
	getMessages()
	setInterval('getMessages();',20000);
}


function checkTimes (date_sms, date){

	if (date_sms > date){
		return "True";
	}
	return "False";
}

	
function getMessages(){
	// Pedimos al servidor que nos envie todos los mensajes que han sido publicados
	// desde la ultima lectura que realizamos de los mismos:

	var event_id = $('#event_id').text();
	var team_id = $('#team_id').text();

	// Coge los parametros correspondientes al equipo y evento
        http_request_0 = createXMLHttpRequest();
        http_request_0.open("GET", "/gymkhana/event/" + event_id + "/team/" + team_id + "/parameters/",false);
      	http_request_0.onreadystatechange = function() {
		if (http_request_0.readyState == 4) {
        	                if (http_request_0.status == 200) {
        	                        var info_0 =  eval( "(" + http_request_0.responseText + ")" );
					if ((info_0.date !=undefined) && (info_0.length != undefined)){
						date = info_0.date;
						old_length = info_0.length;
						$('#date').html(info_0.date);
						$('#length_messages').html(info_0.length);
					}
				}
		}
	}
        http_request_0.send(null);

	var date = $('#date').text();
        var old_length = parseInt($('#length_messages').text());
	var done = 0;
	// Si es necesario modifica esos parametros
	http_request = createXMLHttpRequest();
	http_request.open("GET", "/gymkhana/event/" + event_id + "/message/list/?format=json",false);
	http_request.onreadystatechange = function() {
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
			if (done == 0){
				//var html_text = http_request.responseText;
				var info = eval( "(" + http_request.responseText + ")" );
				var to_teams = null;
				if (info.messages!=undefined){
					done = 1;
					// info.messages contiene los mensajes
					var list_messages = info.messages.reverse();
					new_length = list_messages.length;
					if (new_length > old_length){   // Hay mensajes nuevos
						for (j = 0; j < new_length; j++){
							// Nos quedamos con los mensajes más nuevos
							var date_sms = list_messages[j].date;
							var correct = checkTimes(date_sms, date);
							if (correct == "True"){
								// El mensaje es nuevo
								if (list_messages[j].to_teams != undefined){
									to_teams = list_messages[j].to_teams;
								}
								if (to_teams != null){
									// Comprobamos destinos
									for (g = 0; g < to_teams.length; g++){
										if (to_teams[g].to_team_identifier == team_id){
											//alertamos nuevo mensaje
											old_length++;
											i++;
											$("#date").html(date_sms);
											newMessage(i);
										}
									}
								}				
							}
						}
						$("#length_messages").html(old_length);
					}
					
				}
			}
			}
		}
	}
	http_request.send(null);
	

	// Envia los parametros para que se guarden
        date = $("#date").text();
        old_length = parseInt($("#length_messages").text());
	console.log( date + " " + old_length );
        http_request2 = createXMLHttpRequest();
	http_request2.open("POST", "/gymkhana/event/" + event_id + "/team/" + team_id + "/parameters/?length=" + old_length + "&date=" + date, false);
	http_request2.onreadystatechange = function() {
	}
	http_request2.send(null);


	// setTimeOut se ejecutaria una unica vez pasado el tiempo indicado:
	// setTimeout('loadMessages();',5000);
	// Pero ya esta puesto en el configurate() el setInterval() que se ejecuta
	// siempre cada periodo de tiempo, no solo una vez, por lo que no es
	// necesario escribir aqui esta instruccion
}
