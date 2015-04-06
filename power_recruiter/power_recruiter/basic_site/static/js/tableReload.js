function reloadTable(){
    if(setAutosize()) {
        $("#maintable tr").each(function () {
            currentTr = $(this);
            if (currentlyOpened != null) {
                if(currentTr.find('td:nth-child(2)').text() == currentlyOpened.find('td:nth-child(2)').text()){ //nth-child(2) == td of candidate_id
                    openLargeTd($(this));
                    currentlyOpened = $(this);
                }
            }
        });
    }

    blockTableEventPropagation();
    Dropzone.discover();
    $('[data-toggle="popover"]').popover();
}

function blockTableEventPropagation(){
    $(".blockTableEvent").click(function(e) {
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