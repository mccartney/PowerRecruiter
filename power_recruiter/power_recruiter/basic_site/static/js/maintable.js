/**
 * Created by shadowsword on 25.10.14.
 */
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
            if(currentlyOpened.find('td').first().hasClass('td-with-bottom-bar-upsidedown')){
                currentlyOpened.find('td').removeClass('td-with-bottom-bar-upsidedown');
                currentlyOpened.find('td').addClass('td-with-bottom-bar');
            }
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
        addBottomBarToTd();
    })
    .on('load-success.bs.table',function (e, name, order) {
        addBottomBarToTd();
     });
});

function addBottomBarToTd(){
    //Add bottom bar to tr
    $("#maintable tr").each(function() {
        haveBottomBar = false;
        currentTr = $(this);
        $(this).find('td div.innertd').each (function() {
            oldHeight = $(this).css('height');
            $(this).addClass('large-inner-div');
            autoHeight = $(this).parent().height();
            $(this).removeClass('large-inner-div');
            if($(this).parent().height() < autoHeight){
                currentTr.find('td').addClass('td-with-bottom-bar');
            }
        });
        $(this).find('.personid').first().val(currentTr.children().first().text());
        if(currentlyOpened != null) {
            currentlyOpened = $('#maintable tr:has(td:textEquals("' + currentlyOpenedId + '"))');
            openLargeTd(currentlyOpened);
        }
    });
    Dropzone.discover();
}

function openLargeTd(element){
    element.addClass('maintable-row-large');
    if(element.find('td').first().hasClass('td-with-bottom-bar')){
        element.find('td').removeClass('td-with-bottom-bar');
        element.find('td').addClass('td-with-bottom-bar-upsidedown');
    }
}

function reloadData() {
    $('#maintable').bootstrapTable('refresh', "{silent: true}");
}