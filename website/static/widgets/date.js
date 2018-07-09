$(function () {
    $('.datepicker').each(function() {
      if ($(this).val() != undefined) {
        val = moment($(this).val(), "YYYY-MM-DD");
      } else {
        val = null;
      }
      if ($(this).attr('min') != undefined) {
        min = moment($(this).attr('min'), "YYYY-MM-DD");
      } else {
        min = false;
      }
      if ($(this).attr('max') != undefined) {
        max = moment($(this).attr('max'), "YYYY-MM-DD");
      } else {
        max = false;
      }
      if ($(this).attr('locale') != undefined) {
        loc = moment($(this).attr('locale'), "YYYY-MM-DD");
      } else {
        loc = 'fr';
      }

      $(this).datetimepicker({
        date: val,
        minDate: min,
        maxDate: max,
        locale: loc,
        format: 'L'
      });
    });
});
