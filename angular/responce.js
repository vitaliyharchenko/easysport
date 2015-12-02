var error_response = function(data){
  $('.api-response').html("API Response: " + data.status + ' ' + data.statusText + '<br/>Content: ' + data.responseText);
};

var susccess_response = function(data){
  $('.api-response').html("API Response: OK<br/>Content: " + JSON.stringify(data));
};

$(document).on('click','#btn', function(){
    var email = $('#email').val();
    var password = $('#password').val();
    $.ajax({
        url: "http://127.0.0.1:8000/token/?format=json",
        data: {
            password: password,
            email: email
        },
        async: true,
        success: function (data, textStatus) {
            $('.api-response').html("API Response: OK<br/>Content: " + JSON.stringify(data));
        },
        error: function (response, status, errorThrown) {
            $('.api-response').html("API Response: " + status + response);
        },
        type: "POST",
        dataType: "json"
    });
});