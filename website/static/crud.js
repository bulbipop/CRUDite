$(document).ready(function () {
    $('.delete').click(function (ev) {
        ev.preventDefault();
        if (confirm(ev.target.href)) {
            $.ajax({
                type: 'DELETE',
                dataType: 'json',
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: ev.target.href,
                success: function (data) {
                    if (data['success']) {
                        $(ev.target).closest('tr').remove();
                    } else {
                        alert(data['error']);
                    }
                },
                error: function (data) {
                    alert(data)
                }
            });
        }
    });
});
