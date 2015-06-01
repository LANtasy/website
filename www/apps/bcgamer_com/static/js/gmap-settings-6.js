/* ---------------------------------------------------------------------- */
/*	map street view mode function
/* ---------------------------------------------------------------------- */
function initialize() {
	// birdseye of Topaz park
    var park = new google.maps.LatLng(48.443253,-123.363293);
	var field1 = new google.maps.LatLng(48.444153,-123.363493);
    var field2 = new google.maps.LatLng(48.443653,-123.363893);
    var field3 = new google.maps.LatLng(48.443303,-123.363593);

	var mapOptions = {
		// https://developers.google.com/maps/documentation/javascript/reference#MapOptions
		center: park,
		mapTypeId: google.maps.MapTypeId.SATELLITE,
		zoom: 18
	};

	var map = new google.maps.Map(document.getElementById('map'), mapOptions);


    var field1_marker = new google.maps.Marker({
       position: field1,
       title: 'Topaz #1'
    });

    var field2_marker = new google.maps.Marker({
       position: field2,
       title: 'Topaz #2'
    });

    var field3_marker = new google.maps.Marker({
       position: field3,
       title: 'Topaz #3'
    });

    field1_marker.setMap(map);
    field2_marker.setMap(map);
    field3_marker.setMap(map);
    map.setVisible(true);
}

try {
	google.maps.event.addDomListener(window, 'load', initialize);
} catch(err) {

}