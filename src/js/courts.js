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


var courts = '{{map_data}}';
courts = courts.replace(/&quot;/g,"\"");
courts = jQuery.parseJSON(courts);
console.log(courts);

ymaps.ready(function () {

    var map = new ymaps.Map("CourtMap", {
        center: [56.834331,60.607307],
        zoom: 11,
        controls: ['zoomControl', 'fullscreenControl']
    });

    for (i = 0; i < courts.length; i++) {
        var court = courts[i]
        var point = [court[3], court[4]];
        var myPlacemark = new ymaps.Placemark(point, {
            balloonContentHeader: court[1],
            balloonContentBody: court[2],
            balloonContentFooter: court[5]
        });
        map.geoObjects.add(myPlacemark);
    }

});