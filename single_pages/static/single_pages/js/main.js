(function ($) {
    "use strict";

    // Latest-news-carousel
    $(document).ready(function(){
        $(".latest-news-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 2000,
            center: false,
            dots: true,
            loop: true,
            margin: 25,
            nav : true,
            navText : [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ],
            responsiveClass: true,
            responsive: {
                0:{
                    items:1
                },
                576:{
                    items:1
                },
                768:{
                    items:2
                },
                992:{
                    items:3
                },
                1200:{
                    items:4
                }
            }
        });
    });
    
})(jQuery);

function scrollToBottom() {
    $('html, body').animate({ scrollTop: $(document).height() }, 500, 'easeInOutExpo');
}