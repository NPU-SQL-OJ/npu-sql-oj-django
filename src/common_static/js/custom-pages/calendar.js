!(function (i) {
    "use strict";
    function e() {}
    (e.prototype.init = function () {
        var e, t, a, n;
        i.isFunction(i.fn.fullCalendar)
            ?
             (i("#external-events .fc-event").each(function () {
                  var e = { title: i.trim(i(this).text()) };
                  i(this).data("eventObject", e),
                      i(this).draggable({
                          zIndex: 999,
                          revert: !0,
                          revertDuration: 0,
                      });
              }),
              (t = (e = new Date()).getDate()),
              (a = e.getMonth()),
              (n = e.getFullYear()),
              i("#calendar").fullCalendar({
                  header: {
                      left: "prev,next today",
                      center: "title",
                      right: "month,basicWeek,basicDay",
                  },
                  editable: !0,
                  eventLimit: !0,
                  droppable: !0,
                  drop: function (e, t) {
                      var a = i(this).data("eventObject"),
                          n = i.extend({}, a);
                      (n.start = e),
                          (n.allDay = t),
                          i("#calendar").fullCalendar("renderEvent", n, !0),
                          i("#drop-remove").is(":checked") && i(this).remove();
                  },
                  events: [
                      { title: "复习", start: new Date(n, a, 1) },
                      {
                          title: "复习",
                          start: new Date(n, a, t - 5),
                          end: new Date(n, a, t - 2),
                      },
                      {
                          id: 999,
                          title: "第三章1测试",
                          start: new Date(n, a, t - 3, 16, 0),
                          end: new Date(n, a, t - 3, 18, 0),
                          allDay: !1,
                          url: "exams-manage.html"
                      },
                      {
                          title: "第四章测试",
                          start: new Date(n, a, t, 12, 0),
                          end: new Date(n, a, t, 14, 0),
                          allDay: !1,
                      },
                      {
                          title: "第五章测试",
                          start: new Date(n, a, t + 1, 19, 0),
                          end: new Date(n, a, t + 1, 22, 30),
                          allDay: !1,
                      },
                      {
                          title: "期中考试",
                          start: new Date(n, a, 28),
                          end: new Date(n, a, 29),
                          url: "exams-manage.html",
                      },
                  ],
              }),
              i("#add_event_form").on("submit", function (e) {
                  e.preventDefault();
                  var t,
                      a,
                      n = i(this).find(".new-event-form"),
                      r = n.val();
                  3 <= r.length
                      ? ((t = "new" + Math.random().toString(36).substring(7)),
                        i("#external-events").append(
                            '<div id="' +
                                t +
                                '" class="fc-event">' +
                                r +
                                "</div>"
                        ),
                        (a = { title: i.trim(i("#" + t).text()) }),
                        i("#" + t).data("eventObject", a),
                        i("#" + t).draggable({
                            revert: !0,
                            revertDuration: 0,
                            zIndex: 999,
                        }),
                        n.val("").focus())
                      : n.focus();
              }))
            : 
            alert("Calendar plugin is not installed");
    }),
        (i.CalendarPage = new e()),
        (i.CalendarPage.Constructor = e);
})(window.jQuery),
    (function () {
        "use strict";
        window.jQuery.CalendarPage.init();
    })();
