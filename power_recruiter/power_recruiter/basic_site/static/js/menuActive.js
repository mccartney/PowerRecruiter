$(function() {
    if (window.location.pathname.substring(1).indexOf("Chart") != -1) {
        $(".statsli").addClass('active');
    }
    else if (window.location.pathname.substring(1).indexOf("notifications") != -1) {
        $(".notifili").addClass('active');
    }
    else if (window.location.pathname.substring(1).indexOf("configuration") != -1) {
        $(".configli").addClass('active');
    }
    else {
        $(".homeli").addClass('active');
    }
});