// Main Javascript(Jquery) file for the application
$(document).ready(function () {
  var windowOn = $(window);

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
      min: 10,
      max: 999,
      values: [10, 999],
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

  // magnificPopup img view
  $(".image-popups").magnificPopup({
    type: "image",
    gallery: {
      enabled: true,
    },
  });

  // Wow Js
  new WOW().init();

  // Cart Quantity Js
  $(".cart-minus").click(function () {
    var $input = $(this).parent().find("input");
    var count = parseInt($input.val()) - 1;
    count = count < 1 ? 1 : count;
    $input.val(count);
    $input.change();
    return false;
  });
  $(".cart-plus").click(function () {
    var $input = $(this).parent().find("input");
    $input.val(parseInt($input.val()) + 1);
    $input.change();
    return false;
  });

  // Cart Plus Minus Js
  $(".cart-plus-minus").append(
    '<div class="dec qtybutton">-</div><div class="inc qtybutton">+</div>'
  );
  $(".qtybutton").on("click", function () {
    var $button = $(this);
    var oldValue = $button.parent().find("input").val();
    if ($button.text() == "+") {
      var newVal = parseFloat(oldValue) + 1;
    } else {
      // Don't allow decrementing below zero
      if (oldValue > 0) {
        var newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 0;
      }
    }
    $button.parent().find("input").val(newVal);
    $("#quantity_val").val(newVal);
  });

  $("#ship-box").on("click", function () {
    $("#ship-box-info").slideToggle(1000);
  });

  $(".counter").counterUp({
    delay: 10,
    time: 1000,
  });

  $(".hover__active").on("mouseenter", function () {
    $(this)
      .addClass("active")
      .parent()
      .siblings()
      .find(".hover__active")
      .removeClass("active");
  });

  $("[data-background").each(function () {
    $(this).css(
      "background-image",
      "url( " + $(this).attr("data-background") + "  )"
    );
  });

  $("[data-width]").each(function () {
    $(this).css("width", $(this).attr("data-width"));
  });

  // Testimonial
  if (jQuery(".testimonial_active").length > 0) {
    let testimonialTwo = new Swiper(".testimonial_active", {
      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      autoplay: {
        delay: 6000,
      },

      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".ts-button-next",
        prevEl: ".ts-button-prev",
      },

      scrollbar: {
        el: ".swiper-scrollbar",
      },
      breakpoints: {
        550: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 1,
        },
        1200: {
          slidesPerView: 1,
        },
        1400: {
          slidesPerView: 1,
        },
      },
    });
  }
  if (jQuery(".slider__active").length > 0) {
    let sliderActive1 = ".slider__active";
    let sliderInit1 = new Swiper(sliderActive1, {
      slidesPerView: 1,
      slidesPerColumn: 1,
      loop: true,
      effect: "fade",
      autoplay: {
        delay: 6000,
      },

      pagination: {
        el: ".hero-pagination",
        clickable: true,
      },

      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },

      a11y: false,
    });

    function animated_swiper(selector, init) {
      let animated = function animated() {
        $(selector + " [data-animation]").each(function () {
          let anim = $(this).data("animation");
          let delay = $(this).data("delay");
          let duration = $(this).data("duration");

          $(this)
            .removeClass("anim" + anim)
            .addClass(anim + " animated")
            .css({
              webkitAnimationDelay: delay,
              animationDelay: delay,
              webkitAnimationDuration: duration,
              animationDuration: duration,
            })
            .one(
              "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend",
              function () {
                $(this).removeClass(anim + " animated");
              }
            );
        });
      };
      animated();
      // Make animated when slide change
      init.on("slideChange", function () {
        $(sliderActive1 + " [data-animation]").removeClass("animated");
      });
      init.on("slideChange", animated);
    }

    animated_swiper(sliderActive1, sliderInit1);
  }
  $(".fitness-slider_active").owlCarousel({
    loop: true,
    center: true,
    margin: 0,
    autoplay: true,
    autoplayTimeout: 5000,
    smartSpeed: 500,
    items: 6,
    navText: [
      '<button><i class="fal fa-angle-left"></i></button>',
      '<button><i class="fal fa-angle-right"></i></button>',
    ],
    nav: false,
    dots: false,
    responsive: {
      0: {
        items: 1,
      },
      576: {
        items: 1,
      },
      767: {
        items: 2,
      },
      992: {
        items: 2,
      },
      1200: {
        items: 3,
      },
      1600: {
        items: 3,
      },
    },
  });

  $(".popup-video").magnificPopup({
    type: "iframe",
  });

  if (jQuery(".client-feedback_active").length > 0) {
    let testimonialTwo = new Swiper(".client-feedback_active", {
      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      autoplay: {
        delay: 6000,
      },

      pagination: {
        el: ".swiper-pagination",
        clickable: false,
      },
      navigation: {
        nextEl: ".ts-button-next",
        prevEl: ".ts-button-prev",
      },

      scrollbar: {
        el: ".swiper-scrollbar",
      },
      breakpoints: {
        550: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 1,
        },
        1200: {
          slidesPerView: 1,
        },
        1400: {
          slidesPerView: 1,
        },
      },
    });
  }

  if (jQuery(".sponsor_slider-active").length > 0) {
    let testimonialTwo = new Swiper(".sponsor_slider-active", {
      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      autoplay: {
        delay: 6000,
      },

      pagination: {
        el: ".swiper-pagination",
        clickable: false,
      },

      scrollbar: {
        el: ".swiper-scrollbar",
      },
      breakpoints: {
        400: {
          slidesPerView: 2,
        },
        550: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
        1200: {
          slidesPerView: 4,
        },
        1400: {
          slidesPerView: 4,
        },
      },
    });
  }

  $(document).on("change", ".sort-select", function (e) {
    e.target.dispatchEvent(new Event("change"));
  });

  var total = 0;
  var cart_qty_val = document.getElementsByClassName("cart-item-qty");

  if (cart_qty_val.length > 0) {
    for (var i = 0; i < cart_qty_val.length; i++) {
      total += parseInt(cart_qty_val[i].value);
    }
    $(".qtybutton").on("click", function () {
      var $button = $(this);
      var oldValue = total;
      if ($button.text() == "+") {
        var newVal = oldValue + 1;
      } else {
        if (oldValue > 0) {
          var newVal = oldValue - 1;
        } else {
          newVal = 0;
        }
      }
      total = newVal;
    });
  }

  var qtybutton = document.querySelectorAll(".qtybutton");
  if (qtybutton.length > 0) {
    for (var i = 0; i < qtybutton.length; i++) {
      qtybutton[i].addEventListener("click", function (e) {
        var get_qty_elem = this.parentElement.querySelector("input");
        let id_counter = get_qty_elem.id.split("_")[1];
        let set_qty_elem = document.getElementById(
          "cart_item_qt_hid" + id_counter
        );
        set_qty_elem.value = get_qty_elem.value;
      });
    }
  }

  var cart_clear_btn = document.getElementById("cart_clear_btn");
  if (cart_clear_btn) {
    cart_clear_btn.addEventListener("click", function (e) {
      var cart_count = document.getElementById("cart_items_counts");
      cart_count.innerHTML = "0";
    });
  }

  var cart_update_btn = document.getElementById("cart_update_btn");
  if (cart_update_btn) {
    cart_update_btn.addEventListener("click", function (e) {
      var cart_count = document.getElementById("cart_items_counts");
      cart_count.innerHTML = total;
    });
  }

  var delete_item_btns = document.getElementsByClassName("delete_item_btn");
  if (delete_item_btns.length > 0) {
    for (var i = 0; i < delete_item_btns.length; i++) {
      delete_item_btns[i].addEventListener("click", function (e) {
        var item_count =
          this.parentElement.parentNode.parentElement.querySelector(
            ".cart-item-qty"
          ).value;
        if (total > 0) {
          total -= parseInt(item_count);
        } else {
          total = 0;
        }
        var cart_count = document.getElementById("cart_items_counts");
        cart_count.innerHTML = total;
      });
    }
  }
});
