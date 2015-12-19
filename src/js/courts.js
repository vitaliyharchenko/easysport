$(document).ready(function() {
    queryfunc();
});

function queryfunc() {
    var len = $("#searchquery").val().length;
    if (len > 2) {
        $("#searchbutton").attr('disabled', false);
    } else {
        $("#searchbutton").attr('disabled', true);
    }
};

$(document).on('input', '#searchquery', function () {
    queryfunc();
});

$(document).on('click', '#searchbutton', function () {
    var url = "{% url 'courts_view' %}?q=".concat($("#searchquery").val())
    window.location.replace(url);
});