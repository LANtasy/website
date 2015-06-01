/* ---------------------------------------------------------------------- */
/*	map street view mode function
/* ---------------------------------------------------------------------- */
function initialize() {
	var bryantPark = new google.maps.LatLng(37.422017,-122.083788); //Change a map street view cordinate here! {"lat":"-33.880641", "lon":"151.204298"}
	var panoramaOptions = {
		position: bryantPark,
		pov: {
			heading: -48.28,
			pitch: 5.34
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