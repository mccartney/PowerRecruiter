var NameField = function(candidate_id, candidate_name){
    this.candidate_id = candidate_id;
    this.candidate_name = candidate_name;
    this.editMode = false;

    this.editModeBox = function(){
        toReturn = '<input type="text" class="changeNameInput" id="changeNameInputUnique-' + this.candidate_id + '" value="' + this.candidate_name + '">';
        toReturn += '<span class="glyphicon glyphicon-ok edit-ok" id="nameContainerOk-' + this.candidate_id + '" aria-hidden="true"></span>';
        toReturn += '<span class="glyphicon glyphicon-remove edit-remove" id="nameContainerRemove-' + this.candidate_id + '" aria-hidden="true"></span>';
        return toReturn;
    }

    this.standardModeBox = function(){
        toReturn = '<div id="nameInnerContainer-' + this.candidate_id + '">';
        toReturn += this.candidate_name;
        toReturn += '<span class="glyphicon glyphicon-pencil edit-pencil" id="nameContainerPencil-' + this.candidate_id + '" aria-hidden="true"></span>';
        toReturn += '</div>';
        return toReturn;
    }

    this.setEditable = function(){
        this.editMode = true;
        this.refresh();
    }

    this.clickOk = function(){
        var new_name = $("#changeNameInputUnique-" + this.candidate_id).val();
        var resp = sendAjax('candidate/change_name/', {
            'id': this.candidate_id,
            'name': new_name
            }, function(data) {
        })
        this.candidate_name = new_name;
        this.editMode = false;
        this.refresh();
    }

    this.clickCancel = function(){
        this.editMode = false;
        this.refresh();
    }

    this.updateEventListeners = function(){
        var myobject = this;
        $("#nameInnerContainer-" + this.candidate_id).mouseenter(function() {
            $("#nameContainerPencil-" + myobject.candidate_id).show();
        });

        $("#nameInnerContainer-" + this.candidate_id).mouseleave(function() {
            $("#nameContainerPencil-" + myobject.candidate_id).hide();
        });

        $("#nameContainerPencil-" + this.candidate_id).click(function(e){
            e.stopPropagation();
            myobject.setEditable();
        });

        $("#nameContainerRemove-" + this.candidate_id).click(function(e){
            e.stopPropagation();
            myobject.clickCancel();
        });

        $("#nameContainerOk-" + this.candidate_id).click(function(e){
            e.stopPropagation();
            myobject.clickOk();
        });
    }

    this.refresh = function(){
        $("#nameContainerUnique-" + this.candidate_id).html(this.toString());
        this.updateEventListeners();
    }

    this.toString = function() {
        toReturn = this.standardModeBox();
        if (this.editMode)
            toReturn = this.editModeBox();
        return '<div id="nameContainerUnique-' + this.candidate_id + '">' + toReturn + '</div>';
    }
}
