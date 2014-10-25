/**
 * Created by shadowsword on 25.10.14.
 */

$(function () {
    currentlyOpened = null;
    currentlyOpenedId = null;
    closedAll = false;

    $('#maintable').bootstrapTable({})
    //Open or close large row view
    .on('click-row.bs.table', function (e, row, $element) {
        if(!$element.hasClass('maintable-row-large')) {
            $element.addClass('maintable-row-large');
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
    .on('sort.bs.table',function (e, name, order)  {
        if(currentlyOpened != null) {
            console.log(currentlyOpenedId == 1);
            currentlyOpened = $('#maintable tr:has(td:textEquals("' + currentlyOpenedId + '"))');
            currentlyOpened.addClass('maintable-row-large');
        }
    });
});