/**
 * Created by vitaliyharchenko on 13.01.16.
 */
// DOM element where the Timeline will be attached
var container = document.getElementById('mytimeline');
// Create a DataSet with data (enables two way data binding)
var data = new vis.DataSet([
    {
        id: 'A',
        content: 'Гимназия №9, Екатеринбург',
        start: '2000-09-01',
        end: '2010-05-29'
    },
    {
        id: 'B',
        content: 'Физический факультет, кафедра физики твердого тела, СпбГУ, г. Санкт-Петербург',
        start: '2010-09-01',
        end: '2013-05-29'
    },
    {
        id: 'С',
        content: 'Физический факультет, кафедра компьютерной физики УрФУ, г. Екатеринбург',
        start: '2013-09-01',
        end: '2014-06-28'
    },
    {
        id: 0,
        content: 'Родился',
        start: '1992-12-21',
        'className': 'orange'
    },
    {
        id: 1,
        content: 'Репетитор по физике',
        start: '2010-10-01',
        end: '2011-09-01',
        'className': 'orange'
    },
    {
        id: 2,
        content: 'Onlife - вечеринки знакомств, основатель и руководитель, г. Санкт-Петербург',
        start: '2011-09-01',
        end: '2013-05-30',
        'className': 'orange'
    },
    {
        id: 3,
        content: 'Инструктор по виндсерфингу, г. Екатеринбург',
        start: '2013-06-01',
        end: '2013-09-30'
    },
    {
        id: 4,
        content: 'Бар «Золотой Каньон», организатор мероприятий, г. Екатеринбург',
        start: '2013-10-01',
        end: '2014-05-30',
        'className': 'orange'
    },
    {
        id: 5,
        content: 'ООО «Фабрика праздника», направление тимбилдингов, г. Екатеринбург',
        start: '2014-06-01',
        end: '2015-09-01',
        'className': 'orange'
    },
    {
        id: 6,
        content: 'SportCourts.ru, CEO',
        start: '2014-08-02',
        end: (new Date()).getTime(),
        'className': 'orange'
    },
    {
        id: 7,
        content: 'Бакалавр физики',
        start: '2014-06-28',
        'className': 'green'
    },
    {
        id: 8,
        content: 'EasyMoto, прокат питбайков',
        start: '2015-12-01',
        end: (new Date()).getTime(),
        'className': 'orange'
    },
    {
        id: 9,
        content: 'ОЦ Юниум, преподаватель физики',
        start: '2014-09-01',
        end: (new Date()).getTime(),
        'className': 'orange'
    }
]);
// Configuration for the Timeline
var options = {
    height: '260px',
    min: new Date(1990, 0, 1),                // lower limit of visible range
    max: new Date((new Date()).getTime() + 1000 * 60 * 60 * 24 * 31 * 12 * 2),                // upper limit of visible range
    zoomMin: 1000 * 60 * 60 * 24 * 31 * 11,             // one day in milliseconds
    zoomMax: 1000 * 60 * 60 * 24 * 31 * 12 * 5     // about twentee years in milliseconds
};
// Create a Timeline
var timeline = new vis.Timeline(container, data, options);

var endtime = (new Date()).getTime() + 1000*60*60*24*31*2;
timeline.setWindow('2014-10-08', endtime);


document.getElementById('fit').onclick = function () {
    timeline.setWindow('2011-10-08', endtime);
};