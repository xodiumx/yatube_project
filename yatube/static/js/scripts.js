function csrf() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name +'=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length +1));
                    break;
                }
            }
        }
        return cookieValue;    
    }
    
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host;
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))){
                xhr.setRequestHeader('X-CSRFToken',
                    $('input[name="csrfmiddlewaretoken"]').val());
                
            }
        }
    });
}


function addRemovePostLike() {
    $('form.add-remove-post-like').each((index, el) => {
        $(el).on('submit', (e) => {
            e.preventDefault();

            const post_id = $(el).find('input[name="post_id"]').val();
            const user_id= $(el).find('input[name="user_id"]').val();
            const post_likes_id = $(el).find('input[name="post_likes_id"]').val();

            if ( $(e.currentTarget).hasClass('add-post-like') ) {
                $.ajax({
                    url: "/likes/add/",
                    type: "POST",
                    dataType: "json",
                    data: {
                        post_id: post_id,
                        user_id: user_id,
                    },
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                      },
                    success: (data) => {
                        console.log(data);

                        if (data['added']) {
                            $(el).removeClass('add-post-like').addClass('remove-post-like');
                            $(el).attr('action', '/likes/remove/');
                        }
                }
            });
        }

            if ( $(e.currentTarget).hasClass('remove-post-like') ) {
                $.ajax({
                    url: "/likes/remove/",
                    type: "POST",
                    dataType: "json",
                    data: {
                        post_id: post_id,
                        user_id: user_id,
                        post_likes_id: post_likes_id,
                    },
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                      },
                    success: (data) => {
                        console.log(data);
                        if (data['removed']) {
                            $(el).removeClass('remove-post-like').addClass('add-post-like');
                            $(el).attr('action', '/likes/add/');
                        }
                    }
                });
            }
        });
    });
}


$(document).ready(() => {
    csrf();
    
    addRemovePostLike();
});