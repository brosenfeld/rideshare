$(function() {
    $( "#id_date" ).datepicker();
});

function initialize() {
	var input = document.getElementById('id_location');
	autocomplete = new google.maps.places.Autocomplete(input, { types: ['geocode'] });
}