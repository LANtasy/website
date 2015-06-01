/* ---------------------------------------------------------------------- */
/*	map street view mode function
/* ---------------------------------------------------------------------- */
function initialize() {
	var bryantPark = new google.maps.LatLng(52.914306,-1.448395); //Change a map street view cordinate here! {"lat":"-33.880641", "lon":"151.204298"}
	var panoramaOptions = {
		position: bryantPark,
		pov: {
			heading: 0.11,
			pitch: 6.84
		},
		zoom: 1
	};
	var myPano = new google.maps.StreetViewPanorama(
		document.getElementById('map'),
		panoramaOptions);
	myPano.setVisible(true);
}

try {
	google.maps.event.addDomListener(window, 'load', initialize);
} catch(err) {

}