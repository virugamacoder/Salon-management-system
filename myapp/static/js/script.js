/**
 * Global variables
 */
"use strict";

var userAgent = navigator.userAgent.toLowerCase(),
	initialDate = new Date(),

	$document = $(document),
	$window = $(window),
	$html = $("html"),

	isDesktop = $html.hasClass("desktop"),
	isIE = userAgent.indexOf("msie") != -1 ? parseInt(userAgent.split("msie")[1]) : userAgent.indexOf("trident") != -1 ? 11 : userAgent.indexOf("edge") != -1 ? 12 : false,
	isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
	isTouch = "ontouchstart" in window,
	perspectiveMenu = $('#perspective'),

	plugins = {
		pointerEvents: isIE < 11 ? "js/pointer-events.min.js" : false,
		bootstrapTooltip: $("[data-toggle='tooltip']"),
		bootstrapModalDialog: $('.modal'),
		bootstrapTabs: $(".tabs"),
		rdNavbar: $(".rd-navbar"),
		rdParallax: $(".rd-parallax"),
		rdGoogleMaps: $(".rd-google-map"),
		rdMailForm: $(".rd-mailform"),
		captcha: $('.recaptcha'),
		rdInputLabel: $(".form-label"),
		regula: $("[data-constraints]"),
		owl: $(".owl-carousel"),
		statefulButton: $('.btn-stateful'),
		isotope: $(".isotope"),
		popover: $('[data-toggle="popover"]'),
		viewAnimate: $('.view-animate'),
		photoSwipeGallery: $("[data-photo-swipe-item]"),
		radio: $("input[type='radio']"),
		checkbox: $("input[type='checkbox']"),
		customToggle: $("[data-custom-toggle]"),
		counter: $(".counter"),
		progressBar: $(".progress-bar-js"),
		selectFilter: $("select"),
		slick: $('.slick-slider'),
		stepper: $("input[type='number']"),
		materialTabs: $('.rd-material-tabs'),
		copyrightYear: $("#copyright-year")
	};


/**
 * Initialize All Scripts
 */
$document.ready(function () {
	
	/**
	 * isScrolledIntoView
	 * @description  check the element whas been scrolled into the view
	 */
	function isScrolledIntoView(elem) {
		var $window = $(window);
		return elem.offset().top + elem.outerHeight() >= $window.scrollTop() && elem.offset().top <= $window.scrollTop() + $window.height();
	}

	/**
	 * initOnView
	 * @description  calls a function when element has been scrolled into the view
	 */
	function lazyInit(element, func) {
		var $win = jQuery(window);
		$win.on('load scroll', function () {
			if ((!element.hasClass('lazy-loaded') && (isScrolledIntoView(element)))) {
				func.call();
				element.addClass('lazy-loaded');
			}
		});
	}

	/**
	 * attachFormValidator
	 * @description  attach form validation to elements
	 */
	function attachFormValidator(elements) {
		for (var i = 0; i < elements.length; i++) {
			var o = $(elements[i]),
				v;
			o.addClass("form-control-has-validation").after("<span class='form-validation'></span>");
			v = o.parent().find(".form-validation");
			if (v.is(":last-child")) {
				o.addClass("form-control-last-child");
			}
		}

		elements
			.on('input change propertychange blur', function (e) {
				var $this = $(this),
					results;

				if (e.type !== "blur") {
					if (!$this.parent().hasClass("has-error")) {
						return;
					}
				}

				if ($this.parents('.rd-mailform').hasClass('success')) {
					return;
				}

				if ((results = $this.regula('validate')).length) {
					for (i = 0; i < results.length; i++) {
						$this.siblings(".form-validation").text(results[i].message).parent().addClass("has-error")
					}
				} else {
					$this.siblings(".form-validation").text("").parent().removeClass("has-error")
				}
			})
			.regula('bind');

		var regularConstraintsMessages = [{
				type: regula.Constraint.Required,
				newMessage: "The text field is required."
			},
			{
				type: regula.Constraint.Email,
				newMessage: "The email is not a valid email."
			},
			{
				type: regula.Constraint.Numeric,
				newMessage: "Only numbers are required"
			},
			{
				type: regula.Constraint.Selected,
				newMessage: "Please choose an option."
			}
		];

		for (var i = 0; i < regularConstraintsMessages.length; i++) {
			var regularConstraint = regularConstraintsMessages[i];

			regula.override({
				constraintType: regularConstraint.type,
				defaultMessage: regularConstraint.newMessage
			});
		}
	}

	/**
	 * isValidated
	 * @description  check if all elemnts pass validation
	 */
	function isValidated(elements, captcha) {
		var results, errors = 0;

		if (elements.length) {
			for (j = 0; j < elements.length; j++) {

				var $input = $(elements[j]);
				if ((results = $input.regula('validate')).length) {
					for (k = 0; k < results.length; k++) {
						errors++;
						$input.siblings(".form-validation").text(results[k].message).parent().addClass("has-error");
					}
				} else {
					$input.siblings(".form-validation").text("").parent().removeClass("has-error")
				}
			}

			if (captcha) {
				if (captcha.length) {
					return validateReCaptcha(captcha) && errors == 0
				}
			}

			return errors == 0;
		}
		return true;
	}

	/**
	 * validateReCaptcha
	 * @description  validate google reCaptcha
	 */
	function validateReCaptcha(captcha) {
		var captchaToken = captcha.find('.g-recaptcha-response').val();

		if (captchaToken.length === 0) {
			captcha
				.siblings('.form-validation')
				.html('Please, prove that you are not robot.')
				.addClass('active');
			captcha
				.closest('.form-group')
				.addClass('has-error');

			captcha.on('propertychange', function () {
				var $this = $(this),
					captchaToken = $this.find('.g-recaptcha-response').val();

				if (captchaToken.length > 0) {
					$this
						.closest('.form-group')
						.removeClass('has-error');
					$this
						.siblings('.form-validation')
						.removeClass('active')
						.html('');
					$this.off('propertychange');
				}
			});

			return false;
		}

		return true;
	}

	/**
	 * onloadCaptchaCallback
	 * @description  init google reCaptcha
	 */
	window.onloadCaptchaCallback = function () {
		for (i = 0; i < plugins.captcha.length; i++) {
			var $capthcaItem = $(plugins.captcha[i]);

			grecaptcha.render(
				$capthcaItem.attr('id'), {
					sitekey: $capthcaItem.attr('data-sitekey'),
					size: $capthcaItem.attr('data-size') ? $capthcaItem.attr('data-size') : 'normal',
					theme: $capthcaItem.attr('data-theme') ? $capthcaItem.attr('data-theme') : 'light',
					callback: function (e) {
						$('.recaptcha').trigger('propertychange');
					}
				}
			);
			$capthcaItem.after("<span class='form-validation'></span>");
		}
	};

	/**
	 * Init Bootstrap tooltip
	 * @description  calls a function when need to init bootstrap tooltips
	 */
	function initBootstrapTooltip(tooltipPlacement) {
		if (window.innerWidth < 599) {
			plugins.bootstrapTooltip.tooltip('destroy');
			plugins.bootstrapTooltip.tooltip({
				placement: 'bottom'
			});
		} else {
			plugins.bootstrapTooltip.tooltip('destroy');
			plugins.bootstrapTooltip.tooltipPlacement;
			plugins.bootstrapTooltip.tooltip();
		}
	}

	/**
	 * Copyright Year
	 * @description  Evaluates correct copyright year
	 */
	if (plugins.copyrightYear.length) {
		plugins.copyrightYear.text(initialDate.getFullYear());
	}

	/**
	 * IE Polyfills
	 * @description  Adds some loosing functionality to IE browsers
	 */
	if (isIE) {
		if (isIE < 10) {
			$html.addClass("lt-ie-10");
		}

		if (isIE < 11) {
			if (plugins.pointerEvents) {
				$.getScript(plugins.pointerEvents)
					.done(function () {
						$html.addClass("ie-10");
						PointerEventsPolyfill.initialize({});
					});
			}
		}

		if (isIE === 11) {
			$("html").addClass("ie-11");
		}

		if (isIE === 12) {
			$("html").addClass("ie-edge");
		}
	}

	/**
	 * Bootstrap Tooltips
	 * @description Activate Bootstrap Tooltips
	 */
	if (plugins.bootstrapTooltip.length) {
		var tooltipPlacement = plugins.bootstrapTooltip.attr('data-placement');
		initBootstrapTooltip(tooltipPlacement);
		$(window).on('resize orientationchange', function () {
			initBootstrapTooltip(tooltipPlacement);
		})
	}

	/**
	 * bootstrapModalDialog
	 * @description Stap vioeo in bootstrapModalDialog
	 */
	if (plugins.bootstrapModalDialog.length > 0) {
		var i = 0;

		for (i = 0; i < plugins.bootstrapModalDialog.length; i++) {
			var modalItem = $(plugins.bootstrapModalDialog[i]);

			modalItem.on('hidden.bs.modal', $.proxy(function () {
				var activeModal = $(this),
					rdVideoInside = activeModal.find('video'),
					youTubeVideoInside = activeModal.find('iframe');

				if (rdVideoInside.length) {
					rdVideoInside[0].pause();
				}

				if (youTubeVideoInside.length) {
					var videoUrl = youTubeVideoInside.attr('src');

					youTubeVideoInside
						.attr('src', '')
						.attr('src', videoUrl);
				}
			}, modalItem))
		}
	}

	/**
	 * RD Google Maps
	 * @description Enables RD Google Maps plugin
	 */
	if (plugins.rdGoogleMaps.length) {
		var i;

		$.getScript("//maps.google.com/maps/api/js?key=AIzaSyAFeB0kVA6ouyJ_gEvFbMaefLy3cBCyRwo&sensor=false&libraries=geometry,places&v=3.7", function () {
			var head = document.getElementsByTagName('head')[0],
				insertBefore = head.insertBefore;

			head.insertBefore = function (newElement, referenceElement) {
				if (newElement.href && newElement.href.indexOf('//fonts.googleapis.com/css?family=Roboto') != -1 || newElement.innerHTML.indexOf('gm-style') != -1) {
					return;
				}
				insertBefore.call(head, newElement, referenceElement);
			};

			function initGoogleMap() {
				var $this = $(this),
					styles = $this.attr("data-styles");

				$this.googleMap({
					styles: styles ? JSON.parse(styles) : [],
					onInit: function (map) {
						var inputAddress = $('#rd-google-map-address');

						if (inputAddress.length) {
							var input = inputAddress;
							var geocoder = new google.maps.Geocoder();
							var marker = new google.maps.Marker({
								map: map,
								icon: "images/gmap_marker.png",
							});
							var autocomplete = new google.maps.places.Autocomplete(inputAddress[0]);
							autocomplete.bindTo('bounds', map);
							inputAddress.attr('placeholder', '');
							inputAddress.on('change', function () {
								$("#rd-google-map-address-submit").trigger('click');
							});
							inputAddress.on('keydown', function (e) {
								if (e.keyCode == 13) {
									$("#rd-google-map-address-submit").trigger('click');
								}
							});


							$("#rd-google-map-address-submit").on('click', function (e) {
								e.preventDefault();
								var address = input.val();
								geocoder.geocode({
									'address': address
								}, function (results, status) {
									if (status == google.maps.GeocoderStatus.OK) {
										var latitude = results[0].geometry.location.lat();
										var longitude = results[0].geometry.location.lng();

										map.setCenter(new google.maps.LatLng(
											parseFloat(latitude),
											parseFloat(longitude)
										));
										marker.setPosition(new google.maps.LatLng(
											parseFloat(latitude),
											parseFloat(longitude)
										))
									}
								});
							});
						}
					}
				});
			}

			for (i = 0; i < plugins.rdGoogleMaps.length; i++) {
				initGoogleMap.bind(plugins.rdGoogleMaps[i])();
			}
		});
	}

	/**
	 * Radio
	 * @description Add custom styling options for input[type="radio"]
	 */
	if (plugins.radio.length) {
		var i;
		for (i = 0; i < plugins.radio.length; i++) {
			var $this = $(plugins.radio[i]);
			$this.addClass("radio-custom").after("<span class='radio-custom-dummy'></span>")
		}
	}

	/**
	 * Checkbox
	 * @description Add custom styling options for input[type="checkbox"]
	 */
	if (plugins.checkbox.length) {
		var i;
		for (i = 0; i < plugins.checkbox.length; i++) {
			var $this = $(plugins.checkbox[i]);
			$this.addClass("checkbox-custom").after("<span class='checkbox-custom-dummy'></span>")
		}
	}

	/**
	 * Popovers
	 * @description Enables Popovers plugin
	 */
	if (plugins.popover.length) {
		if (window.innerWidth < 767) {
			plugins.popover.attr('data-placement', 'bottom');
			plugins.popover.popover();
		} else {
			plugins.popover.popover();
		}
	}

	/**
	 * Bootstrap Buttons
	 * @description  Enable Bootstrap Buttons plugin
	 */
	if (plugins.statefulButton.length) {
		$(plugins.statefulButton).on('click', function () {
			var statefulButtonLoading = $(this).button('loading');

			setTimeout(function () {
				statefulButtonLoading.button('reset')
			}, 2000);
		})
	}

	/**
	 * RD Navbar
	 * @description Enables RD Navbar plugin
	 */
	if (plugins.rdNavbar.length) {
		plugins.rdNavbar.RDNavbar({
			stickUpClone: (plugins.rdNavbar.attr("data-stick-up-clone")) ? plugins.rdNavbar.attr("data-stick-up-clone") === 'true' : false
		});
		if (plugins.rdNavbar.attr("data-body-class")) {
			document.body.className += ' ' + plugins.rdNavbar.attr("data-body-class");
		}
	}

	/**
	 * ViewPort Universal
	 * @description Add class in viewport
	 */
	if (plugins.viewAnimate.length) {
		var i;
		for (i = 0; i < plugins.viewAnimate.length; i++) {
			var $view = $(plugins.viewAnimate[i]).not('.active');
			$document.on("scroll", $.proxy(function () {
					if (isScrolledIntoView(this)) {
						this.addClass("active");
					}
				}, $view))
				.trigger("scroll");
		}
	}
	/**
	 * Owl carousel
	 * @description Enables Owl carousel plugin
	 */
	if (plugins.owl.length) {
		var i;
		for (i = 0; i < plugins.owl.length; i++) {
			var c = $(plugins.owl[i]),
				responsive = {};

			var aliaces = ["-", "-xs-", "-sm-", "-md-", "-lg-"],
				values = [0, 480, 768, 992, 1200],
				j, k;

			for (j = 0; j < values.length; j++) {
				responsive[values[j]] = {};
				for (k = j; k >= -1; k--) {
					if (!responsive[values[j]]["items"] && c.attr("data" + aliaces[k] + "items")) {
						responsive[values[j]]["items"] = k < 0 ? 1 : parseInt(c.attr("data" + aliaces[k] + "items"));
					}
					if (!responsive[values[j]]["stagePadding"] && responsive[values[j]]["stagePadding"] !== 0 && c.attr("data" + aliaces[k] + "stage-padding")) {
						responsive[values[j]]["stagePadding"] = k < 0 ? 0 : parseInt(c.attr("data" + aliaces[k] + "stage-padding"));
					}
					if (!responsive[values[j]]["margin"] && responsive[values[j]]["margin"] !== 0 && c.attr("data" + aliaces[k] + "margin")) {
						responsive[values[j]]["margin"] = k < 0 ? 30 : parseInt(c.attr("data" + aliaces[k] + "margin"));
					}
				}
			}

			// Create custom Pagination
			if (c.attr('data-dots-custom')) {
				c.on("initialized.owl.carousel", function (event) {
					var carousel = $(event.currentTarget),
						customPag = $(carousel.attr("data-dots-custom")),
						active = 0;

					if (carousel.attr('data-active')) {
						active = parseInt(carousel.attr('data-active'));
					}

					carousel.trigger('to.owl.carousel', [active, 300, true]);
					customPag.find("[data-owl-item='" + active + "']").addClass("active");

					customPag.find("[data-owl-item]").on('click', function (e) {
						e.preventDefault();
						carousel.trigger('to.owl.carousel', [parseInt(this.getAttribute("data-owl-item")), 300, true]);
					});

					carousel.on("translate.owl.carousel", function (event) {
						customPag.find(".active").removeClass("active");
						customPag.find("[data-owl-item='" + event.item.index + "']").addClass("active")
					});
				});
			}

			// Create custom Numbering
			if (typeof (c.attr("data-numbering")) !== 'undefined') {
				var numberingObject = $(c.attr("data-numbering"));

				c.on('initialized.owl.carousel changed.owl.carousel', function (numberingObject) {
					return function (e) {
						if (!e.namespace) return;
						numberingObject.find('.numbering-current').text(e.item.index + 1);
						numberingObject.find('.numbering-count').text(e.item.count);
					};
				}(numberingObject));
			}

			c.owlCarousel({
				autoplay: c.attr("data-autoplay") === "true",
				loop: c.attr("data-loop") == 'true',
				items: 1,
				dotsContainer: c.attr("data-pagination-class") || false,
				navContainer: c.attr("data-navigation-class") || false,
				mouseDrag: c.attr("data-mouse-drag") !== "false",
				nav: c.attr("data-nav") === "true",
				dots: c.attr("data-dots") === "true",
				dotsEach: c.attr("data-dots-each") ? parseInt(c.attr("data-dots-each")) : false,
				animateIn: c.attr('data-animation-in') ? c.attr('data-animation-in') : 'slide',
				animateOut: c.attr('data-animation-out') ? c.attr('data-animation-out') : false,
				responsive: responsive,
				navText: []
			});
		}
	}

	/**
	 * Isotope
	 * @description Enables Isotope plugin
	 */
	if (plugins.isotope.length) {
		var i, isogroup = [];
		for (i = 0; i < plugins.isotope.length; i++) {
			var isotopeItem = plugins.isotope[i],
				iso = new Isotope(isotopeItem, {
					itemSelector: '.isotope-item',
					layoutMode: isotopeItem.getAttribute('data-isotope-layout') ? isotopeItem.getAttribute('data-isotope-layout') : 'masonry',
					filter: '*'
				});

			isogroup.push(iso);
		}

		$(window).on('load', function () {
			setTimeout(function () {
				var i;
				for (i = 0; i < isogroup.length; i++) {
					isogroup[i].element.className += " isotope--loaded";
					isogroup[i].layout();
				}
			}, 600);
		});

		var resizeTimout;

		$("[data-isotope-filter]").on("click", function (e) {
			e.preventDefault();
			var filter = $(this);
			clearTimeout(resizeTimout);
			filter.parents(".isotope-filters").find('.active').removeClass("active");
			filter.addClass("active");
			var iso = $('.isotope[data-isotope-group="' + this.getAttribute("data-isotope-group") + '"]');
			iso.isotope({
				itemSelector: '.isotope-item',
				layoutMode: iso.attr('data-isotope-layout') ? iso.attr('data-isotope-layout') : 'masonry',
				filter: this.getAttribute("data-isotope-filter") == '*' ? '*' : '[data-filter*="' + this.getAttribute("data-isotope-filter") + '"]'
			});
		}).eq(0).trigger("click")
	}

	/**
	 * WOW
	 * @description Enables Wow animation plugin
	 */
	if (isDesktop && $html.hasClass("wow-animation") && $(".wow").length) {
		new WOW().init();
	}

	/**
	 * Bootstrap tabs
	 * @description Activate Bootstrap Tabs
	 */
	if (plugins.bootstrapTabs.length) {
		var i;
		for (i = 0; i < plugins.bootstrapTabs.length; i++) {
			var bootstrapTabsItem = $(plugins.bootstrapTabs[i]);

			bootstrapTabsItem.on("click", "a", function (event) {
				event.preventDefault();
				$(this).tab('show');
			});
		}
	}

	/**
	 * RD Input Label
	 * @description Enables RD Input Label Plugin
	 */
	if (plugins.rdInputLabel.length) {
		plugins.rdInputLabel.RDInputLabel();
	}

	/**
	 * Regula
	 * @description Enables Regula plugin
	 */
	if (plugins.regula.length) {
		attachFormValidator(plugins.regula);
	}

	/**
	 * Google ReCaptcha
	 * @description Enables Google ReCaptcha
	 */
	if (plugins.captcha.length) {
		$.getScript("//www.google.com/recaptcha/api.js?onload=onloadCaptchaCallback&render=explicit&hl=en");
	}

	/**
	 * RD Mailform
	 */
	if (plugins.rdMailForm.length) {
		var i, j, k,
			msg = {
				'MF000': 'Successfully sent!',
				'MF001': 'Recipients are not set!',
				'MF002': 'Form will not work locally!',
				'MF003': 'Please, define email field in your form!',
				'MF004': 'Please, define type of your form!',
				'MF254': 'Something went wrong with PHPMailer!',
				'MF255': 'Aw, snap! Something went wrong.'
			};

		for (i = 0; i < plugins.rdMailForm.length; i++) {
			var $form = $(plugins.rdMailForm[i]),
				formHasCaptcha = false;

			$form.attr('novalidate', 'novalidate').ajaxForm({
				data: {
					"form-type": $form.attr("data-form-type") || "contact",
					"counter": i
				},
				beforeSubmit: function (arr, $form, options) {

					var form = $(plugins.rdMailForm[this.extraData.counter]),
						inputs = form.find("[data-constraints]"),
						output = $("#" + form.attr("data-form-output")),
						captcha = form.find('.recaptcha'),
						captchaFlag = true;

					output.removeClass("active error success");

					if (isValidated(inputs, captcha)) {

						// veify reCaptcha
						if (captcha.length) {
							var captchaToken = captcha.find('.g-recaptcha-response').val(),
								captchaMsg = {
									'CPT001': 'Please, setup you "site key" and "secret key" of reCaptcha',
									'CPT002': 'Something wrong with google reCaptcha'
								};

							formHasCaptcha = true;

							$.ajax({
									method: "POST",
									url: "bat/reCaptcha.php",
									data: {
										'g-recaptcha-response': captchaToken
									},
									async: false
								})
								.done(function (responceCode) {
									if (responceCode !== 'CPT000') {
										if (output.hasClass("snackbars")) {
											output.html('<p><span class="icon text-middle mdi mdi-check icon-xxs"></span><span>' + captchaMsg[responceCode] + '</span></p>')

											setTimeout(function () {
												output.removeClass("active");
											}, 3500);

											captchaFlag = false;
										} else {
											output.html(captchaMsg[responceCode]);
										}

										output.addClass("active");
									}
								});
						}

						if (!captchaFlag) {
							return false;
						}

						form.addClass('form-in-process');

						if (output.hasClass("snackbars")) {
							output.html('<p><span class="icon text-middle fa fa-circle-o-notch fa-spin icon-xxs"></span><span>Sending</span></p>');
							output.addClass("active");
						}
					} else {
						return false;
					}
				},
				error: function (result) {

					var output = $("#" + $(plugins.rdMailForm[this.extraData.counter]).attr("data-form-output")),
						form = $(plugins.rdMailForm[this.extraData.counter]);

					output.text(msg[result]);
					form.removeClass('form-in-process');

					if (formHasCaptcha) {
						grecaptcha.reset();
					}
				},
				success: function (result) {

					var form = $(plugins.rdMailForm[this.extraData.counter]),
						output = $("#" + form.attr("data-form-output")),
						select = form.find('select');

					form
						.addClass('success')
						.removeClass('form-in-process');

					if (formHasCaptcha) {
						grecaptcha.reset();
					}

					result = result.length === 5 ? result : 'MF255';
					output.text(msg[result]);

					if (result === "MF000") {
						if (output.hasClass("snackbars")) {
							output.html('<p><span class="icon text-middle mdi mdi-check icon-xxs"></span><span>' + msg[result] + '</span></p>');
						} else {
							output.addClass("active success");
						}
					} else {
						if (output.hasClass("snackbars")) {
							output.html(' <p class="snackbars-left"><span class="icon icon-xxs mdi mdi-alert-outline text-middle"></span><span>' + msg[result] + '</span></p>');
						} else {
							output.addClass("active error");
						}
					}

					form.clearForm();

					if (select.length) {
						select.select2("val", "");
					}

					form.find('input, textarea').trigger('blur');

					setTimeout(function () {
						output.removeClass("active error success");
						form.removeClass('success');
					}, 3500);
				}
			});
		}
	}

	/**
	 * PhotoSwipe Gallery
	 * @description Enables PhotoSwipe Gallery plugin
	 */
	if (plugins.photoSwipeGallery.length) {

		// init image click event
		$document.delegate("[data-photo-swipe-item]", "click", function (event) {
			event.preventDefault();

			var $el = $(this),
				$galleryItems = $el.parents("[data-photo-swipe-gallery]").find("a[data-photo-swipe-item]"),
				pswpElement = document.querySelectorAll('.pswp')[0],
				encounteredItems = {},
				pswpItems = [],
				options,
				pswpIndex = 0,
				pswp;

			if ($galleryItems.length == 0) {
				$galleryItems = $el;
			}

			// loop over the gallery to build up the photoswipe items
			$galleryItems.each(function () {
				var $item = $(this),
					src = $item.attr('href'),
					size = $item.attr('data-size').split('x'),
					pswdItem;

				if ($item.is(':visible')) {

					// if we have this image the first time
					if (!encounteredItems[src]) {
						// build the photoswipe item
						pswdItem = {
							src: src,
							w: parseInt(size[0], 10),
							h: parseInt(size[1], 10),
							el: $item // save link to element for getThumbBoundsFn
						};

						// store that we already had this item
						encounteredItems[src] = {
							item: pswdItem,
							index: pswpIndex
						};

						// push the item to the photoswipe list
						pswpItems.push(pswdItem);
						pswpIndex++;
					}
				}
			});

			options = {
				index: encounteredItems[$el.attr('href')].index,

				getThumbBoundsFn: function (index) {
					var $el = pswpItems[index].el,
						offset = $el.offset();

					return {
						x: offset.left,
						y: offset.top,
						w: $el.width()
					};
				}
			};

			// open the photoswipe gallery
			pswp = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, pswpItems, options);
			pswp.init();
		});
	}

	/**
	 * Custom Toggles
	 */
	if (plugins.customToggle.length) {
		var i;

		for (i = 0; i < plugins.customToggle.length; i++) {
			var $this = $(plugins.customToggle[i]);

			$this.on('click', $.proxy(function (event) {
				event.preventDefault();
				var $ctx = $(this);
				$($ctx.attr('data-custom-toggle')).add(this).toggleClass('active');
			}, $this));

			if ($this.attr("data-custom-toggle-disable-on-blur") === "true") {
				$("body").on("click", $this, function (e) {
					if (e.target !== e.data[0] &&
						$(e.data.attr('data-custom-toggle')).find($(e.target)).length &&
						e.data.find($(e.target)).length == 0) {
						$(e.data.attr('data-custom-toggle')).add(e.data[0]).removeClass('active');
					}
				})
			}

			if ($this.attr("data-custom-toggle-hide-on-blur") === "true") {
				$("body").on("click", $this, function (e) {
					if (e.target !== e.data[0] && $(e.data.attr('data-custom-toggle')).find($(e.target)).length == 0 && e.data.find($(e.target)).length == 0) {
						$(e.data.attr('data-custom-toggle')).add(e.data[0]).removeClass('active');
					}
				})
			}
		}
	}

	/**
	 * Perspective menu
	 * @description Open menu in perspective
	 */
	if (perspectiveMenu.length) {
		var nav = $('.rd-navbar-wrap'),
			perspective = $('#perspective');
		$('#perspective-open-menu').on('click', function () {
			nav.addClass('active');
			perspective.addClass('active modalView');
		});
		$('#perspective-content-overlay').on('click', function () {
			nav.removeClass('active');
			perspective.removeClass('active');
			setTimeout(function () {
				perspective.removeClass('modalView');
			}, 400);
		});
	}
	$('#wrapper').scroll(function () {
		var scroll = $('#wrapper').scrollTop();
		if (scroll >= 76) {
			$('.page-header').addClass("stuck-page-header");
		} else {
			$('.page-header').removeClass("stuck-page-header");
		}
	});

	/**
	 * jQuery Count To
	 * @description Enables Count To plugin
	 */
	if (plugins.counter.length) {
		var i;

		for (i = 0; i < plugins.counter.length; i++) {
			var $counterNotAnimated = $(plugins.counter[i]).not('.animated');
			$document
				.on("scroll", $.proxy(function () {
					var $this = this;

					if ((!$this.hasClass("animated")) && (isScrolledIntoView($this))) {
						$this.countTo({
							refreshInterval: 40,
							speed: $this.attr("data-speed") || 1000
						});
						$this.addClass('animated');
					}
				}, $counterNotAnimated))
				.trigger("scroll");
		}
	}

	/**
	 * Progress bar
	 * @description  Enable progress bar
	 */
	if (plugins.progressBar.length) {
		var i,
			bar,
			type;

		for (i = 0; i < plugins.progressBar.length; i++) {
			var progressItem = plugins.progressBar[i];
			bar = null;

			if (progressItem.className.indexOf("progress-bar-horizontal") > -1) {
				type = 'Line';
			}

			if (progressItem.className.indexOf("progress-bar-radial") > -1) {
				type = 'Circle';
			}

			if (progressItem.getAttribute("data-stroke") && progressItem.getAttribute("data-value") && type) {
				bar = new ProgressBar[type](progressItem, {
					strokeWidth: Math.round(parseFloat(progressItem.getAttribute("data-stroke")) / progressItem.offsetWidth * 100),
					trailWidth: progressItem.getAttribute("data-trail") ? Math.round(parseFloat(progressItem.getAttribute("data-trail")) / progressItem.offsetWidth * 100) : 0,
					text: {
						value: progressItem.getAttribute("data-counter") === "true" ? '0' : null,
						className: 'progress-bar__body',
						style: null
					}
				});
				bar.svg.setAttribute('preserveAspectRatio', "none meet");
				if (type === 'Line') {
					bar.svg.setAttribute(null, "height", progressItem.getAttribute("data-stroke"));
				}

				bar.path.removeAttribute("stroke");
				bar.path.className.baseVal = "progress-bar__stroke";
				if (bar.trail) {
					bar.trail.removeAttribute("stroke");
					bar.trail.className.baseVal = "progress-bar__trail";
				}

				if (progressItem.getAttribute("data-easing") && !isIE) {
					$(document)
						.on("scroll", {
							"barItem": bar
						}, $.proxy(function (event) {
							var bar = event.data.barItem;
							var $this = $(this);

							if (this.className.indexOf("progress-bar--animated") === -1) {
								this.className += " progress-bar--animated";
								bar.animate(parseInt($this.attr("data-value")) / 100.0, {
									easing: $this.attr("data-easing"),
									duration: $this.attr("data-duration") ? parseInt($this.attr("data-duration")) : 800,
									step: function (state, b) {
										if (!b) {
											if (b._container.className.indexOf("progress-bar-horizontal") > -1 ||
												b._container.className.indexOf("progress-bar-vertical") > -1) {
												b.text.style.width = Math.abs(b.value() * 100).toFixed(0) + "%"
											}
											b.setText(Math.abs(b.value() * 100).toFixed(0));
										}
									}
								});
							}
						}, progressItem))
						.trigger("scroll");
				} else {
					bar.set(parseInt($(progressItem).attr("data-value")) / 100.0);
					bar.setText($(progressItem).attr("data-value"));
					if (type === 'Line') {
						bar.text.style.width = parseInt($(progressItem).attr("data-value")) + "%";
					}
				}
			} else {
				console.error(progressItem.className + ": progress bar type is not defined");
			}
		}
	}

	/**
	 * Select2
	 * @description Enables select2 plugin
	 */
	if (plugins.selectFilter.length) {
		var i;
		for (i = 0; i < plugins.selectFilter.length; i++) {
			var select = $(plugins.selectFilter[i]);

			select.select2({
				theme: select.attr('data-custom-theme') ? select.attr('data-custom-theme') : "bootstrap"
			}).next().addClass(select.attr("class").match(/(input-sm)|(input-lg)|($)/i).toString().replace(new RegExp(",", 'g'), " "));
		}
	}

	/**
	 * Slick carousel
	 * @description  Enable Slick carousel plugin
	 */
	if (plugins.slick.length) {
		var i;
		for (i = 0; i < plugins.slick.length; i++) {
			var $slickItem = $(plugins.slick[i]);

			$slickItem.slick({
					slidesToScroll: parseInt($slickItem.attr('data-slide-to-scroll')) || 1,
					asNavFor: $slickItem.attr('data-for') || false,
					dots: $slickItem.attr("data-dots") == "true",
					infinite: $slickItem.attr("data-loop") == "true",
					focusOnSelect: true,
					arrows: $slickItem.attr("data-arrows") == "true",
					swipe: $slickItem.attr("data-swipe") == "true",
					autoplay: $slickItem.attr("data-autoplay") == "true",
					vertical: $slickItem.attr("data-vertical") == "true",
					centerMode: $slickItem.attr("data-center-mode") == "true",
					centerPadding: $slickItem.attr("data-center-padding") ? $slickItem.attr("data-center-padding") : '0.50',
					mobileFirst: true,
					responsive: [{
							breakpoint: 0,
							settings: {
								slidesToShow: parseInt($slickItem.attr('data-items')) || 1,
							}
						},
						{
							breakpoint: 479,
							settings: {
								slidesToShow: parseInt($slickItem.attr('data-xs-items')) || 1,
							}
						},
						{
							breakpoint: 767,
							settings: {
								slidesToShow: parseInt($slickItem.attr('data-sm-items')) || 1,
							}
						},
						{
							breakpoint: 991,
							settings: {
								slidesToShow: parseInt($slickItem.attr('data-md-items')) || 1,
							}
						},
						{
							breakpoint: 1199,
							settings: {
								slidesToShow: parseInt($slickItem.attr('data-lg-items')) || 1,
								swipe: false
							}
						}
					]
				})
				.on('afterChange', function (event, slick, currentSlide, nextSlide) {
					var $this = $(this),
						childCarousel = $this.attr('data-child');

					if (childCarousel) {
						$(childCarousel + ' .slick-slide').removeClass('slick-current');
						$(childCarousel + ' .slick-slide').eq(currentSlide).addClass('slick-current');
					}
				});
		}
	}

	/**
	 * Stepper
	 * @description Enables Stepper Plugin
	 */
	if (plugins.stepper.length) {
		plugins.stepper.stepper({
			labels: {
				up: "",
				down: ""
			}
		});
	}

	/**
	 * RD MaterialTabs
	 * @description Enables RD MaterialTabs plugin
	 */
	if (plugins.materialTabs.length) {
		var i;
		for (i = 0; i < plugins.materialTabs.length; i++) {
			var materialTabsItem = plugins.materialTabs[i],
				responsive = {},
				c = $(materialTabsItem);

			var aliaces = ["-", "-xs-", "-sm-", "-md-", "-lg-"],
				values = [0, 480, 768, 992, 1200],
				j, k;

			for (j = 0; j < values.length; j++) {
				responsive[values[j]] = {};
				for (k = j; k >= -1; k--) {
					if (!responsive[values[j]]["items"] && c.attr("data" + aliaces[k] + "items")) {
						responsive[values[j]]["items"] = k < 0 ? 1 : parseInt(c.attr("data" + aliaces[k] + "items"));
					}
					if (!responsive[values[j]]["stagePadding"] && responsive[values[j]]["stagePadding"] !== 0 && c.attr("data" + aliaces[k] + "stage-padding")) {
						responsive[values[j]]["stagePadding"] = k < 0 ? 0 : parseInt(c.attr("data" + aliaces[k] + "stage-padding"));
					}
					if (!responsive[values[j]]["margin"] && responsive[values[j]]["margin"] !== 0 && c.attr("data" + aliaces[k] + "margin")) {
						responsive[values[j]]["margin"] = k < 0 ? 30 : parseInt(c.attr("data" + aliaces[k] + "margin"));
					}
				}
			}

			$(materialTabsItem).RDMaterialTabs({
				responsive: responsive,
				dragContent: true,
				speed: 800
			});
		}
	}

});