jQuery(function($){
	"use strict";

var CONVOCATION = window.CONVOCATION || {};

/* ==================================================
	Contact Form Validations
================================================== */
	CONVOCATION.RegistrationForm = function(){
		$('.registration-form').each(function(){
			var formInstance = $(this);
			formInstance.submit(function(){
		
			var action = $(this).attr('action');
		
			$("#message").slideUp(750,function() {
			$('#message').hide();
		
			$('#submit')
				.after('<img src="images/assets/ajax-loader.gif" class="loader" />')
				.attr('disabled','disabled');
		
			$.post(action, {
				plan: $('input[name=plan]:checked').val(),
				name: $('#Name').val(),
				email: $('#Email').val(),
				phone: $('#Phone').val()
			},
				function(data){
					document.getElementById('message').innerHTML = data;
					$('#message').slideDown('slow');
					$('.registration-form img.loader').fadeOut('slow',function(){$(this).remove()});
					$('#submit').removeAttr('disabled');
				}
			);
			});
			return false;
		});
		});
	}
/* ==================================================
	Scroll to Top
================================================== */
	CONVOCATION.scrollToTop = function(){
		var windowWidth = $(window).width(),
			didScroll = false;
	
		var $arrow = $('#back-to-top');
		var $sharefloat = $('.social-share');
	
		$arrow.click(function(e) {
			$('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
			e.preventDefault();
		})
	
		$(window).scroll(function() {
			didScroll = true;
		});
	
		setInterval(function() {
			if( didScroll ) {
				didScroll = false;
	
				if( $(window).scrollTop() > 200 ) {
					$arrow.css("right",10);
					$sharefloat.css("right",60);
				} else {
					$arrow.css("right","-40px");
					$sharefloat.css("right",10);
				}
			}
		}, 250);
	}
/* ==================================================
   Accordion
================================================== */
	CONVOCATION.accordion = function(){
		var accordion_trigger = $('.accordion-heading.accordionize');
		
		accordion_trigger.delegate('.accordion-toggle','click', function(event){
			if($(this).hasClass('active')){
				$(this).removeClass('active');
				$(this).addClass('inactive');
			}
			else{
				accordion_trigger.find('.active').addClass('inactive');          
				accordion_trigger.find('.active').removeClass('active');   
				$(this).removeClass('inactive');
				$(this).addClass('active');
			}
			event.preventDefault();
		});
	}
/* ==================================================
   Toggle
================================================== */
	CONVOCATION.toggle = function(){
		var accordion_trigger_toggle = $('.accordion-heading.togglize');
		
		accordion_trigger_toggle.delegate('.accordion-toggle','click', function(event){
			if($(this).hasClass('active')){
				$(this).removeClass('active');
				$(this).addClass('inactive');
			}
			else{
				$(this).removeClass('inactive');
				$(this).addClass('active');
			}
			event.preventDefault();
		});
	}
/* ==================================================
   Tooltip
================================================== */
	CONVOCATION.toolTip = function(){ 
		$('a[data-toggle=tooltip]').tooltip();
		$('a[data-toggle=popover]').popover({html:true}).click(function(e) { 
       e.preventDefault(); 
       $(this).focus(); 
   });
	}
/* ==================================================
   Twitter Widget
================================================== */
	/*CONVOCATION.TwitterWidget = function() {
		$('.twitter-widget').each(function(){
			var twitterInstance = $(this); 
			var twitterTweets = twitterInstance.attr("data-tweets-count") ? twitterInstance.attr("data-tweets-count") : "1"
			twitterInstance.twittie({
            	dateFormat: '%b. %d, %Y',
            	template: '<li><i class="fa fa-twitter"></i> {{tweet}} <span class="date">{{date}}</span></li>',
            	count: twitterTweets,
            	hideReplies: true
        	});
		}); 
	}   */
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
/* ==================================================
   PrettyPhoto
================================================== */
	CONVOCATION.PrettyPhoto = function() {
		$("a[data-rel^='prettyPhoto']").prettyPhoto({
			  opacity: 0.5,
			  social_tools: "",
			  deeplinking: false
		});
	}
/* ==================================================
   Animated Counters
================================================== */
	CONVOCATION.Counters = function() {
		$('.counters').each(function () {
			$(".timer .count").appear(function() {
			var counter = $(this).html();
			$(this).countTo({
				from: 0,
				to: counter,
				speed: 2000,
				refreshInterval: 60,
				});
			});
		});
	}
/* ==================================================
   SuperFish menu
================================================== */
	CONVOCATION.SuperFish = function() {
		$('.sf-menu').superfish({
			  delay: 200,
			  animation: {opacity:'show', height:'show'},
			  speed: 'fast',
			  cssArrows: false,
			  disableHI: true
		});
		$(".main-navigation > ul > li > ul > li:has(ul)").find("a:first").append(" <i class='fa fa-angle-right'></i>");
		$(".main-navigation > ul > li > ul > li > ul > li:has(ul)").find("a:first").append(" <i class='fa fa-angle-right'></i>");
	}
/* ==================================================
   Header Functions
================================================== */
	CONVOCATION.StickyHeader = function() {
		var windowWidth = $(window).width(),
		didScroll = false;
	
		var $menu = $('.site-header');
	
		$(window).scroll(function() {
			didScroll = true;
		});
	
		setInterval(function() {
	
				if( $(window).scrollTop() > 20 ) {
					$menu.addClass('sticky-header');
				} else {
					$menu.removeClass('sticky-header');
				}
		}, 250);
		setInterval(function() {
	
				if( $(window).scrollTop() > 120 ) {
					$menu.addClass('tranlucent');
				} else {
					$menu.removeClass('tranlucent');
				}
		}, 250);
	}
/* ==================================================
	Responsive Nav Menu
================================================== */
	CONVOCATION.MobileMenu = function() {
		// Responsive Menu Events
		$('#menu-toggle').click(function(){
			$(this).toggleClass("opened");
			$(".main-navigation").slideToggle();
			return false;
		});
		if($(window).width() < 992){
			var WHG = $(window).height();
			var HH = $('.site-header').height();
			var WNH = WHG -HH;
			$('.main-navigation').css("height",WNH);
		}
		$(window).resize(function(){
			if($(body).hasClass(no-touch) & $(window).width() > 992) {
				$(".main-navigation").css("display","block");
				} else {
				$(".main-navigation").css("display","none");
			}
		});
		$(window).resize(function(){
			if($("#menu-toggle").hasClass("opened")){
				$(".main-navigation").css("display","block");
			} else {
				$(".main-navigation").css("display","none");
			}
		});
	}
/* ==================================================
   Flickr Widget
================================================== */
	CONVOCATION.FlickrWidget = function() {
		$('.flickr-widget').each(function(){
			var flickrInstance = $(this); 
			var flickrImages = flickrInstance.attr("data-images-count") ? flickrInstance.attr("data-images-count") : "1"
			var flickrUserid = flickrInstance.attr("data-flickr-userid") ? flickrInstance.attr("data-flickr-userid") : "1"
			flickrInstance.jflickrfeed({
				limit: flickrImages,
				qstrings: {
					id: flickrUserid
				},
				itemTemplate: '<li><a href="{{image_b}}"><img alt="{{title}}" src="{{image_s}}" /></a></li>'
			});
		});
	}
/* ==================================================
   Init Functions
================================================== */
$(document).ready(function(){
	CONVOCATION.RegistrationForm();
	CONVOCATION.scrollToTop();
	CONVOCATION.accordion();
	CONVOCATION.toggle();
	CONVOCATION.toolTip();
	//CONVOCATION.TwitterWidget();
	CONVOCATION.PrettyPhoto();
	CONVOCATION.SuperFish();
	CONVOCATION.Counters();
	CONVOCATION.StickyHeader();
	CONVOCATION.MobileMenu();
	CONVOCATION.heroflex();
	CONVOCATION.FlickrWidget();
});


// Pages Design Functions

// Any Button Scroll to section
$('.scrollto').click(function(){
	$.scrollTo( this.hash, 800, { easing:'easeOutQuint' });
	return false;
});

// FITVIDS
$(".fw-video").fitVids();

// Image Hover icons for gallery items
var MBC = function(){
	$(".media-box .zoom").each(function(){
		mpwidth = $(this).parent().width();
		mpheight = $(this).parent().find("img").height();
	
		$(this).css("width", mpwidth);
		$(this).css("height", mpheight);
		$(this).css("line-height", mpheight+"px");
	});
}
$(document).ready(function(){
	$(".format-image").each(function(){
		$(this).find(".media-box").append("<span class='zoom'><span class='icon'><i class='icon-image'></i></span></span>");
	});
	$(".format-standard").each(function(){
		$(this).find(".media-box").append("<span class='zoom'><span class='icon'><i class='icon-eye'></i></span></span>");
	});
	$(".format-video").each(function(){
		$(this).find(".media-box").append("<span class='zoom'><span class='icon'><i class='icon-music-play'></i></span></span>");
	});
	$(".format-link").each(function(){
		$(this).find(".media-box").append("<span class='zoom'><span class='icon'><i class='fa fa-link'></i></span></span>");
	});
	$('.pricing-plans input[name=plan]:checked').parent('.plan-option').addClass("selected");
    $('.pricing-plans input[name=plan]').click(function () {
        $('.pricing-plans input[name=plan]:not(:checked)').parent('.plan-option').removeClass("selected");
        $('.pricing-plans input[name=plan]:checked').parent('.plan-option').addClass("selected");
    });
	$(".plan-option").each(function(){
			if($(this).hasClass('selected')){
				$(this).append("<span class='plan-selection'><span class='btn btn-default btn-transparent'><i class='fa fa-check'></i> Selected</span></span>");
			} else {
				$(this).append("<span class='plan-selection'><span class='btn btn-default btn-transparent'>Select</span></span>");
			}
	});
	$(".plan-option").click(function(){
		$(".plan-option").find(".plan-selection").find(".btn").html('Select');
		$(this).find(".plan-selection").find(".btn").html('<i class="fa fa-check"></i> Selected');
	});
	if(Modernizr.touch && $(window).width() < 991 ) {
		$(".sf-menu > li > a").click(function(e){
			$(".main-navigation").slideUp();
			e.preventDefault();
		});
	}
	$('.share-float').click(function(e){
		e.preventDefault();
	});
	$('.social-share').hover(function(e){
		if($(this).hasClass('opened')){
			$('.social-share .social-icons').delay(1000).animate({height:'0',opacity:0}, "fast", "easeInQuad");
			$(this).removeClass('opened');
			$(this).addClass('closed');
		} else {
			$('.social-share .social-icons').animate({height:'160px',opacity:1}, "fast", "easeOutQuad");
			$('.social-share').css("overflow","visible");
			$(this).removeClass('closed');
			$(this).addClass('opened');
		}
	});
	CONVOCATION.StickyHeader();
});

$(window).resize(function(){
	if ($(window).width() > 992){
		$(".main-navigation").css("display","block");
	} else {
		$(".main-navigation").css("display","none");
	}
});
$(document).ready(function(){
	// Icon Append
	$('.basic-link').append(' <i class="fa fa-angle-right"></i>');
	$('.basic-link.backward').prepend(' <i class="fa fa-angle-left"></i> ');
	$(".nav-tabs li").prepend('<i class="fa fa-caret-down"></i> ');
	$('ul.checks li').prepend('<i class="fa fa-check"></i> ');
	$('ul.angles li, .nav-list-primary li a > a:first-child').prepend('<i class="fa fa-angle-right"></i> ');
	$('ul.inline li').prepend('<i class="fa fa-check-circle-o"></i> ');
	$('ul.chevrons li').prepend('<i class="fa fa-chevron-right"></i> ');
	$('ul.carets li').prepend('<i class="fa fa-caret-right"></i> ');
	$('a.external').prepend('<i class="fa fa-external-link"></i> ');
	// Centering the dropdown menus
	$(".main-navigation ul li").mouseover(function() {
		 var the_width = $(this).find("a").width();
		 var child_width = $(this).find("ul").width();
		 var width = parseInt((child_width - the_width)/2);
		 $(this).find("ul").css('left', -width);
	});
	var $tallestCol;
	$('.pricing-plans').each(function(){
	   $tallestCol = 0;
	   $(this).find('.inclusive').
		each(function(){
			($(this).height() > $tallestCol) ? $tallestCol = $(this).height() : $tallestCol = $tallestCol;
		});   
		if($tallestCol == 0) $tallestCol = 'auto';
		$(".inclusive ul").css('height',$tallestCol);
	});
});

// Animation Appear
$("[data-appear-animation]").each(function() {
	var $this = $(this);
	$this.addClass("appear-animation");
	if(!$("html").hasClass("no-csstransitions") && $(window).width() > 767) {
		$this.appear(function() {
			var delay = ($this.attr("data-appear-animation-delay") ? $this.attr("data-appear-animation-delay") : 1);
			if(delay > 1) $this.css("animation-delay", delay + "ms");
			$this.addClass($this.attr("data-appear-animation"));
			setTimeout(function() {
				$this.addClass("appear-animation-visible");
			}, delay);
		}, {accX: 0, accY: -150});
	} else {
		$this.addClass("appear-animation-visible");
	}
});
// Animation Progress Bars
$("[data-appear-progress-animation]").each(function() {
	var $this = $(this);
	$this.appear(function() {
		var delay = ($this.attr("data-appear-animation-delay") ? $this.attr("data-appear-animation-delay") : 1);
		if(delay > 1) $this.css("animation-delay", delay + "ms");
		$this.addClass($this.attr("data-appear-animation"));
		setTimeout(function() {
			$this.animate({
				width: $this.attr("data-appear-progress-animation")
			}, 1500, "easeOutQuad", function() {
				$this.find(".progress-bar-tooltip").animate({
					opacity: 1
				}, 500, "easeOutQuad");
			});
		}, delay);
	}, {accX: 0, accY: -50});
});

$(document).ready(function(){
	// Parallax Jquery Callings
	if(!Modernizr.touch) {
		$(window).bind('load', function () {
			parallaxInit();						  
		});
	}
	function parallaxInit() {
		$('.parallax1').parallax("50%", 0.1);
		$('.parallax2').parallax("50%", 0.1);
		$('.parallax3').parallax("50%", 0.1);
		$('.parallax4').parallax("50%", 0.1);
		$('.parallax5').parallax("50%", 0.1);
		$('.parallax6').parallax("50%", 0.1);
		$('.parallax7').parallax("50%", 0.1);
		$('.parallax8').parallax("50%", 0.1);
		/*add as necessary*/
	}
	
	//LOCAL SCROLL
	jQuery('.sf-menu').localScroll({
		offset: -62
	});
	
	var sections = jQuery('section');
	var navigation_links = jQuery('.sf-menu a');
	sections.waypoint({
		handler: function(direction) {
			var active_section;
			active_section = jQuery(this);
			if (direction === "up") active_section = active_section.prev();
			var active_link = jQuery('.sf-menu a[href="#' + active_section.attr("id") + '"]');
			navigation_links.removeClass("current");
			active_link.addClass("current").delay(1500);
		},
		offset: 150
	});
	// Window height/Width Getter Classes
	var wheighter = $(window).height();
	var wwidth = $(window).width();
	var wheightlh = wheighter - 80;
	$(".wheighter").css("height",wheighter);
	$(".wwidth").css("width",wwidth);
	$(".wheighterlh").css("height",wheightlh);
});
$(window).resize(function(){
	var wheighter = $(window).height();
	var wwidth = $(window).width();
	var wheightlh = wheighter - 80;
	$(".wheighter").css("height",wheighter);
	$(".wwidth").css("width",wwidth);
	$(".wheighterlh").css("height",wheightlh);
});
$(window).load(function(){
	$('.event-hero-info').fadeIn();
});
});