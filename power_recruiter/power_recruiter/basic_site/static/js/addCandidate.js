function show_if_checked(show_id, checked_id) {
    _show_if_checked = function(show_id, checked_id, fade) {
        if ($(checked_id).prop('checked')) {
            if (fade == true) {
                $(show_id).fadeIn('slow');
            } else {
                $(show_id).show();
            };
        } else {
            $(show_id).hide();
        }
    }
    _show_if_checked(show_id, checked_id);
    $(checked_id).change(function(e) {
        _show_if_checked(show_id, checked_id, true);
    });
}

$(document).ready(function(){
    $("#save-candidate").click(function() {
        var resp = sendAjax(
                '/candidate/add_from_app/',
                {
                    'first_name': $('#input-first-name').val(),
                    'last_name': $('#input-last-name').val(),
                    'linkedin_link': $('#linkedin-link').val(),
                    'goldenline_link': $('#goldenline-link').val(),
                    'email_link': $('#email-link').val()
                },
                function (data) {
                    $("#creation-modal").modal('toggle');
                    reloadData();
                });
    });

    show_if_checked('#linkedin-section', '#linkedin-checkbox');
    show_if_checked('#goldenline-section', '#goldenline-checkbox');
    show_if_checked('#email-section', '#email-checkbox');
});