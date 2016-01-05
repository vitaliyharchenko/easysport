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


function href() {
    var sporttype = $('#sporttype').val();
    var query = $("#searchquery").val();
    if (sporttype == '0') {
        if (query) {
            location.href = '{% url "courts_view" %}' + '?q=' + query;
        } else {
            location.href = '{% url "courts_view" %}';
        }
    }
    else {
        if (query) {
            location.href = '{% url "courts_view" %}' + '?s=' + sporttype + '&q=' + query;
        } else {
            location.href = '{% url "courts_view" %}' + '?s=' + sporttype;
        }
    }
};



$(document).on('click', '#searchbutton', function () {
    href();
});

$(document).on('click', '#resetbutton', function () {
    $("#searchquery").val('');
    href();
});

$(document).on('change','#sporttype',function(){
    href();
});


var courts = JSON.parse("{{map_data|escapejs}}");

ymaps.ready(function () {

    var map = new ymaps.Map("CourtMap", {
        center: [56.834331,60.607307],
        zoom: 11,
        controls: ['zoomControl', 'fullscreenControl']
    });

    for (i = 0; i < courts.length; i++) {
        var court = courts[i]
        var point = [court[3], court[4]];
        var string = '<a href="/court/' + court[0] + '" target="_blank">' + court[1] + '<' + '/a>';
        var myPlacemark = new ymaps.Placemark(point, {
            balloonContentHeader: string,
            balloonContentBody: court[2],
            balloonContentFooter: court[5]
        });
        map.geoObjects.add(myPlacemark);
    }

});