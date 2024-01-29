$(document).ready(function () {
  const buttons = [
    {
      extend: "copy",
      text: '<i class="fa fa-copy"></i>',
      titleAttr: "Copy",
      className: "btn-copy",
      title: $(".datatable").data("exportTitle"),
      exportOptions: {
        columns: ["thead th:not(.no-export)"],
      },
    },
    {
      extend: "excel",
      text: '<i class="fa fa-file-excel"></i>',
      titleAttr: "Excel",
      className: "btn-excel",
      title: $(".datatable").data("exportTitle"),
      exportOptions: {
        columns: ["thead th:not(.no-export)"],
      },
    },
    {
      extend: "csv",
      text: '<i class="fa fa-file-text"></i>',
      titleAttr: "CSV",
      className: "btn-csv",
      title: $(".datatable").data("exportTitle"),
      exportOptions: {
        columns: ["thead th:not(.no-export)"],
      },
    },
    {
      extend: "pdf",
      text: '<i class="fa fa-file-pdf"></i>',
      titleAttr: "PDF",
      className: "btn-pdf",
      title: $(".datatable").data("exportTitle"),
      exportOptions: {
        columns: ["thead th:not(.no-export)"],
      },
    },
    {
      extend: "print",
      text: '<i class="fa fa-print"></i>',
      titleAttr: "Print",
      className: "btn-print",
      title: $(".datatable").data("exporttitle"),
      // customize: function (win) {
      //   $(win.document.body)
      //     .find("th")
      //     .addClass("display")
      //     .css("text-align", "left");
      //   $(win.document.body)
      //     .find("table")
      //     .addClass("display")
      //     .css("font-size", "14px");
      //   $(win.document.body)
      //     .find("td")
      //     .addClass("display")
      //     .css("text-align", "left");
      // },
      exportOptions: {
        columns: ["thead th:not(.no-export)"],
      },
    },
    {
      extend: "colvis",
      text: '<i class="fa fa-columns"></i>',
      titleAttr: "Columns",
      className: "btn-colvis",
    },
  ];

  $.extend($.fn.dataTable.defaults, {
    scrollCollapse: true,
    scrollX: true,
    scrollY: "75vh",
    dom: '<"top"B><"clearfix"><lf><rt><ip>',
    lengthMenu: [
      [10, 25, 50, 100, -1],
      [10, 25, 50, 100, "All"],
    ],
    pageLength: 100,
    buttons: buttons,
    language: {
      searchPlaceholder: " Search...",
      search: "",
      order: [],
      lengthMenu: "Showing _MENU_ Records",
      processing:
        '<i class="fa fa-spinner fa-spin fa-1x fa-fw"></i><span class="sr-only">Loading...</span> ',
      emptyTable:
        "<div align='center' class='text-danger'>No data available in table<br /><br /><img src='/../media/addnewitem.svg' width='150'/><br /><br /><span class='text-success bolds'><i class='fa fa-arrow-left'></i> Add new record or search with different criteria</span><div></div></div>",
      zeroRecords:
        "<div align='center' class='text-danger'>No matching record found<br /><br /><img src='/../media/addnewitem.svg' width='150'/><br /><br /><span class='text-success bolds'><i class='fa fa-arrow-left'></i> Search with different criteria</span><div></div></div>",
      //info: LANG.table_info,
      //infoEmpty: LANG.table_infoEmpty,
      //loadingRecords: LANG.table_loadingRecords,
      paginate: {
        first: "<<",
        last: ">>",
        next: ">",
        previous: "<",
      },
    },
  });

  toastr.options = {
    closeButton: true, // true/false
    debug: false, // true/false
    newestOnTop: false, // true/false
    progressBar: false, // true/false
    positionClass: "toast-top-right", // toast-top-right / toast-top-left /
    preventDuplicates: false,
    onclick: null,
    showDuration: "300", // in milliseconds
    hideDuration: "1000", // in  milliseconds
    timeOut: "5000", // in milliseconds
    extendedTimeOut: "1000", // in milliseconds
    showEasing: "swing",
    hideEasing: "linear",
    showMethod: "fadeIn",
    hideMethod: "fadeOut",
  };

  /* add active class and stay opened when selected */
  const current_url = window.location; //.pathname;

  // for sidebar menu entirely but not cover treeview
  $("ul.nav-sidebar a")
    .filter(function () {
      if (this.href) {
        return this.href == current_url; //|| current_url.href.indexOf(this.href) == 0;
      }
    })
    .addClass("active");

  // for the treeview
  $("ul.nav-treeview a")
  .filter(function () {
    if (this.href) {
      return this.href == current_url; //|| current_url.href.indexOf(this.href) == 0;
    }
  })
  .parentsUntil(".nav-sidebar > .nav-treeview")
  .addClass("menu-open")
  .prev("a")
  .addClass("active");

  $(".filter").on("click", function () {
    $("#filter").toggle();
  });
    
});

function successMsg(msg) {
  toastr.success(msg);
}

function errorMsg(msg) {
  toastr.error(msg);
}

function infoMsg(msg) {
  toastr.info(msg);
}

function warningMsg(msg) {
  toastr.warning(msg);
}

//This method removes unwanted get parameter from the data.
function __datatable_ajax_callback(data) {
  for (var i = 0, len = data.columns.length; i < len; i++) {
    if (!data.columns[i].search.value) delete data.columns[i].search;
    if (data.columns[i].searchable === true) delete data.columns[i].searchable;
    if (data.columns[i].orderable === true) delete data.columns[i].orderable;
    if (data.columns[i].data === data.columns[i].name)
      delete data.columns[i].name;
  }
  delete data.search.regex;

  return data;
}

var baseurl = window.location.origin;

function confirmDelete(e) {
  const url = baseurl + $(e).attr("data-url");

  Swal.fire({
    title: "Are you sure? This action is irreversible.",
    text: "This will delete all associated records.",
    icon: "warning",
    showCancelButton: true,
    showCloseButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel!",
    // reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
      $.get(url, {}, (data, status) => {
        if (status == "success" && data == "success") {
          $(e).closest("tr").remove();
          successMsg("Record successfully deleted!");
        } else {
          errorMsg("Error while deleting record");
        }
      }).fail(function(xhr, status, errorThrown){
        if(xhr.status == 403){
          errorMsg('Access denied');
        }
      });
    }
  });

  
}
