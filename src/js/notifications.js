$(document).ready(function () {
    var count = "{{ notifications_new|length }}"
    if (count != "0") {
        $('.notifications .alert').each(function () {
            $(this).fadeIn('slow');
        });
        setTimeout(function () {
            $.ajax({
                url: "{% url 'notification_read' %}",
                data: {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                async: true,
                success: function (data, textStatus) {
                    if (data['response'] = 'OK') {
                        $('.notifications .alert').each(function () {
                            $(this).fadeOut('slow');
                        });
                    } else {
                        alert('Ошибка чтения уведомлений');
                    }
                },
                error: function (response, status, errorThrown) {
                    alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
                    console.log(response);
                },
                type: "POST",
                dataType: "json"
            });
        }, 6000);
    }
});

$(document).on('click','.delete-notification', function(){
    var arr = $(this).attr("id").split('-');
    var notification_id = arr[1];
    $.ajax({
        url: "{% url 'notification_delete' %}",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            notification_id: notification_id
        },
        async: true,
        success: function (data, textStatus) {
            var count = $(".notifications-count").html();
            count = count - 1;
            if (count == 0) {
                $(".notifications-menu-item").html('');
                $('#notificationsModal').modal('hide')
            } else {
                $(".notifications-count").html(count);
            }
        },
        error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            console.log(response);
        },
        type: "POST",
        dataType: "json"
    });
});