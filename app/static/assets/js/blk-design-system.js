/*!

 =========================================================
 * Blk• Design System - v1.0.0
 =========================================================

 * Product Page: https://www.creative-tim.com/product/blk-design-system
 * Copyright 2018 Creative Tim (http://www.creative-tim.com)

 * Coded by www.creative-tim.com

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */ function getQuery(
     e
 ) {
    for (var t = window.location.search.substring(1).split("&"), a = 0; a < t.length; a++) {
        var o = t[a].split("=");
        if (o[0] == e) return o[1];
    }
    return !1;
}
(preanimate = "true" == getQuery("ani")), console.log(getQuery("ani"), preanimate), preanimate && ($("#fullFill").show(), (cX = getQuery("cX")), (cY = getQuery("cY")), history.pushState("", document.title, window.location.pathname));
var big_image,
    navbar_initialized,
    transparent = !0,
    transparentDemo = !0,
    fixedTop = !1,
    backgroundOrange = !1,
    toggle_initialized = !1,
    $datepicker = $(".datepicker"),
    $collapse = $(".navbar .collapse"),
    $html = $("html");
function hideNavbarCollapse(e) {
    e.addClass("collapsing-out");
}
function hiddenNavbarCollapse(e) {
    e.removeClass("collapsing-out");
}
function debounce(e, t, a) {
    var o;
    return function () {
        var r = this,
            n = arguments;
        clearTimeout(o),
            (o = setTimeout(function () {
                (o = null), a || e.apply(r, n);
            }, t)),
            a && !o && e.apply(r, n);
    };
}
function debounce(e, t, a) {
    var o;
    return function () {
        var r = this,
            n = arguments;
        clearTimeout(o),
            (o = setTimeout(function () {
                (o = null), a || e.apply(r, n);
            }, t)),
            a && !o && e.apply(r, n);
    };
}
navigator.platform.indexOf("Win") > -1
    ? (0 != $(".tab-content .table-responsive").length &&
        $(".table-responsive").each(function () {
            new PerfectScrollbar($(this)[0]);
        }),
        $html.addClass("perfect-scrollbar-on"))
    : $html.addClass("perfect-scrollbar-off"),
    $(document).ready(function () {
        $('[data-toggle="tooltip"], [rel="tooltip"]').tooltip(),
            $('[data-toggle="popover"]').each(function () {
                (color_class = $(this).data("color")),
                    $(this).popover({ template: '<div class="popover popover-' + color_class + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>' });
            });
        var e = document.getElementById("square1"),
            t = document.getElementById("square2"),
            a = document.getElementById("square3"),
            r = document.getElementById("square4"),
            n = document.getElementById("square5"),
            l = document.getElementById("square6"),
            i = document.getElementById("square7"),
            s = document.getElementById("square8");
        0 != $(".square").length &&
            $(document).mousemove(function (c) {
                (posX = o.clientX - window.innerWidth / 2),
                    (posY = o.clientY - window.innerWidth / 6),
                    (e.style.transform = "perspective(500px) rotateY(" + 0.05 * posX + "deg) rotateX(" + -0.05 * posY + "deg)"),
                    (t.style.transform = "perspective(500px) rotateY(" + 0.05 * posX + "deg) rotateX(" + -0.05 * posY + "deg)"),
                    (a.style.transform = "perspective(500px) rotateY(" + 0.05 * posX + "deg) rotateX(" + -0.05 * posY + "deg)"),
                    (r.style.transform = "perspective(500px) rotateY(" + 0.05 * posX + "deg) rotateX(" + -0.05 * posY + "deg)"),
                    (n.style.transform = "perspective(500px) rotateY(" + 0.05 * posX + "deg) rotateX(" + -0.05 * posY + "deg)"),
                    (l.style.transform = "perspective(500px) rotateY(" + 0.05 * posX + "deg) rotateX(" + -0.05 * posY + "deg)"),
                    (i.style.transform = "perspective(500px) rotateY(" + 0.02 * posX + "deg) rotateX(" + -0.02 * posY + "deg)"),
                    (s.style.transform = "perspective(500px) rotateY(" + 0.02 * posX + "deg) rotateX(" + -0.02 * posY + "deg)");
            }),
            blackKit.initNavbarImage(),
            (scroll_distance = ($navbar = $(".navbar[color-on-scroll]")).attr("color-on-scroll") || 500),
            0 != $(".navbar[color-on-scroll]").length && (blackKit.checkScrollForTransparentNavbar(), $(window).on("scroll", blackKit.checkScrollForTransparentNavbar)),
            $(".form-control")
                .on("focus", function () {
                    $(this).parent(".input-group").addClass("input-group-focus");
                })
                .on("blur", function () {
                    $(this).parent(".input-group").removeClass("input-group-focus");
                }),
            $(".bootstrap-switch").each(function () {
                (data_on_label = ($this = $(this)).data("on-label") || ""), (data_off_label = $this.data("off-label") || ""), $this.bootstrapSwitch({ onText: data_on_label, offText: data_off_label });
            }),
            $(".carousel").carousel({ interval: !1 });
    }),
    $collapse.length &&
    ($collapse.on({
        "hide.bs.collapse": function () {
            hideNavbarCollapse($collapse);
        },
    }),
        $collapse.on({
            "hidden.bs.collapse": function () {
                hiddenNavbarCollapse($collapse);
            },
        })),
    $(document).on("click", ".navbar-toggler", function () {
        ($toggle = $(this)),
            1 == blackKit.misc.navbar_menu_visible
                ? ($("html").removeClass("nav-open"),
                    (blackKit.misc.navbar_menu_visible = 0),
                    $("#bodyClick").remove(),
                    setTimeout(function () {
                        $toggle.removeClass("toggled");
                    }, 550))
                : (setTimeout(function () {
                    $toggle.addClass("toggled");
                }, 580),
                    $((div = '<div id="bodyClick"></div>'))
                        .appendTo("body")
                        .click(function () {
                            $("html").removeClass("nav-open"),
                                (blackKit.misc.navbar_menu_visible = 0),
                                setTimeout(function () {
                                    $toggle.removeClass("toggled"), $("#bodyClick").remove();
                                }, 550);
                        }),
                    $("html").addClass("nav-open"),
                    (blackKit.misc.navbar_menu_visible = 1));
    }),
    (blackKit = {
        misc: { navbar_menu_visible: 0 },
        checkScrollForTransparentNavbar: debounce(function () {
            $(document).scrollTop() > scroll_distance
                ? transparent && ((transparent = !1), $(".navbar[color-on-scroll]").removeClass("navbar-transparent"))
                : transparent || ((transparent = !0), $(".navbar[color-on-scroll]").addClass("navbar-transparent"));
        }, 17),
        initNavbarImage: function () {
            var e = $(".navbar").find(".navbar-translate").siblings(".navbar-collapse"),
                t = e.data("nav-image");
            991 > $(window).width() || $("body").hasClass("burger-menu")
                ? void 0 != t &&
                e
                    .css("background", "url('" + t + "')")
                    .removeAttr("data-nav-image")
                    .css("background-size", "cover")
                    .addClass("has-image")
                : void 0 != t &&
                e
                    .css("background", "")
                    .attr("data-nav-image", "" + t)
                    .css("background-size", "")
                    .removeClass("has-image");
        },
        initDatePicker: function () {
            0 != $datepicker.length &&
                $datepicker.datetimepicker({
                    icons: {
                        time: "tim-icons icon-watch-time",
                        date: "tim-icons icon-calendar-60",
                        up: "fa fa-chevron-up",
                        down: "fa fa-chevron-down",
                        previous: "tim-icons icon-minimal-left",
                        next: "tim-icons icon-minimal-right",
                        today: "fa fa-screenshot",
                        clear: "fa fa-trash",
                        close: "fa fa-remove",
                    },
                });
        },
        initSliders: function () {
            var e = document.getElementById("sliderRegular");
            0 != $("#sliderRegular").length && noUiSlider.create(e, { start: 40, connect: [!0, !1], range: { min: 0, max: 100 } });
            var t = document.getElementById("sliderDouble");
            0 != $("#sliderDouble").length && noUiSlider.create(t, { start: [20, 60], connect: !0, range: { min: 0, max: 100 } });
        },
    });
let columns = Math.floor(window.innerWidth / 50),
    rows = Math.floor(window.innerHeight / 50);
const createTile = (e) => {
    let t = document.createElement("div");
    return t.classList.add("tile"), (t.style.opacity = preanimate ? 1 : 0), t.setAttribute("data-tile-index", e), t;
};
((wrapper = document.getElementById("loaderGrid")).style.display = preanimate ? "grid" : "none"), wrapper.style.setProperty("--cols", columns), wrapper.style.setProperty("--rows", rows);
const createTiles = (e) => {
    Array.from(Array(e)).map((e, t) => {
        wrapper.appendChild(createTile(t));
    });
};
function showLoader(e, t) {
    wrapper.style.display = "grid";
    let a = Math.floor(t / 50) * columns + Math.floor(e / 50);
    console.log(a), (document.body.style.overflow = "hidden"), gsap.to(".tile", { duration: 0.4, opacity: 1, stagger: { each: 5e-4, from: a, axis: "x" } });
}
if ((createTiles(columns * rows), preanimate)) {
    let e = Math.floor(cY / 50) * columns + Math.floor(cX / 50);
    console.log(e),
        $("#fullFill").hide(),
        gsap.to(".tile", { duration: 0.4, opacity: 0, stagger: { each: 5e-4, from: e, axis: "x" } }),
        setTimeout(function () {
            wrapper.style.display = "none";
        }, 600);
}
$(document).on("click", "[alink]", function (e) {
    e.preventDefault();
    var t = $(this).attr("href");
    showLoader(e.clientX, e.clientY),
        setTimeout(function () {
            t.indexOf("?") > -1 ? (t += "&") : (t += "?"), (window.location.href = t + "ani=true&cX=" + e.clientX + "&cY=" + e.clientY);
        }, 600);
}),
    $(document).on("click", "[asubmit]", function (e) {
        e.preventDefault();
        var t = $(this).attr("asubmit"),
            t = $(t);
        showLoader(e.clientX, e.clientY),
            setTimeout(function () {
                void 0 == t.attr("action") ? t.attr("action", window.location.href + "?ani=true&cX=" + e.clientX + "&cY=" + e.clientY) : t.attr("action", t.attr("action") + "?ani=true&cX=" + e.clientX + "&cY=" + e.clientY), t.submit();
            }, 600);
    }),
    $(document).on("keypress", "form", function (e) {
        if (13 == e.which) return e.preventDefault(), $("*[asubmit='" + $(this).attr("id") + "']").click(), !1;
    });

const rangeInput = document.querySelector('.js-range-input');
const output = document.querySelector('.js-range-output');
const root = document.documentElement;

function setHue() {
    output.value = rangeInput.value + '°';
    root.style.setProperty('--hue', rangeInput.value);
}

function setDefaultState() {
    rangeInput.focus();
    setHue();
}

rangeInput.addEventListener('input', function () {
    setHue();
});

document.addEventListener('DOMContentLoaded', function () {
    setDefaultState();
});