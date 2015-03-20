$(document).ready(function(){

	var correct = $('#correct');
	var solutions = $('#solutions');
	var coords = $('#coords');
	

	$("#textual").click(function(){
		coords.hide();
		correct.show();
		solutions.show();
	});
	
	$("#Ophoto").click(function(){
		coords.hide();
		correct.hide();
		solutions.hide();
	});
	
	$("#location").click(function(){
		correct.hide();
		solutions.hide();
		coords.show();
	});



});
