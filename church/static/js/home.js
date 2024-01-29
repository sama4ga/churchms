
$(function () {
  'use strict'
  
    // bootstrap WYSIHTML5 - text editor
  // $('.textarea').summernote()

  // $('.daterange').daterangepicker({
  //   ranges: {
  //     Today: [moment(), moment()],
  //     Yesterday: [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
  //     'Last 7 Days': [moment().subtract(6, 'days'), moment()],
  //     'Last 30 Days': [moment().subtract(29, 'days'), moment()],
  //     'This Month': [moment().startOf('month'), moment().endOf('month')],
  //     'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
  //     'This Year': [moment().startOf('year'), moment().endOf('year')],
  //     'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')],
  //   },
  //   startDate: moment().subtract(29, 'days'),
  //   endDate: moment()
  // }, function (start, end) {
  //   // eslint-disable-next-line no-alert
  //   // alert('You chose: ' + start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))
  // });
  
   
    /* initialize the calendar
     -----------------------------------------------------------------*/
    //Date for the calendar events (dummy data)
    var date = new Date()
    var d    = date.getDate(),
        m    = date.getMonth(),
        y    = date.getFullYear()

    var Calendar = FullCalendar.Calendar;
    var Draggable = FullCalendar.Draggable;

    // var containerEl = document.getElementById('external-events');
    // var checkbox = document.getElementById('drop-remove');
    var calendarEl = document.getElementById('calendar');

    // initialize the external events
    // -----------------------------------------------------------------

    // new Draggable(containerEl, {
    //   itemSelector: '.external-event',
    //   eventData: function(eventEl) {
    //     return {
    //       title: eventEl.innerText,
    //       backgroundColor: window.getComputedStyle( eventEl ,null).getPropertyValue('background-color'),
    //       borderColor: window.getComputedStyle( eventEl ,null).getPropertyValue('background-color'),
    //       textColor: window.getComputedStyle( eventEl ,null).getPropertyValue('color'),
    //     };
    //   }
    // });

    var calendar = new Calendar(calendarEl, {
      headerToolbar: {
        left  : 'prev,next today',
        center: 'title',
        right : 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
      },
      themeSystem: 'bootstrap',
      //Random default events
      events: {
        url: baseurl + '/calendar/get_event/',
      },
      timeZone: 'Africa/Lagos', // Africa/Lagos, UTC
      // selectable: true,
      // editable  : true,
      droppable : true,
      drop      : function(info) {
        if (checkbox.checked) {
          info.draggedEl.parentNode.removeChild(info.draggedEl);
        }
      },
      dateClick: function (info) {
        // console.log(info);
        $("#eventTitle").html('Create Event');
        $("#save").attr('data-type', 'create');
        let date = new Date(info.date).toISOString();
        $("#start").val(date.substring(0, date.length-1));
        $("#end").val(date.substring(0, date.length-1));
        $("#event").modal('show');
        $("#delete").addClass('d-none');
      },
      eventClick: function (info) {
        // console.log(info);
        info.jsEvent.preventDefault();
        $("#title").val(info.event.title);
        $("#description").val(info.event.extendedProps.description);
        $("#all_day").prop("checked", info.event.allDay);
        let start = info.event.startStr
        let end = info.event.endStr
        if (info.event.allDay) {
          start = info.event.startStr + "T00:00"
          end = info.event.endStr + "T23:59"
          $("#start").val(start);
          $("#end").val(end);
          $("#end").prop('disabled', true);
        }else{
          $("#end").prop('disabled', false);
          $("#start").val(start.substring(0, start.length-1));
          $("#end").val(end.substring(0, end.length-1));
        }
        $("#eventTitle").html('Edit Event');     
        $("#id").val(info.event.id);
        $("#save").attr('data-type', 'edit');
        $("#event").modal('show');
        $("#delete").removeClass('d-none');
      },
      select: function (info) {
        // console.log(info);
      }
    });

    calendar.render();

    // $(".datetime").datetimepicker({
    //   format: "YYYY-MM-DD hh:mm A"
    // });

});

function formatDate(dateStr) {
  date = new Date(dateStr);
  date =  [
    date.getFullYear(),
    (date.getMonth() + 1).toString().padStart(2, "0"),
    date.getDate().toString().padStart(2, "0"),
  ].join("-");
  return date;
}

function formatDateTime(dateTimeStr) {
  let date = formatDate(dateTimeStr);
  let time = new Date(dateTimeStr);
  time =  [
    time.getHours().toString().padStart(2, "0"),
    time.getMinutes().toString().padStart(2, "0"),
  ].join(":");
  return date + " " + time;
}

  