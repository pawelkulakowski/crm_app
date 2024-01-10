$(function () {

  $(".js-create-country").click(function () {
    $.ajax({
      url: '/country_create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-country").modal("show");
      },
      success: function (data) {
        $("#modal-country .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-country").on("submit", ".js-country-create-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_countries_list);  // <-- Replace the table body
          $("#modal-country").modal("hide");  // <-- Close the modal
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });

});