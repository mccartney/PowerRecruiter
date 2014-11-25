var NameField = function(candidateId, candidateName){
    this.candidateId = candidateId;
    this.candidateName = candidateName;
    this.editMode = false;

    this.editModeBox = function(){
        toReturn = "<input type='text' class='changeNameInput' id='changeNameInputUnique-" + this.candidateId + "' value='" + this.candidateName + "'>";
        toReturn += '<span class="glyphicon glyphicon-ok edit-ok blockTableEvent" id="nameContainerOk-' + this.candidateId + '" aria-hidden="true"></span>';
        toReturn += '<span class="glyphicon glyphicon-remove edit-remove blockTableEvent" id="nameContainerRemove-' + this.candidateId + '" aria-hidden="true"></span>';
        return toReturn;
    }

    this.standardModeBox = function(){
        toReturn = '<div id="nameInnerContainer-' + this.candidateId + '">';
        toReturn += this.candidateName;
        toReturn += '<span class="glyphicon glyphicon-pencil edit-pencil" id="nameContainerPencil-' + this.candidateId + '" aria-hidden="true"></span>';
        toReturn += '</div>';
        return toReturn;
    }

    this.setEditable = function(){
        this.editMode = true;
        this.refresh();
    }

    this.clickOk = function(){
        this.editMode = false;
        this.refresh();
    }

    this.clickCancel = function(){
        this.editMode = false;
        this.refresh();
    }

    this.updateEventListeners = function(){
        var myobject = this;
        $("#nameInnerContainer-" + this.candidateId).mouseenter(function() {
            $("#nameContainerPencil-" + myobject.candidateId).show();
        });

        $("#nameInnerContainer-" + this.candidateId).mouseleave(function() {
            $("#nameContainerPencil-" + myobject.candidateId).hide();
        });

        $("#nameContainerPencil-" + this.candidateId).click(function(e){
            e.stopPropagation();
            myobject.setEditable();
        });

        $("#nameContainerRemove-" + this.candidateId).click(function(e){
            e.stopPropagation();
            myobject.clickCancel();
        });

        $("#nameContainerOk-" + this.candidateId).click(function(e){
            e.stopPropagation();
            myobject.clickOk();
        });
    }

    this.refresh = function(){
        $("#nameContainerUnique-" + this.candidateId).html(this.toString());
        this.updateEventListeners();
    }

    this.toString = function() {
        toReturn = this.standardModeBox();
        if (this.editMode)
            toReturn = this.editModeBox();
        return "<div id='nameContainerUnique-" + this.candidateId + "'>" + toReturn + "</div>";
    }
}
