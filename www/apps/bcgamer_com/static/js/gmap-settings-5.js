/* ---------------------------------------------------------------------- */
/*	map street view mode function
/* ---------------------------------------------------------------------- */
function initialize() {
	var topazPark = new google.maps.LatLng(48.444253,-123.363293);

	var panoramaOptions = {
		center: topazPark,
		mapTypeId: google.maps.MapTypeId.SATELLITE,
		/*position: topazPark,
		pov: {
			heading: 75.21,
			pitch: 0.84
		},*/
		zoom: 18
	};

	var myPano = new google.maps.Map(
		document.getElementById('map'),
		panoramaOptions);
	myPano.setVisible(true);
}

try {
	google.maps.event.addDomListener(window, 'load', initialize);
} catch(err) {

}