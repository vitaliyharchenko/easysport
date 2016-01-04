/**
 * Created by vitaliyharchenko on 04.01.16.
 */
/**
 * Created by vitaliyharchenko on 04.01.16.
 */
ymaps.ready(function () {
    var point = [parseFloat('{{ game.court.place.latitude }}'.replace(",", ".")),
                 parseFloat('{{ game.court.place.longitude }}'.replace(",", "."))];

    var map = new ymaps.Map("CourtMap", {
        center: point,
        zoom: 16,
        controls: ['zoomControl', 'fullscreenControl']
    });

    var myPlacemark = new ymaps.Placemark(point, {
        balloonContentHeader: '{{ game.court.title }}',
        balloonContentBody: '{{ game.court.place.fulladdress }}'
    });

    map.geoObjects.add(myPlacemark);
    myPlacemark.balloon.open();
});