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

function triggerIdGeneratorFunction(){
    this.id = 0;
    this.getNextId = function(){
        this.id++;
        return this.id;
    }
    this.getCurrentId = function(){
        return this.id;
    }
}

var triggerIsFired = 0;
var triggerIdGenerator = new triggerIdGeneratorFunction();

function triggerSaveAfterHalfSecond(id, content){
    var myId = triggerIdGenerator.getNextId();
    setTimeout(function(){
        if (myId == triggerIdGenerator.getCurrentId()) {
            sendAjax( "/candidate/caveats/upload/", { id: id, caveats: content, timestamp: new Date().getTime() });
        }
    }, 500);
}

function setAutosize(){
    $(document).ready(function(){
        $('textarea').autosize();
    });
    $('textarea').bind('input propertychange', function() {
        id = $(this).attr('id').substr('caveats-'.length, $(this).attr('id').lenght);
        content = $(this).val();
        triggerSaveAfterHalfSecond(id, content)
    });
    $('textarea').click(function(){
        if($(this).parents('.maintable-row-large').length) {
            return false;
        }
    })
    return true;
}