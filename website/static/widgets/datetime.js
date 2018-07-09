$(function () {
    $('.datetimepicker').each(function() {
      $(this).datetimepicker({
        date: moment($(this).val(), "YYYY-MM-DD HH:MM"),
        locale: 'fr',
        format: 'L'
      });
    });
});
