// user account js
$(document).ready(function () {
    var target = 'user-profile';

    $('#menu-toggle').on('click', function () {
        $('.drawer-nav').toggleClass('open');
        $('.overlay').toggleClass('active');
    });

    // Close the drawer navigation on overlay click
    $('.overlay').on('click', function () {
        $('.drawer-nav').removeClass('open');
        $('.overlay').removeClass('active');
    });

    // Toggle the menu on button click
    $('#menu-toggle').on('click', function () {
        $('#menu').toggleClass('active');
    });

    // Close the menu when an option is clicked
    $('.option').on('click', function () {
        $('#menu').removeClass('active');
    });

    $('#menu-toggle').click(function () {
        $('#menu').toggleClass('show-menu');
    });

    $(window).resize(function () {
        // Get the window width
        var windowWidth = $(window).width();

        // Perform actions based on the window width
        if (windowWidth < 768) {
            // Actions for mobile devices
            $('#menu').addClass('drawer-nav')
            $('#menu-toggle').show();
            $('#u-profile').hide()
            $('#navigation').removeClass('col-3')
            $('#content').removeClass('col-9')
            $('#content').addClass('col-12')
            //action for tablet
        } else if (windowWidth >= 768 && windowWidth < 992) {
            // Actions for tablet devices
            $('#menu-toggle').show();
            $('#menu').addClass('drawer-nav')
            $('#u-profile').hide()
            $('#navigation').removeClass('col-3')
            $('#content').removeClass('col-9')
            $('#content').addClass('col-12')
            // action for other screen
        } else {
            $('#menu').removeClass('drawer-nav')
            $('#menu-toggle').hide();
            $('#navigation').addClass('col-3')
            $('#u-profile').show()
            $('#content').addClass('col-9')
            $('#content').removeClass('col-12')
        }
    }).resize();

    $.ajax({
        url: '/' + target + '/',
        dataType: 'html',
        success: function (response) {
            $('#' + target).html(response);
            $('#' + target).addClass('active');
        },
        error: function () {
            $('#' + target).html('<h3>Error loading content</h3>');
            $('#' + target).addClass('active');
        }
    });

    $('.option').click(function () {
        var target = $(this).data('target');
        $('.option').removeClass('active');
        $(this).addClass('active');
        $('.content-section').removeClass('active');

        console.log(target)
        $.ajax({
            url: '/' + target + '/',
            dataType: 'html',
            success: function (response) {
                $('#' + target).html(response);
                $('#' + target).addClass('active');

                // Close the drawer navigation
                $('.drawer-nav').removeClass('open');
                $('.overlay').removeClass('active');
            },
            error: function () {
                $('.drawer-nav').removeClass('open');
                $('#' + target).html('<h3>Error loading content</h3>');
                $('#' + target).addClass('active');
                $('.overlay').removeClass('active');
            }
        });
    });
});
