/*!

 =========================================================
 * Blk• Design System - v1.0.0
 =========================================================

 * Product Page: https://www.creative-tim.com/product/blk-design-system
 * Copyright 2018 Creative Tim (http://www.creative-tim.com)

 * Coded by www.creative-tim.com

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */

 
function getQuery(key) {
  // get query string from url (If none return empty string)
  var query = window.location.search.substring(1);
  // split query string into separate key/value pairs
  var vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    if (pair[0] == key) {
      return pair[1];
    }
  }
  return false;
}

(getQuery("ani") == "true") ? preanimate = true : preanimate = false;
console.log(getQuery("ani"), preanimate);

if (preanimate) {
  $("#fullFill").show();

  cX = getQuery("cX");
  cY = getQuery("cY");

  history.pushState("", document.title, window.location.pathname);

}


var transparent = true;
var big_image;

var transparentDemo = true;
var fixedTop = false;

var navbar_initialized,
  backgroundOrange = false,
  toggle_initialized = false;

var $datepicker = $('.datepicker');
var $collapse = $('.navbar .collapse');
var $html = $('html');

(function () {
  var isWindows = navigator.platform.indexOf('Win') > -1 ? true : false;

  if (isWindows) {
    // if we are on windows OS we activate the perfectScrollbar function


    if ($('.tab-content .table-responsive').length != 0) {

      $('.table-responsive').each(function () {
        var ps2 = new PerfectScrollbar($(this)[0]);
      });
    }



    $html.addClass('perfect-scrollbar-on');
  } else {
    $html.addClass('perfect-scrollbar-off');
  }
})();

$(document).ready(function () {
  //  Activate the Tooltips
  $('[data-toggle="tooltip"], [rel="tooltip"]').tooltip();

  // Activate Popovers and set color for popovers
  $('[data-toggle="popover"]').each(function () {
    color_class = $(this).data('color');
    $(this).popover({
      template: '<div class="popover popover-' + color_class + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
    });
  });

  var squares1 = document.getElementById("square1");
  var squares2 = document.getElementById("square2");
  var squares3 = document.getElementById("square3");
  var squares4 = document.getElementById("square4");
  var squares5 = document.getElementById("square5");
  var squares6 = document.getElementById("square6");
  var squares9 = document.getElementById("square7");
  var squares10 = document.getElementById("square8");

  if ($('.square').length != 0) {

    $(document).mousemove(function (e) {
      posX = event.clientX - window.innerWidth / 2;
      posY = event.clientY - window.innerWidth / 6;

      squares1.style.transform = "perspective(500px) rotateY(" + posX * 0.05 + "deg) rotateX(" + posY * (-0.05) + "deg)";
      squares2.style.transform = "perspective(500px) rotateY(" + posX * 0.05 + "deg) rotateX(" + posY * (-0.05) + "deg)";
      squares3.style.transform = "perspective(500px) rotateY(" + posX * 0.05 + "deg) rotateX(" + posY * (-0.05) + "deg)";
      squares4.style.transform = "perspective(500px) rotateY(" + posX * 0.05 + "deg) rotateX(" + posY * (-0.05) + "deg)";
      squares5.style.transform = "perspective(500px) rotateY(" + posX * 0.05 + "deg) rotateX(" + posY * (-0.05) + "deg)";
      squares6.style.transform = "perspective(500px) rotateY(" + posX * 0.05 + "deg) rotateX(" + posY * (-0.05) + "deg)";
      squares9.style.transform = "perspective(500px) rotateY(" + posX * 0.02 + "deg) rotateX(" + posY * (-0.02) + "deg)";
      squares10.style.transform = "perspective(500px) rotateY(" + posX * 0.02 + "deg) rotateX(" + posY * (-0.02) + "deg)";

    });
  }

  // Activate the image for the navbar-collapse
  blackKit.initNavbarImage();

  $navbar = $('.navbar[color-on-scroll]');
  scroll_distance = $navbar.attr('color-on-scroll') || 500;

  // Check if we have the class "navbar-color-on-scroll" then add the function to remove the class "navbar-transparent" so it will transform to a plain color.

  if ($('.navbar[color-on-scroll]').length != 0) {
    blackKit.checkScrollForTransparentNavbar();
    $(window).on('scroll', blackKit.checkScrollForTransparentNavbar)
  }

  $('.form-control').on("focus", function () {
    $(this).parent('.input-group').addClass("input-group-focus");
  }).on("blur", function () {
    $(this).parent(".input-group").removeClass("input-group-focus");
  });

  // Activate bootstrapSwitch
  $('.bootstrap-switch').each(function () {
    $this = $(this);
    data_on_label = $this.data('on-label') || '';
    data_off_label = $this.data('off-label') || '';

    $this.bootstrapSwitch({
      onText: data_on_label,
      offText: data_off_label
    });
  });

  // Activate Carousel
  $('.carousel').carousel({
    interval: false
  });
});

// Methods

function hideNavbarCollapse($this) {
  $this.addClass('collapsing-out');
}

function hiddenNavbarCollapse($this) {
  $this.removeClass('collapsing-out');
}


// Events

if ($collapse.length) {
  $collapse.on({
    'hide.bs.collapse': function () {
      hideNavbarCollapse($collapse);
    }
  })

  $collapse.on({
    'hidden.bs.collapse': function () {
      hiddenNavbarCollapse($collapse);
    }
  })
}


// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
  var timeout;
  return function () {
    var context = this,
      args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    }, wait);
    if (immediate && !timeout) func.apply(context, args);
  };
};

$(document).on('click', '.navbar-toggler', function () {
  $toggle = $(this);

  if (blackKit.misc.navbar_menu_visible == 1) {
    $('html').removeClass('nav-open');
    blackKit.misc.navbar_menu_visible = 0;
    $('#bodyClick').remove();
    setTimeout(function () {
      $toggle.removeClass('toggled');
    }, 550);
  } else {
    setTimeout(function () {
      $toggle.addClass('toggled');
    }, 580);
    div = '<div id="bodyClick"></div>';
    $(div).appendTo('body').click(function () {
      $('html').removeClass('nav-open');
      blackKit.misc.navbar_menu_visible = 0;
      setTimeout(function () {
        $toggle.removeClass('toggled');
        $('#bodyClick').remove();
      }, 550);
    });

    $('html').addClass('nav-open');
    blackKit.misc.navbar_menu_visible = 1;
  }
});

blackKit = {
  misc: {
    navbar_menu_visible: 0
  },

  checkScrollForTransparentNavbar: debounce(function () {
    if ($(document).scrollTop() > scroll_distance) {
      if (transparent) {
        transparent = false;
        $('.navbar[color-on-scroll]').removeClass('navbar-transparent');
      }
    } else {
      if (!transparent) {
        transparent = true;
        $('.navbar[color-on-scroll]').addClass('navbar-transparent');
      }
    }
  }, 17),

  initNavbarImage: function () {
    var $navbar = $('.navbar').find('.navbar-translate').siblings('.navbar-collapse');
    var background_image = $navbar.data('nav-image');

    if ($(window).width() < 991 || $('body').hasClass('burger-menu')) {
      if (background_image != undefined) {
        $navbar.css('background', "url('" + background_image + "')")
          .removeAttr('data-nav-image')
          .css('background-size', "cover")
          .addClass('has-image');
      }
    } else if (background_image != undefined) {
      $navbar.css('background', "")
        .attr('data-nav-image', '' + background_image + '')
        .css('background-size', "")
        .removeClass('has-image');
    }
  },

  initDatePicker: function () {
    if ($datepicker.length != 0) {
      $datepicker.datetimepicker({
        icons: {
          time: "tim-icons icon-watch-time",
          date: "tim-icons icon-calendar-60",
          up: "fa fa-chevron-up",
          down: "fa fa-chevron-down",
          previous: 'tim-icons icon-minimal-left',
          next: 'tim-icons icon-minimal-right',
          today: 'fa fa-screenshot',
          clear: 'fa fa-trash',
          close: 'fa fa-remove'
        }
      });
    }
  },

  initSliders: function () {
    // Sliders for demo purpose in refine cards section
    var slider = document.getElementById('sliderRegular');
    if ($('#sliderRegular').length != 0) {

      noUiSlider.create(slider, {
        start: 40,
        connect: [true, false],
        range: {
          min: 0,
          max: 100
        }
      });
    }

    var slider2 = document.getElementById('sliderDouble');

    if ($('#sliderDouble').length != 0) {

      noUiSlider.create(slider2, {
        start: [20, 60],
        connect: true,
        range: {
          min: 0,
          max: 100
        }
      });
    }
  }
}



// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
  var timeout;
  return function () {
    var context = this,
      args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    }, wait);
    if (immediate && !timeout) func.apply(context, args);
  };
};


let columns = Math.floor(window.innerWidth / 50),
  rows = Math.floor(window.innerHeight / 50);

const createTile = index => {
  const tile = document.createElement('div');
  tile.classList.add('tile');
  tile.style.opacity = (preanimate ? 1 : 0);

  tile.setAttribute('data-tile-index', index);



  return tile;
}

wrapper = document.getElementById("loaderGrid");

wrapper.style.display = (preanimate ? "grid" : "none");

wrapper.style.setProperty('--cols', columns);
wrapper.style.setProperty('--rows', rows);

const createTiles = quantity => {
  Array.from(Array(quantity)).map((tile, index) => {
    wrapper.appendChild(createTile(index));
  });
}

createTiles(columns * rows);

function showLoader(x,y) {
  wrapper.style.display = "grid"; 
  // get the index of the tile the mouse is over
  let index = Math.floor(y / 50) * columns + Math.floor(x / 50);
  console.log(index);
  // stagger animation through the tiles using GSAP from the tile the mouse is over
  // disable scroll
  document.body.style.overflow = "hidden";
  // make a wave of tiles appear (all tiles should get 1 opacity in a wave)
  gsap.to(".tile", {
    duration: 0.4,
    opacity: 1,
    stagger: {
      each: 0.0005,
      from: index,
      axis: "x",
      }
  });

}

if (preanimate) {
  // we need to hide the loaderGrid with the same animation
  // get the index of the tile the mouse is over
  let index = Math.floor(cY / 50) * columns + Math.floor(cX / 50);
  console.log(index);
  // stagger animation through the tiles using GSAP from the tile the mouse is over
  // disable scroll
  // make a wave of tiles appear (all tiles should get 1 opacity in a wave)
  $("#fullFill").hide();
  gsap.to(".tile", {
    duration: 0.4,
    opacity: 0,
    stagger: {
      each: 0.0005,
      from: index,
      axis: "x",
    }
  });
  setTimeout(function () {
    wrapper.style.display = "none";
  }, 600);
}

// when clicked on *[alink] (use jquery)
$(document).on('click', '[alink]', function (e) {
  e.preventDefault();
  var link = $(this).attr('alink');
  showLoader(e.clientX, e.clientY);
  setTimeout(function () {
    // if the url already has query params, add & to the end of the url
    if (link.indexOf('?') > -1) {
      link += '&';
    } else {
      link += '?';
    }
    window.location.href = link+"ani=true&cX="+e.clientX+"&cY="+e.clientY;
  }, 600);
});

// when clicked on *[asubmit] (use jquery)
$(document).on('click', '[asubmit]', function (e) {
  e.preventDefault();
  var form = $(this).attr('asubmit');
  var form = $(form);
  showLoader(e.clientX, e.clientY);
  setTimeout(function () {
    // at the end of the action of the form put ?ani=true&cX="+e.clientX+"&cY="+e.clientY
    if (form.attr('action') == undefined) {
      // make the form action the current page
      form.attr('action', window.location.href+"?ani=true&cX="+e.clientX+"&cY="+e.clientY);
    } else {
      form.attr('action', form.attr('action') + "?ani=true&cX=" + e.clientX + "&cY=" + e.clientY);
    }
    form.submit();
  }, 600);
});

// prevent using enter to submit forms. Instead click on the submit button
$(document).on('keypress', 'form', function (e) {
  var key = e.which;
  if (key == 13) {
    e.preventDefault();
    $("*[asubmit='" + $(this).attr('id') + "']").click();
    return false;
  }
}); 


var colorRange = document.querySelector('.color-range')
if (colorRange) {
  var randomRange = Math.floor(100*Math.random())
  var colorChoice = document.getElementById("color-choice")

  colorRange.addEventListener('input', function(e) {
    var hue = ((this.value/100)*360).toFixed(0)
    var hsl = "hsl("+ hue + ", 100%, 50%)"
    var bgHsl = "hsl("+ hue + ", 100%, 95%)"
    colorRange.style.color = hsl
    colorChoice.style.color = hsl
    colorChoice.innerHTML = hsl
    document.body.style.background = bgHsl
  });
  colorRange.value = randomRange;
  var event = new Event('input');
  colorRange.dispatchEvent(event);
}