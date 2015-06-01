/* ---------------------------------------------------------------------- */
/*	map street view mode function
/* ---------------------------------------------------------------------- */
function initialize() {
	var topazPark = new google.maps.LatLng(48.443798,-123.365468);
	//Change a map street view cordinate here! {"lat":"-33.880641", "lon":"151.204298"}
	//48.444262, -123.363912
	var panoramaOptions = {
		position: topazPark,
		pov: {
			heading: 75.21,
			pitch: 0.84
		},
		zoom: 1.5
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