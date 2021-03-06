$(document).ready(function(){
    EMPTY_FIRST_NAME_ERROR = "First name cannot be empty";
    EMPTY_LAST_NAME_ERROR = "Last name cannot be empty";
    WRONG_LINKEDIN_ERROR = "It's not a valid linkedin url";
    WRONG_GOLDENLINE_ERROR = "It's not a valid goldenline url";
    WRONG_EMAIL_ERROR = "It's not a valid email address";

    function show_if_checked(show_id, checked_id) {
        _show_if_checked = function(show_id, checked_id, fade) {
            if ($(checked_id).prop('checked')) {
                if (fade == true) {
                    $(show_id).fadeIn('slow');
                } else {
                    $(show_id).show();
                }
            } else {
                $(show_id).hide();
            }
        };
        _show_if_checked(show_id, checked_id);
        $(checked_id).change(function(e) {
            _show_if_checked(show_id, checked_id, true);
        });
    }

    $("#save-candidate").click(function() {
        var first_name = $('#input-first-name').val();
        var last_name = $('#input-last-name').val();
        var linkedin = $('#linkedin-link').val();
        var goldenline = $('#goldenline-link').val();
        var email = $('#email-link').val();
        $('#validation-errs').html('');
        $('.highlight').removeClass('highlight');

        if (validate(first_name, last_name, linkedin, goldenline, email)) {
            var resp = sendAjax(
                'candidate/add_from_app/',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'linkedin_link': linkedin,
                    'goldenline_link': goldenline,
                    'email_link': email
                },
                function (data) {
                    $("#creation-modal").modal('toggle');
                    reloadData();
                }
            );
        }
    });

    function show_error(text) {
        var entity = document.createElement("p");    // Create with DOM
        entity.innerHTML = text;
        $('#validation-errs').append(entity);
    }

    function validate(first_name, last_name, linkedin, goldenline, email) {
        var result = true;
        if (!first_name) {
            result = false;
            show_error(EMPTY_FIRST_NAME_ERROR);
            highlight('#input-first-name');
        }
        if (!last_name) {
            result = false;
            show_error(EMPTY_LAST_NAME_ERROR);
            highlight('#input-last-name');
        }
        if (linkedin && !(is_valid_url(linkedin) && includes(linkedin, 'linkedin'))) {
            result = false;
            show_error(WRONG_LINKEDIN_ERROR);
            highlight('#linkedin-link');
        }
        if (goldenline && !(is_valid_url(goldenline) && includes(goldenline, 'goldenline'))) {
            result = false;
            show_error(WRONG_GOLDENLINE_ERROR);
            highlight('#goldenline-link');
        }
        if (email && !is_valid_email(email)) {
            result = false;
            show_error(WRONG_EMAIL_ERROR);
            highlight('#email-link');
        }
        return result;
    }

    function is_valid_url(url) {
        return url.match(/^(ht|f)tps?:\/\/[a-z0-9-\.]+\.[a-z]{2,4}\/?([^\s<>\#%"\,\{\}\\|\\\^\[\]`]+)?$/);
    }

    function is_valid_email(email) {
        var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        return re.test(email);
    }

    function includes(str, substr) {
        return str.indexOf(substr) > -1;
    }

    function highlight(div) {
        $(div).addClass('highlight');
    }

    function cleanup_modal() {
        $('#input-first-name').val('');
        $('#input-last-name').val('');
        $('#linkedin-link').val('');
        $('#goldenline-link').val('');
        $('#email-link').val('');
        $('.highlight').removeClass('highlight');
        $('#validation-errs').html('');

    }

    $('#creation-modal').on('show.bs.modal', cleanup_modal);

    show_if_checked('#linkedin-section', '#linkedin-checkbox');
    show_if_checked('#goldenline-section', '#goldenline-checkbox');
    show_if_checked('#email-section', '#email-checkbox');
});