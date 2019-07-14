// Sitewide
// ********
$(".toast").toast('show', {
    autohide: false,
});

// Set CSFR token for ajax 
// Assistance from https://stackoverflow.com/questions/26029862/django-ajax-call-not-working-in-chrome-working-in-firefox?rq=1
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

// Function to send message to defined user
function send_message() {
    $.ajax({
        url: "/chat/ajax/new_message/",
        type: 'POST',
        data: {
            message_content: $('#message-input').val(),
            message_receiver: $('#message-receiver-id').val()
        },
        success: function(json) {
            // If user is not premium, redirect as informed by premium_required decorator
            if(json['redirect']) {
                window.location.href = json['redirect'];
            } else {
               $('.toast-container').html('')
                $('.toast-container').html(
                '<div data-delay="4000" class="toast fade"><div class="toast-header"><strong class="mr-auto"><i class="fa fa-globe"></i> Attention</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button></div><div class="toast-body">' + json['message'] + '</div></div>'
                );
                $(".toast").toast('show', {
                    autohide: false,
                }); 
            }
        }
    });
}

// Show message modal on click
$(".card-link-left").on('click', function(e) {
    $('#message-modal').modal('toggle', $(this))
});

// https://getbootstrap.com/docs/4.0/components/modal/#varying-modal-content
// Populate modal with necessary user information to create message record
$('#message-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var username = button.data('username');
    var username_id = button.data('user-id');
    var modal = $(this)
    modal.find('.card-form-subtitle').text('Start a conversation with ' + username);
    modal.find('#message-receiver-id').val(username_id);
});

// Send message to user on form submit
$('.not-profile-page-message-form').on('submit', function(event) {
    $('#message-modal').modal('toggle')
    // Stop page refreshing on form submit
    event.preventDefault();
    send_message();
    $('#message-input').val('')
});

// Send wink - when passing receiver_id
function send_wink_grid_link(receiver_id) {
    $.ajax({
        url: "/chat/ajax/winks/",
        datatype: 'json',
        data: {
            receiver_id: receiver_id
        },
        success: function(json) {
            $('.toast-container').html('')
            $('.toast-container').html(
                '<div data-delay="4000" class="toast fade"><div class="toast-header"><strong class="mr-auto"><i class="fa fa-globe"></i> Attention</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button></div><div class="toast-body">' + json['message'] + '</div></div>'
                );
            $(".toast").toast('show', {
                autohide: false,
            });
        }
    })
}

// Account Page
// ********

// If account form has errors, show modal on refresh
if ($("#edit-account-modal").find('.errorlist').length) {
    $('#edit-account-modal').modal('show')
}

// If password form has errors, show modal on refresh
if ($("#edit-password-modal").find('.errorlist').length) {
    $('#edit-password-modal').modal('show')
}

// Display cancel subscription modal with link to cancel sub URL
$('#cancel-message-modal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget);
    var sub_id = button.data('subid');
    var modal = $(this)
    modal.find('.single-button-modal a').attr('href', sub_id)
});

$('#delete-message-modal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var sub_id = button.data('subid');
    var modal = $(this)
    modal.find('.single-button-modal a').attr('href', sub_id);
});

// Show modal on relevant button click
$(".account-modal-button").on('click', function() {
    var modal_id = $(this).data('modal-id')
    $('#' + modal_id).modal('toggle', $(this));
});

// Chat page
// ********

if ($('#page-ref').data('page-ref') == "chat") {

    // Scroll message box to latest message
    $('.message-box-content').scrollTop($('.message-box-content')[0].scrollHeight + parseInt($('.message-box-content').css("margin-bottom")));

    // Scroll conversation list to current conversation
    var url_id = /[^/]*$/.exec(window.location.pathname)[0];
    $('li[data-id="' + url_id + '"]')[0].scrollIntoView()

    // Scroll page to top
    window.scrollTo(0, 0);

    // Periodically check if conversation has new messages, display a 'refresh' button when it does
    function new_message_check() {
        var url_id = /[^/]*$/.exec(window.location.pathname)[0];
        // https://stackoverflow.com/questions/8376525/get-value-of-a-string-after-a-slash-in-javascript
        $.ajax({
            url: '/chat/ajax/new_message_check',
            data: {
                'url_id': url_id
            },
            dataType: 'json',
            success: function(data) {
                if (data.conversation) {
                    $(".new_message_button").css("display", "flex");
                }
            },
            complete: function(data) {
                if (!data.conversation) {
                    setTimeout(new_message_check, 5000);
                }
            }
        });
    };

    // Mark all messages in conversation as read
    function read_messages() {
        var url_id = /[^/]*$/.exec(window.location.pathname)[0];
        $.ajax({
            url: "/chat/ajax/read/",
            dataType: 'json',
            data: {
                'url_id': url_id
            },
            success: function(data) {
                if (data.conversation) {
                    $(".new_message_button").css("display", "flex");
                }
                else {
                    $(".new_message_button").css("display", "none");
                    setTimeout(new_message_check(), 6000);
                }
            }
        });
    }

    read_messages()
}

// Views and winks page 
// ********

// Mark all views or winks on page as read
function read_engagement(page_type) {
    var page = $('.current').data('page')
    $.ajax({
        url: "/chat/ajax/read-" + page_type + "/",
        datatype: 'json',
        data: {
            'page': page
        },
        success: function(json) {
            if(json) {
                // If user is not premium, redirect as informed by premium_required decorator
                if(json['redirect']) {
                    window.location.href = json['redirect'];
                }
            }
        }
    });
}

if ($('#page-ref').data('page-ref') == "view" || $('#page-ref').data('page-ref') == "wink") {
    // Mark all views on page as read
    read_engagement($('#page-ref').data('page-ref'));
}


// Home
// ******

if ($('#page-ref').data('page-ref') == "home") {
    
    // Centers and rotates draggable cards
    // https://stackoverflow.com/questions/210717/using-jquery-to-center-a-div-on-the-screen
    jQuery.fn.center = function () {
    this.css("position","absolute");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2 + 250) + 
                                                $(window).scrollLeft()) + "px");
    return this;
    }
    
    $('.draggable-card').each(function() {
            $(this).center()
        });
    
    $( window ).resize(function() {
       $('.draggable-card').each(function() {
            $(this).center()
        });
    });
    
    $('.draggable-card').each(function() {
        if(!$(this).hasClass('draggable-reset-card')) {
            var random_number = Math.round(Math.random()) * 2 - 1
            $(this).css("transform", "rotate(" + random_number + "deg)")
        }
    });
    
    
    // Remove links on draggable card for mobile as issues with selecting button
    // on Android Chrome
    // https://ctrlq.org/code/19616-detect-touch-screen-javascript
    function is_touch_device() {
     return (('ontouchstart' in window)
          || (navigator.MaxTouchPoints > 0)
          || (navigator.msMaxTouchPoints > 0));
    }
    
    if (is_touch_device()) {
        $('.draggable-card .interaction-container').css('display','none')
        $('.draggable-view-profile').css('display', 'block')
    } else {
        $('.draggable-view-profile').css('display', 'none')
    }
    
    // Function to remove draggable card and send wink/reject when relevant
    // option is selected
    function send_wink_draggable(receiver_id, wink=false) {
        var left_length = $(window).width() / 2
        // If dropped to wink area
        if(wink==true) {
            $("#draggable-" + receiver_id).animate({
                left: "+=" + left_length,
                top: "-=25"
            }, 400, "easeOutQuart", function() {
                $(this).css('display', 'none')
            });
        
            $.ajax({
            url: "/chat/ajax/winks/",
            datatype: 'json',
            data: {
                receiver_id: receiver_id
            },
            success: function(json) {
                $('.toast-container').html('')
                $('.toast-container').html(
                    '<div data-delay="4000" class="toast fade"><div class="toast-header"><strong class="mr-auto"><i class="fa fa-globe"></i> Attention</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button></div><div class="toast-body">' + json['message'] + '</div></div>'
                );
                $(".toast").toast('show', {
                    autohide: false,
                });
            }
            });
            // If not dropped to wink area
        } else {
            $("#draggable-" + receiver_id).animate({
                left: "+=" + -left_length,
                top: "-=25"
            }, 400, "easeOutQuart", function() {
                $(this).css('display', 'none')
            });
                
            $.ajax({
            url: "/chat/ajax/reject/",
            datatype: 'json',
            data: {
                receiver_id: receiver_id
            }
            
            });
        }
    }
    
    // Function to send wink/reject when dropped in relevant area
    function send_engagement(ui, engagement) {
        $.ajax({
            url: "/chat/ajax/" + engagement + "/",
            datatype: 'json',
            data: {
                receiver_id: ui.draggable.attr('id').replace('draggable-','')
            },
            success: function(json) {
                $('.toast-container').html('')
                $('.toast-container').html(
                    '<div data-delay="4000" class="toast fade"><div class="toast-header"><strong class="mr-auto"><i class="fa fa-globe"></i> Attention</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button></div><div class="toast-body">' + json['message'] + '</div></div>'
                )
                $(".toast").toast('show', {
                    autohide: false,
                });
            }
        })
    }
    
    // Select quick swipe messages and turn opacity to 0
    const messages = [$('.right-quick-match-message .text'), $('.left-quick-match-message .text')]

    function reset_quick_messages() {
          $(messages).each(function () {
                $(this).css({'border': '3px solid rgba(255, 255, 255, 0)', 'color': '3px solid rgba(255, 255, 255, 0)'})
            });
    }
    
    $( function() {
    // Initialise cards to be draggable
    $( ".draggable" ).draggable({
        // Contain them to section
        containment: "parent",
        // Because of jqueryUI bug, 'revert' is not pixel perfect, this workaround
        // from https://stackoverflow.com/questions/5603745/jquery-draggable-revert-is-not-pixel-perfect
        // has been used instead
        stop: function(event, ui) {
            this._originalPosition = this._originalPosition || ui.originalPosition;
            ui.helper.animate( this._originalPosition );
            reset_quick_messages();
        },
        drag: function(event, ui) {
            // Quick message's opacity increases as draggable card is moved to that area
            var right_distance = (-1 * ( $( "#droppable-right" ).offset().left - ($(this).offset().left + parseInt($(this).css('width'), 10))) + 100) / 100
            var left_distance = (-1 * ( $(this).offset().left) - $( "#droppable-left" ).offset().left + 100) / 100
            $('.right-quick-match-message .text').css({'color': 'rgba(255, 255, 255,' +  right_distance + ')', 'border': '3px solid rgba(255, 255, 255,' + right_distance + ')'})  
            $('.left-quick-match-message .text').css({'color': 'rgba(255, 255, 255,' +  left_distance + ')', 'border': '3px solid rgba(255, 255, 255,' + left_distance + ')'})  
        },
        scroll: false,
    });
    
    // Refresh page to add new draggable cards
    $('.draggable-reset-button').click(function(event) {
        window.location = '/home#swipe-match-finder';
    });
    
    // Initialise droppable area right
    $( "#droppable-right" ).droppable({
        greedy: true,
        tolerance: "touch",
      drop: function(event, ui) {
        // Once dropped, wink record is created and card is removed
        send_engagement(ui, 'winks');
        ui.draggable.draggable( "option", "revert", false );
        ui.draggable.css("display", "none");
        $('.' + ui.draggable.attr('id') + '.draggable-view-profile').css("display", "none");
        reset_quick_messages()
      }
    });
    
    // Initialise droppable area left
    $( "#droppable-left" ).droppable({
        greedy: true,
        tolerance: "touch",
      drop: function(event, ui) {
         // Once dropped, reject record is created and card is removed 
          send_engagement(ui, 'reject');
          ui.draggable.draggable( "option", "revert", false );
          ui.draggable.css("display", "none");
          $('.' + ui.draggable.attr('id') + '.draggable-view-profile').css("display", "none");
          reset_quick_messages()
      }
    });
  });
}

// Create Profile
// *********

// Show loading image on form submit
$('.create-profile-form').submit(function() {
    $('.loading-image').show();
});


if ($('#page-ref').data('page-ref') == "create_profile") {
    // Google Maps API function to bias autocomplete to user's current location
    function geolocate() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var geolocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                var circle = new google.maps.Circle({ center: geolocation, radius: position.coords.accuracy });
                autocomplete.setBounds(circle.getBounds());
            });
        }
    }
    
    // Display image when file input is used
    // http://jsfiddle.net/LvsYc/
    function readURL(input) {

        var image_input_id = $(input).attr('id')

        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $("#" + image_input_id).parent().find('.profile-delete-icon-container').css('display', 'inherit')
                $("#" + image_input_id).parent().find('.delete-hidden-input').attr('checked', false)
                $("#" + image_input_id).parent().find('.profile-photo-image').css('background-image', 'url("' + e.target.result + '")');
            }
            $(image_input_id).siblings('.profile-delete-icon-container').css("display", "block");
            reader.readAsDataURL(input.files[0]);
        }
    }

    $(".profile-photo-input").change(function() {
        readURL(this);
    });
    
    // Function to remove file input image from display and empty input
    function delete_profile_photo(event, field_id) {
      if ($(event.target).attr("class") == "far fa-trash-alt") {
        $("#" + field_id).find('.profile-photo-image').css('background','none');
        $("#" + field_id).find('.profile-photo-image').css('background-size','cover');
        $("#" + field_id).find('.profile-photo-input').val('');
        $("#" + field_id).find('.delete-hidden-input').attr('checked', true);
        $(event.target).parent().css("display","none");
      }
    }
    
    $(function() {
        
        // Ensure correct date format
            var dateAndTimeAr = $('.standard-form input[name=birth_date]').val().split(' ');
            var dateAr = dateAndTimeAr[0].split('-')
        if(typeof dateAr[2] !== "undefined" && typeof dateAr[1] !== "undefined" && typeof dateAr[0] !== "undefined") {
            var newDate = dateAr[2] + "/" + dateAr[1] + "/" + dateAr[0];
            $('.standard-form input[name=birth_date]').val(newDate);
        }
        
    
        // Initiliase date picker, limiting user to DoB over 18 years ago 
        var min_date = new Date();
        min_date.setFullYear(min_date.getFullYear() - 18);
        
        $("#id_birth_date").datepicker({
            format: 'dd/mm/yyyy',
            'endDate': min_date,
        });
    
    });
    
}

// Member profile page
// ********

// Carousel for profile pictures
if ($('#page-ref').data('page-ref') == "member_profile") {
    $(window).bind("load", function() {
       var draggable_profile_width = $('.profile-img-draggable')[0].scrollWidth
       var window_width = parseInt($( window ).width(), 10)
        
       $('.profile-img-draggable').draggable({
           axis: "x",
           containment: [ window_width - draggable_profile_width, window_width - draggable_profile_width, 0, 0 ]
       });
       
       $( window ).resize(function() {
           var draggable_profile_width = $('.profile-img-draggable')[0].scrollWidth
           var window_width = parseInt($( window ).width(), 10);
           $( ".profile-img-draggable" ).css('left', '0px');
           $( ".profile-img-draggable" ).draggable( "option", "containment", [ window_width - draggable_profile_width, window_width - draggable_profile_width, 0, 0 ] )
       })  
    })
        
}

// Search page
// *******
if ($('#page-ref').data('page-ref') == "search") {
    // Function to reset search options
    function remove_selected() {
        var custom_fields = {
            sexuality: "Sexuality ▾",
            height_max: "Max Height ▾",
            height_min: "Min Height ▾",
            distance: "Distance ▾"
        }
        
        $('.custom-form-field').each(function() {
            $(this).val('')
            let field_id = $(this).attr('id')
            $(this).siblings('.dropdown-toggle').find('.filter-option-inner-inner').text(custom_fields[field_id])
        });
        $('.search-form select').selectpicker('deselectAll');
        $('.dropdown-toggle').removeClass('selected-search-option');
    }
    
    
    // Ensure value of selected inputs remain on page load
    var sexuality = $('#sexuality').data('sexuality')
    if (sexuality) {
        var sexuality_arr = JSON.parse(sexuality.replace(/\'/g, "\""));
        $('#sexuality').val(sexuality_arr)
    }
    var min_height = $('#height_min').data('min-height');
    var max_height = $('#height_max').data('max-height');
    var distance = $('#distance').data('distance');
    $('#height_max').val(max_height);
    $('#height_min').val(min_height);
    $('#distance').val(distance);
    
    // Set titles of selected options to inputted values
    var min_height_option = $('select[name="height_min"] option[value="' + min_height + '"]').text();
    if(min_height_option) {
        $('.dropdown-toggle[data-id="height_min"] .filter-option-inner-inner').text(min_height_option);
    }
    var max_height_option = $('select[name="height_max"] option[value="' + max_height + '"]').text();
    if(max_height_option) {
        $('.dropdown-toggle[data-id="height_max"] .filter-option-inner-inner').text(max_height_option);
    }
    var distance_option = $('select[name="distance"] option[value="' + distance + '"]').text();
    if(distance_option) {
        distance_option
        $('.dropdown-toggle[data-id="distance"] .filter-option-inner-inner').text(distance_option);
    }
   
    // Set title of sexuality to inputted values
    if(sexuality_arr){
        var sexuality_title = ""
        for(i=0; i < sexuality_arr.length; i++) {
            var sexuality_option = $('select[name="sexuality"] option[value="' + sexuality_arr[i] + '"]').text() 
            if(i == 0 || sexuality_arr.length == 0) {
                sexuality_title += sexuality_option
            } else {
                sexuality_title += ", "
                sexuality_title += sexuality_option
            }
        }
        $('.dropdown-toggle[data-id="sexuality"] .filter-option-inner-inner').text(sexuality_title);
    }
    
    // On select search options, change option's appearance
    $('.search-form select').on('change', function() {
        if ($(this).val() == null) {
            $(this).siblings('.dropdown-toggle').removeClass('selected-search-option')
        }
        else {
            $(this).siblings('.dropdown-toggle').addClass('selected-search-option')
        }
    });
    
    // Initiliase selectpicker options
    $('.search-form select').attr('data-container', 'body');
    $('.search-form select').selectpicker();
    $('.search-form select').attr('title', '');
    
    // On load check if any options are selected and update styling
    // Has to be after selectpicker
    $('.search-form select').each(function() {
        if ($(this).val() != null && $(this).val() != "") {
            $(this).siblings('.dropdown-toggle').addClass('selected-search-option')
        }
    });
    
}

// Subscribe page
// *******

// Adjust style and total text when a plan is selected
if ($('#page-ref').data('page-ref') == "subscribe") {
        $('.subscription-button').on('click', function() {
        $('select[name="plans"]').val($(this).data('plan'));
        $('.subscription-button').addClass('inactive-subscription-option');
        $('.subscription-modal h3').addClass('inactive-subscription-option');
        $('.subscription-modal hr').addClass('inactive-subscription-option');
        $(this).removeClass('inactive-subscription-option');
        $(this).siblings('h3').removeClass('inactive-subscription-option');
        $(this).siblings('hr').removeClass('inactive-subscription-option');
        $('.plan-total').text($(this).siblings('h3').text());
        $('.cost-total').text($(this).data('price'));
    })
}