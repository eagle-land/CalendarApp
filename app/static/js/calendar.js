$(document).ready(function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: [ 'timeGrid' ],
        // Defaults to weekly view with times
        defaultView: 'timeGridWeek',
        // Buttons at the top of calendar
        header: {
            left: 'timeGridWeek,timeGridDay',
            center: 'title',
            right: 'today prev,next'
        }
    });

    calendar.render();
});
