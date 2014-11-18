<script>
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
            reloadTable();
        })
        .on('load-success.bs.table',function (e, name, order) {
            reloadTable();
         });
    });

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
        Dropzone.discover();
    }

    function openLargeTd(element){
        element.addClass('maintable-row-large');
        if(element.find('td').first().hasClass('td-with-bottom-bar')){
            element.find('td').removeClass('td-with-bottom-bar');
            element.find('td').addClass('td-with-bottom-bar-upsidedown');
        }
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

    $('.stateCheckbox').change(function() {
        url = {% url 'json' %} + '?dummy=1';
        $('.stateCheckbox').each(function(){
            if(!$(this).is(":checked")){
                url += "&" + encodeURIComponent(this.name) + "=0";
            }
        });
        reloadData(url);
    });

    function stateImage(imgSrc, link) {
	iconHiddenClass = "";		
	hrefBegin = "";
	hrefEnd = "";	
	if(link == null)
	    iconHiddenClass = "icon-hidden";
	else
	{	
	    hrefBegin = '<a href="' + link + '">';
	    hrefEnd = "</a>";
	} 
	return hrefBegin + '<img class="source-icon ' + iconHiddenClass + '" src="' + imgSrc+ '">' + hrefEnd;
    }

    function stateFormatter(value) {
	console.log(value);
	toReturn = "";
	toReturn += stateImage("static/img/icon_linkedin.png", value.linkedin);
	toReturn += stateImage("static/img/icon_goldenline.png", value.goldenline);
	toReturn += stateImage("static/img/icon_email.png", value.email);	
	return toReturn;
    }

    function attachmentsListFormatter(value) {
        toReturn = '<div class="innertd">';
        toReturn += '<form id="my-awesome-dropzone" class="dropzone" action="{% url "upload" %}" method="post" enctype="multipart/form-data">';
        toReturn += 'drop file here to upload';
        toReturn += "{% csrf_token %}";
        toReturn += '<input type="hidden" class="personid" name="person" value="'+ $() +'">';
        toReturn += '</form>';

        i = 0;
        value.forEach(function(){
            toReturn += '<a href="candidate/attachment/get/' + value[i].pk + '">'
            toReturn += value[i].display_name
            toReturn += '</a><br>';
            i++;
        });

        toReturn += "</div>";
        return toReturn;
    }

    function caveatsFormatter(value) {
        toReturn = '<div class="innertd"><textarea class="caveatsArea">' + value + '</textarea></div>';
        return toReturn;
    }

    Dropzone.options.myAwesomeDropzone = {
        init: function() {
            this.on("addedfile", function(file) { window.setTimeout(reloadData, 1000); });
        }
    };

    function caveatsTdStyle(row, index){
        return {
                classes: 'lessPaddingTd'
            };
    }

</script>
