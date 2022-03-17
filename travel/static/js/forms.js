$(function () {
    function init_popup() {
        $('.modal_form select').select2();

        new Select2Cascade($('.modal_form #a_country'), $('.modal_form #a_region'), '/api/get_regions', {parent_id: ''});
        new Select2Cascade($('.modal_form #a_region'), $('.modal_form #a_city'), '/api/get_city', {parent_id: ''});
        select2_loadonclick($('.modal_form #a_country'), '/api/get_country');

        $('.modal_form #a_city').select2().on("change", function (e) {
            $('.modal_form #a_zipcode').removeAttr('disabled');
        });
    }

    function select2_loadonclick(el, url) {
        el.next().on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            $.getJSON(url, {}, function(items) {
                var newOptions = '<option value="">-- Select --</option>';
                var sorted = items.sort(function(a, b) {
                  return a[1] > b[1];
                });
                for(var id in sorted) {
                    var e = sorted[id];
                    newOptions += '<option value="'+ e[0] +'">'+ e[1] +'</option>';
                }

                el.select2('destroy').html(newOptions).prop("disabled", false)
                    .select2({ width: 'resolve', placeholder: "-- Select --" }).select2("open");
            });
        });
    }

    var $resetForm = $('#reset-form'),
        $resetFormMsg = $('#reset-form .msg');

    $resetForm.parsley({
        errorClass: 'error',
        listeners: {
            onFormValidate: function (isFormValid, event, ParsleyForm) {
                if (isFormValid) {
                    ParsleyForm.$element.ajaxSubmit({
                        dataType: "json",
                        success: function (data) {
                            if (data.success) {
                                $.fancybox.open($('div#reset-success'));
                            } else {
                                $resetFormMsg.text(data.error_msg);
                            }
                        }
                    });
                }
                return false;
            }
        }
    });

    function init_home() {
        if (0 == $('#search-form').length)
            return

        $('#landing select').select2();
        new Select2Cascade($('#country'), $('#region'), '/api/get_regions', {parent_id: ''});
        new Select2Cascade($('#region'), $('#city'), '/api/get_city', {parent_id: ''});

        var $searchForm = $('#search-form');

        $searchForm.parsley({
            errorClass: 'error',
        });
    }

    var $registerForm = $('#register-form'),
        $registerFormMsg = $('#register-form .msg');

    $registerForm.parsley({
        errorClass: 'error',
        listeners: {
            onFormValidate: function (isFormValid, event, ParsleyForm) {
                if (isFormValid) {
                    ParsleyForm.$element.ajaxSubmit({
                        dataType: "json",
                        success: function (data) {
                            if (data.success) {
                                if (window.location.pathname.startsWith('/cart/')) {
                                  window.location.reload();
                                } else {
                                    location.href = data.redirect_to;
                                }
                            } else {
                                $registerFormMsg.text(data.error_msg);
                            }
                        }
                    });
                }
                return false;
            }
        }
    });

    var $addressForm = $('#address-form'),
        $addressFormMsg = $('#address-form .msg');

    $addressForm.parsley({
        errorClass: 'error',
        excluded: 'input[type=hidden], input[type=file]',
        listeners: {
            onFormValidate: function (isFormValid, event, ParsleyForm) {
                if (isFormValid) {
                    $paymentFormMsg.text('');
                    $('#internal-wrap').addClass('loading');
                    ParsleyForm.$element.ajaxSubmit({
                        dataType: "json",
                        success: function (data) {
                            if (data.success) {
                                $('#internal-wrap').removeClass('loading');
                                if (window.location.pathname.startsWith('/account')) {
                                  var $li = $('.addresses ul li:last').clone();
                                  $li.children().find('input').attr('id', 'address_'+data.id);
                                  $li.children().find('input').attr('data-id', data.id);
                                  $li.children().find('label').attr('for', 'address_'+data.id);
                                  $li.children().find('label').html(data.label)
                                  $li.children().find('a').attr('data-id', data.id);
                                  $li.css('display', 'inherit');
                                  $('.addresses ul').append($li);

                                  $.fancybox.close();
                                } else {
                                  var $li = $('#select_address ul li:last').clone();
                                  $li.children().find('input').attr('id', 'address_'+data.id);
                                  $li.children().find('input').attr('data-id', data.id);
                                  $li.children().find('label').attr('for', 'address_'+data.id);
                                  $li.children().find('label').html(data.label)
                                  $li.children().find('a').attr('data-id', data.id);
                                  $li.css('display', 'inherit');
                                  $('#select_address ul').append($li);

                                  $.fancybox.open($('div#select_address'));
                                }
                            } else {
                                $addressFormMsg.text(data.error_msg);
                            }
                        }
                    });
                }
                return false;
            }
        }
    });

    var $paymentForm = $('#payment-form'),
        $paymentFormMsg = $('#payment-form .msg');

    $paymentForm.parsley({
        errorClass: 'error',
        excluded: 'input[type=hidden], input[type=file]',
        listeners: {
            onFormValidate: function (isFormValid, event, ParsleyForm) {
                if (isFormValid) {
                    $('#internal-wrap').addClass('loading');
                    Stripe.card.createToken($paymentForm, paymentStripeCallback);
                }
                return false;
            }
        }
    });

    paymentStripeCallback = function(status, response) {
        if (response.error) { // Problem!
            $('#internal-wrap').removeClass('loading');
            $paymentFormMsg.text(response.error.message);
        } else {
            var token = response.id;
            $paymentForm.append($('<input type="hidden" name="token">').val(token));
            $paymentForm.ajaxSubmit({
                dataType: "json",
                success: function (data) {
                    $('#internal-wrap').removeClass('loading');
                    if (data.success) {
                        if (window.location.pathname.startsWith('/account')) {
                            var $li = $('.payments ul li:last').clone();
                            $li.children().find('input').attr('id', 'payment_'+data.id);
                            $li.children().find('input').attr('data-id', data.id);
                            $li.children().find('label').attr('for', 'payment_'+data.id);
                            $li.children().find('label').html('**** **** **** ' + data.last4 + " " + data.brand);
                            $li.children().find('a').attr('data-id', data.id);
                            $li.css('display', 'inherit');
                            $('.payments ul').append($li);
                            $.fancybox.close();
                        } else {
                            var $li = $('#select_payment ul li:last').clone();
                            $li.children().find('input').attr('id', 'payment_'+data.id);
                            $li.children().find('input').attr('data-id', data.id);
                            $li.children().find('label').attr('for', 'payment_'+data.id);
                            $li.children().find('label').html('**** **** **** ' + data.last4 + " " + data.brand);
                            $li.children().find('a').attr('data-id', data.id);
                            $li.css('display', 'inherit');
                            $('#select_payment ul').append($li);

                            $.fancybox.open($('div#select_payment'));
                        }
                    } else {
                        $paymentFormMsg.text(data.error_msg);
                    }
                }
            });
        }
    }

    var $loginForm = $('#login-form'),
        $loginFormMsg = $('#login-form .msg'),
        $loginFormLogin = $('#login-form #login'),
        $loginFormPassword = $('#login-form #password');

    $loginForm.parsley({
        errorClass: 'error',
        listeners: {
            onFormValidate: function (isFormValid, event, ParsleyForm) {
                if (isFormValid) {
                    ParsleyForm.$element.ajaxSubmit({
                        dataType: "json",
                        success: function (data) {
                            if (data.success) {
                                if (window.location.pathname.startsWith('/cart/')) {
                                  window.location.reload();
                                } else {
                                    location.href = data.redirect_to;
                                }
                            } else {
                                $loginFormLogin.addClass('error');
                                $loginFormPassword.addClass('error');
                                $loginFormMsg.text(data.error_msg);
                            }
                        }
                    });
                } else {
                    $loginFormLogin.addClass('error');
                    $loginFormPassword.addClass('error');
                }
                return false;
            }
        }
    });


    function init_search_form() {
        if (0 == $('#search-results').length)
            return

        var cur_size = Cookies.get('cur_size'),
            cur_class = Cookies.get('cur_class'),
            cur_country = Cookies.get('cur_country'),
            cur_region = Cookies.get('cur_region'),
            cur_city = Cookies.get('cur_city'),
            cur_wheel = Cookies.get('cur_wheel');

        $('#refine-search-form #region').val(cur_region);
        $('#refine-search-form #country').val(cur_country);
        $('#refine-search-form #city').val(cur_city);
        if (cur_size) {
            $('#refine-search-form #size_'+cur_size).attr('checked', 'checked')
        } else {
            $('#refine-search-form #size_all').attr('checked', 'checked')
        }

        if (cur_class) {
            $('#refine-search-form #class_'+cur_class).attr('checked', 'checked')
        } else {
            $('#refine-search-form #class_all').attr('checked', 'checked')
        }

        if (cur_wheel) {
            $('#refine-search-form #wheel_'+cur_wheel).attr('checked', 'checked')
        } else {
            $('#refine-search-form #wheel_all').attr('checked', 'checked')
        }
    }

    function fade_update(el, new_val) {
        res = false;
        if (new_val != el.html()) {
            el.fadeOut(function() {
                el.html(new_val);
                el.fadeIn();
            });
            res = true;
        }
        return res;
    }

    function update_cart_item(url, cnt, dates, cart_id, luggage_id, success_f) {
        var data = {
            'cnt': cnt,
            'dates': dates,
            'cart_id': cart_id,
            'luggage_id': luggage_id
        };

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: success_f
        });
    }

    function update_cart_subtotal() {
        var subtotal = 0;
        var subcnt = 0;
        var total_save = 0;
        $('.row.results').each(function (id, el) {
            var $el = $(el);
            var full_price = parseFloat($el.find('.full_price').val());
            var price = parseFloat($el.find('.price_day').val());
            var cnt = parseInt($el.find('.cnt').val());
            var dates = $el.find('.daterange').val();
            var dates_s = dates.split(' - ');
            var from = moment(dates_s[0]);
            var to = moment(dates_s[1]);
            var days = to.diff(from, 'days') || 1;

            var sum = price*cnt*days;
            var url = $el.find('.cart_delete').data('url');
            var luggage_id = $el.find('.luggage_id').val();
            var cart_id = $el.find('.cart_id').val();

            var el_sum = $el.find('.price.final b');
            if (fade_update(el_sum, sum.toFixed(2))) {
                update_cart_item(url, cnt, dates, cart_id, luggage_id, function() {});
            }

            subcnt += cnt;
            subtotal += sum;
            total_save += full_price*cnt - sum;
        });

        fade_update($('#subtotal-price b'), subtotal.toFixed(2));
        fade_update($('#subtotal-cnt span'), subcnt);
        fade_update($('#cart_cnt'), subcnt);
        fade_update($('#subtotal-save b'), total_save>0 ? total_save.toFixed(2):0);

        if (subcnt == 0) {
            $('.row.subtotal').hide();
            $('.row.empty-cart').show();
        }
    }

    function init_cart() {
        if (0 == $('#cart').length)
            return

        $('#select_address li:first input').attr('checked', 'checked');
        $('#select_payment li:first input').attr('checked', 'checked');

        $('.results input').on('change', function(e) {
            setTimeout(function() {
                update_cart_subtotal();
            }, 500);
        });
        $('.daterange').daterangepicker({
            locale: {
                format: 'YYYY-MM-DD'
            },
        });

        $('#apply_code').on('click', function(e) {
            e.preventDefault();

            var code = $('#coupon').val();
            var data = {
                'code': code,
            };

            $.ajax({
                type: "POST",
                url: '/api/apply_coupon/',
                data: data,
                success: function (res) {
                    if (res.success) {
                        $('.code_error').hide();
                        $('#subtotal-price').addClass('strike');
                        $('#subtotal-coupon-price b').html(res.total_coupon);
                        $('#subtotal-coupon-price').removeClass('hide');
                    } else {
                        $('.code_error span').html(res.msg);
                        $('.code_error').show();
                    }
                }
            });
        });

        $('.cart_delete').on('click', function(e) {
            e.preventDefault();

            var $btn = $(this);
            var $el = $btn.parent().parent();
            var url = $el.find('.cart_delete').data('url');
            var luggage_id = $el.find('.luggage_id').val();
            var cart_id = $el.find('.cart_id').val();
            var dates = $el.find('.daterange').val();

            update_cart_item(url, 0, dates, cart_id, luggage_id, function(res) {
                  $('#cart_cnt').html(res.cnt);

                  $el.fadeOut(function() {
                      $el.remove();
                      update_cart_subtotal();
                  });
            });
        });

        $('.confirm-rental').on('click', function(e) {
            e.preventDefault();

            var $btn = $(this);
            var url = $btn.data('url');
            var urlOk = $btn.data('url-ok');
            var urlErr = $btn.data('url-error');

            var data = {
                'address': $('#select_address li input:checked').data('id'),
                'payment': $('#select_payment li input:checked').data('id')
            };

            $('#internal-wrap').addClass('loading');
            $.ajax({
              type: "POST",
              url: url,
              data: data,
              success: function(res) {
                  $('#internal-wrap').removeClass('loading');
                  if (res.success) {
                      $.fancybox.open($(urlOk));
                  } else {
                      $.fancybox.open($(urlErr));
                  }
              }
            });

        });
        update_cart_subtotal();
    }

    function update_details_total_save() {
        var full_price = parseFloat($('#full_price').val());
        var price = parseFloat($('#price_day').val());
        var cnt = parseInt($('#cnt').val());
        var dates = $('#daterange').val();
        var dates_s = dates.split(' - ');
        var from = moment(dates_s[0]);
        var to = moment(dates_s[1]);
        var days = to.diff(from, 'days') || 1;
        var sum = price*cnt*days;

        var total_save = full_price*cnt - sum;

        fade_update($('.save_text b'), total_save>0 ? total_save.toFixed(2):0);
    }

    function init_details() {
        if (0 == $('#details').length)
            return

        $('.order input').on('change', function(e) {
            setTimeout(function() {
                update_details_total_save();
            }, 500);
        });

        $('.rent_now').on('click', function(e) {
            e.preventDefault();
            var $btn = $(this);
            var url = $btn.data('url');
            var urlOk = $btn.data('url-ok');

            var data = {
                'cnt': $('#cnt').val(),
                'dates': $('#daterange').val(),
                'luggage_id': $('#luggage_id').val()
            };

            $.ajax({
              type: "POST",
              url: url,
              data: data,
              success: function(res) {
                  if (res.success) {
                      $('#cart_cnt').html(res.cnt);
                      window.location.href = urlOk;
                  } else {
                      if (res.cnt) {
                          $('.cnt_availiable .cnt').html(res.cnt);
                          $('.cnt_availiable').show();
                      }
                      $.fancybox.open($('div#cart-add-error'));
                  }
              }
            });
        });
        $('#daterange').daterangepicker({
            locale: {
                format: 'YYYY-MM-DD'
            },
        });

        $('.add_to_cart').on('click', function(e) {
            e.preventDefault();

            var $btn = $(this);
            var url = $btn.data('url');

            var data = {
                'cnt': $('#cnt').val(),
                'dates': $('#daterange').val(),
                'luggage_id': $('#luggage_id').val()
            };

            $.ajax({
              type: "POST",
              url: url,
              data: data,
              success: function(res) {
                  if (res.success) {
                      $('#cart_cnt').html(res.cnt);
                      $.fancybox.open($('div#cart-add-success'));
                  } else {
                      if (res.cnt) {
                          $('.cnt_availiable .cnt').html(res.cnt);
                          $('.cnt_availiable').show();
                      }
                      $.fancybox.open($('div#cart-add-error'));
                  }
              }
            });
        });
    }

    function init_account() {
        if (0 == $('#account').length)
            return

        var $accountForm = $('#account-form'),
            $accountFormMsg = $('#account-form .msg');

        $accountForm.parsley({
            errorClass: 'error',
            listeners: {
                onFormValidate: function (isFormValid, event, ParsleyForm) {
                    if (isFormValid) {
                        $accountFormMsg.text('');
                        ParsleyForm.$element.ajaxSubmit({
                            dataType: "json",
                            success: function (data) {
                                $accountFormMsg.text(data.msg);
                            }
                        });
                    }
                    return false;
                }
            }
        });

        $('body').on('click', '.remove_object', function (e) {
            e.preventDefault();

            var $btn = $(this);
            var url = $btn.data('url');
            var data = {
                'address_id': $btn.data('id')
            };
            $('#internal-wrap').addClass('loading');

            $.ajax({
              type: "POST",
              url: url,
              data: data,
              success: function(res) {
                $('#internal-wrap').removeClass('loading');
                $btn.parent().parent().fadeOut(function() {
                    if ($btn.parent().parent().parent().find('li').length == 1) {
                        $btn.parent().parent().parent().parent().find('.no_address').show();
                    }
                    $btn.parent().parent().remove();
                });
              }
            });
        });
    }

    var return_id = '';
    function init_orders() {
        if (0 == $('#orders').length)
            return

        $('.return_item').on('click', function (e) {
            e.preventDefault();
            var $btn = $(this);
            return_id = $btn.data('id');
            $.fancybox.open($($btn.attr('href')));
        });
        $('.return_item_send').on('click', function (e) {
            e.preventDefault();

            var $btn = $(this);
            var url = $btn.data('url');
            var data = {
                'id': return_id,
                'returndate': $('#return-item #returntime').val()
            };

            $.ajax({
              type: "POST",
              url: url,
              data: data,
              success: function(res) {
                  window.location.reload();
              }
            });
        });
    }


    init_home();
    init_search_form();
    init_cart();
    init_details();
    init_popup();
    init_account();
    init_orders();
});
