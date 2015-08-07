// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.

jQuery(function($){
	"use strict";

var CONVOCATION = window.CONVOCATION || {};

/* ==================================================
   Hero Flex Slider
================================================== */
	CONVOCATION.heroflex = function() {
		$('.flexslider').each(function(){
            var carouselInstance = $(this);
            var carouselAutoplay = carouselInstance.attr("data-autoplay") == 'yes' ? true : false
            var carouselPagination = carouselInstance.attr("data-pagination") == 'yes' ? true : false
            var carouselArrows = carouselInstance.attr("data-arrows") == 'yes' ? true : false
            var carouselDirection = carouselInstance.attr("data-direction") ? carouselInstance.attr("data-direction") : "horizontal"
            var carouselStyle = carouselInstance.attr("data-style") ? carouselInstance.attr("data-style") : "fade"
            var carouselSpeed = carouselInstance.attr("data-speed") ? carouselInstance.attr("data-speed") : "5000"
            var carouselPause = carouselInstance.attr("data-pause") == 'yes' ? true : false

            carouselInstance.flexslider({
                animation: carouselStyle,
                easing: "swing",
                direction: carouselDirection,
                slideshow: carouselAutoplay,
                slideshowSpeed: carouselSpeed,
                animationSpeed: 600,
                initDelay: 0,
                randomize: false,
                pauseOnHover: carouselPause,
                controlNav: carouselPagination,
                directionNav: carouselArrows,
                prevText: "",
                nextText: "",
                start: function () {
                  $('.flex-caption').show();
                  BackgroundCheck.init({
                    targets: '.body',
                    images: '.flexslider li.parallax'
                  });
                },
                after: function () {
                  BackgroundCheck.refresh();
                  $('.flex-caption').show();
                }
            });
		});
	}
});

