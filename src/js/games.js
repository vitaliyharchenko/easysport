$(document).on('click', '.action', function (e) {
    var arr = $(this).attr("id").split('-');
    var game_id = arr[0], action = arr[1];

    $(this).parent().parent().parent().find('.btn').attr('disabled', true);

    $('#' + game_id + '-pane').attr('style', 'opacity: 0.7;');

    $.ajax({
        url: '{% url "gameaction" %}',
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            game_id: game_id,
            action: action
        },
        async: true,
        success: function (responseData, textStatus) {
            if (responseData['error']) {
                alert(responseData['error']['error_description']);
            } else {
                $('#' + game_id + '-pane').fadeOut('slow', function () {
                    $('#' + game_id + '-pane').replaceWith(responseData);
                });
            }
        },
        error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
        },
        type: "POST",
        dataType: "text"
    });
    e.preventDefault();
});

$(document).on('change','#sporttype',function(){
    var value = $('#sporttype').val();
    if (value == '0') {
        location.href='/games';
    }
    else {
        location.href='/games?q='+value;
    }
});