(function ($) {
    "use strict";

    $(document).ready(function () {
        // Sticky Navbar
        $(window).scroll(function () {
            if ($(this).scrollTop() > 300) {
                $('.sticky-top').addClass('shadow-sm').css('top', '0px');
            } else {
                $('.sticky-top').removeClass('shadow-sm').css('top', '-150px');
            }
        });

        // Back to top button
        $(window).scroll(function () {
            if ($(this).scrollTop() > 300) {
                $('.back-to-top').fadeIn('slow');
            } else {
                $('.back-to-top').fadeOut('slow');
            }
        });

        $('.back-to-top').click(function () {
            $('html, body').animate({scrollTop: 0}, 500, 'easeInOutExpo');
            return false;
        });

    });
    
})(jQuery);

// modal function
function showAlertModal(message) {
    $("#alertDynamicContent").empty();
    $("#alertDynamicContent").html(message);
    $("#alertModal").modal("show");
}

function showConfirmModal(message, process, val) {
    $("#confirmDynamicContent").empty();
    $("#confirmDynamicContent").html(message);

    $('#confirmButton').attr("onclick", "");
    $('#confirmButton').attr("onclick", process+"("+val+");");

    $("#confirmModal").modal("show");
}

function showLogoutModal(user_id) {
    $("#logoutIdLabel").text('');
    $("#logoutIdLabel").text(user_id);
    $("#logoutModal").modal("show");
}