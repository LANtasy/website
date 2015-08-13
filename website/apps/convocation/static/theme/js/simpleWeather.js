// Docs at http://simpleweatherjs.com
$(document).ready(function() {
    $.simpleWeather({
        location: 'Victoria, BC',
        woeid: '',
        unit: 'c',
        success: function(weather) {
            html = '<i class="wi wi-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'';
            $("#weather").html(html);
            },
        error: function(error) {
            $("#weather").html('<p>'+error+'</p>');
        }
    });
});
