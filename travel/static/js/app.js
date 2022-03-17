$(function () {
    $('#login-form-link').click(function(e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').click(function(e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

    $('.slick-gallery').slick({
        draggable: true,
        arrows: false,
        infinite: true,
        fade: true,
        speed: 500,
        cssEase: 'linear',
        asNavFor: '.slick-thumbnails'
    });

    $('.slick-thumbnails').slick({
        draggable: false,
        slidesToShow: 3,
        slidesToScroll: 1,
        asNavFor: '.slick-gallery',
        dots: false,
        focusOnSelect: true
    });

    $("a.open_popup").fancybox();
});
