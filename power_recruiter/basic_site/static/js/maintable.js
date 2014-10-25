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
            console.log(currentlyOpenedId);
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
            console.log($("#maintable tr td[text='1']").text());
            $("#maintable tr:first-child:contains(currentlyOpenedId)").addClass('maintable-row-large');
        }
    });
});