function reloadTable(){
    //Add bottom bar to tr
    if(setAutosize()) {
        $("#maintable tr").each(function () {
            haveBottomBar = false;
            currentTr = $(this);
            $(this).find('td div.innertd').each(function () {
                $(this).addClass('large-inner-div');
                autoHeight = $(this).parent().height();
                $(this).removeClass('large-inner-div');
                if ($(this).parent().height() < autoHeight) {
                    currentTr.find('td').addClass('td-with-bottom-bar');
                }
            });
            $(this).find('.personid').first().val(currentTr.children().first().text());
            $(this).find('.caveatsArea').first().attr('id', "caveats-" + (currentTr.children().first().text()));
            if (currentlyOpened != null) {
                currentlyOpened = $('#maintable tr:has(td:textEquals("' + currentlyOpenedId + '"))');
                openLargeTd(currentlyOpened);
            }
        });
    }

    setTableEvents();
    Dropzone.discover();
}

function setTableEvents(){
    $("a").click(function(e){
        e.stopPropagation();
    });

    $("button").click(function(e){
        e.stopPropagation();
    });

    $(".blockTableEvent").click(function(e) {
        e.stopPropagation();
    });

    $("input").click(function(e){
       e.stopPropagation();
    });
}

function reloadData(url) {
    if (url !== undefined) {
        $('#maintable').bootstrapTable('refresh', JSON.parse('{"url": "' + url + '"}'));
    }
    else
        $('#maintable').bootstrapTable('refresh', "{silent: true}");
    reloadTable();
}

function setAutosize(){
    $(document).ready(function(){
        $('textarea').autosize();
    });
    $('textarea').bind('input propertychange', function() {
        id = $(this).attr('id').substr('caveats-'.length, $(this).attr('id').lenght);
        content = $(this).val();
        $.post( "/candidate/caveats/upload/", { id: id, caveats: content });
    });
    $('textarea').click(function(){
        if($(this).parents('.maintable-row-large').length)
        {
            return false;
        }
    })
    return true;
}