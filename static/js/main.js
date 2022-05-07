// Main Javascript(Jquery) file for the application

(function ($) {
  "use strict";

  var windowOn = $(window);

  // PreLoader
  $(window).on("load", function (event) {
    $("#preloader").delay(500).fadeOut(500);
  });

  // Mobile Menu
  $("#mobile-menu").meanmenu({
    meanMenuContainer: ".mobile-menu",
    meanScreenWidth: "991",
    meanExpand: ['<i class="fal fa-plus"></i>'],
  });

  // Sidebar
  $(".sidebar-toggle-btn").on("click", function () {
    $(".sidebar__area").addClass("sidebar-opened");
    $(".body-overlay").addClass("opened");
  });
  $(".sidebar__close-btn").on("click", function () {
    $(".sidebar__area").removeClass("sidebar-opened");
    $(".body-overlay").removeClass("opened");
  });

  // Sticky Header
  windowOn.on("scroll", function () {
    var scroll = $(window).scrollTop();
    if (scroll < 100) {
      $("#header-sticky").removeClass("sticky");
    } else {
      $("#header-sticky").addClass("sticky");
    }
  });

  // Range Slider
  if (jQuery("#slider-range").length > 0) {
    $("#slider-range").slider({
      range: true,
      min: 20,
      max: 280,
      values: [75, 300],
      slide: function (event, ui) {
        $("#amount").val("$" + ui.values[0] + " To $" + ui.values[1]);
      },
    });
    $("#amount").val(
      "$" +
        $("#slider-range").slider("values", 0) +
        " To $" +
        $("#slider-range").slider("values", 1)
    );
  }
  // Nice Select Js
  $("select").niceSelect();
})(jQuery);
