currentlyOpened = null;
currentlyOpenedId = null;
closedAll = false;

$(function () {
    $('#maintable').bootstrapTable({})
    //Open or close large row view
    .on('click-row.bs.table', function (e, row, $element) {
        if(!$element.hasClass('maintable-row-large')) {
            openLargeTd($element);
            currentlyOpenedId = $element.children().first().text();
        }
        else{
            closedAll = true;
        }

        if(currentlyOpened != null) {
            currentlyOpened.removeClass('maintable-row-large');
        }

        if(closedAll) {
            currentlyOpened = null;
            closedAll = false;
            currentlyOpenedId = null
        }
        else{
            currentlyOpened = $element;
        }
    })

    //Open large view after sorting
    .on('sort.bs.table',function (e, name, order) {
        reloadData();
    })

    .on('load-success.bs.table',function (e, name, order) {
        reloadTable();
     });
});

function openLargeTd(element){
    if(element !== null){
        element.addClass('maintable-row-large');
    }
}
