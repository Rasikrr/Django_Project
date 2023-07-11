$(document).ready(function() {
    // Получение CSRF-токена из cookie
    var csrftoken = Cookies.get('csrftoken');

    // Установка CSRF-токена в заголовки запроса
    function csrfSafeMethod(method) {
        // Эти методы запроса не требуют CSRF-токена
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $('.like-button').click(function(e) {
        e.preventDefault();
        var post_id = $(this).data('post-id');

        $.ajax({
            type: 'POST',
            url: '/like-post/',
            data: JSON.stringify({'post_id': post_id}),
            contentType: 'application/json',
            success: function(data) {
                $('#like-count-' + post_id).text(data.likes_count);
            },
            error: function(xhr, status, error) {
                // Обработка ошибок, если необходимо
            }
        });
    });
});
