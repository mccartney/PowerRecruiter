function photoFormatter(value) {
    var DEFAULT_SRC = 'https://static.licdn.com/scds/common/u/images/themes/katy/ghosts/person/ghost_person_200x200_v1.png';
    var src = value.photo == '' ? DEFAULT_SRC : value.photo;
    var imageDiv = '<div class="imageDiv"><img src="' + src + '"/></div>';
    return imageDiv;
}

function idFormatter(value){
    return value.id;
}

function shortenDisplayName(name){
    if(name.length > 16) {
        return name.substr(0, 13) + "...";
    }
    return name;
}

function attachmentsListFormatterWithoutCSRF(value, uploadUrl, csrfToken) {
    toReturn = '<div class="innertd blockTableEvent">';
    toReturn += '<form id="my-awesome-dropzone" class="dropzone" action="' + uploadUrl +'" method="post" enctype="multipart/form-data">';
    toReturn += '(' + value.attachments.length + ') attachment(s)';
    toReturn += csrfToken;
    toReturn += '<input type="hidden" name="person" value="'+ value.candidateId +'">';
    toReturn += '</form>';
    i = 0;
    value.attachments.forEach(function(){
        toReturn += '<div id="attachment' + value.attachments[i].pk + '"">';
        toReturn += '<a href="javascript:removeAttachment(' + value.attachments[i].pk + ')">';
        toReturn += '<span class="glyphicon glyphicon-remove btn-xs" aria-hidden="true"></span>';
        toReturn += '</a>';

        toReturn += '<a href="candidate/attachment/get/' + value.attachments[i].pk + '">';
        toReturn += shortenDisplayName(value.attachments[i].display_name);
        toReturn += '</a><br>';
        toReturn += '</div>';
        i++;
    });

    toReturn += "</div>";
    return toReturn;
}

function contactFormatter(value) {
    linkedinIcon = new stateIcon("static/img/icon_linkedin.png", value.linkedin, 'linkedin', value.candidateId, value.candidateName);
    goldenlineIcon = new stateIcon("static/img/icon_goldenline.png", value.goldenline, 'goldenline', value.candidateId, value.candidateName);
    emailIcon = new stateIcon("static/img/icon_email.png", value.email, 'email', value.candidateId, value.candidateName);
    return "<div class='blockTableEvent contactIcons'>" + linkedinIcon + goldenlineIcon + emailIcon + "</div>";
}

function openDeleteCandidateModal(id, name){
    $("#deleteModalInfo").html("candidate <b> " + name + "</b> with <b>id = " + id +"</b>");
    $("#confirmDeleteButton").off();
    $("#confirmDeleteButton").click(function(){removePerson(id); $('#confirm-delete').modal('hide'); });
    $('#confirm-delete').modal('show');
}

function candidateRemoveHtml(id, name){
    toReturn = '<span class="blockTableEvent">';
    toReturn += '<div class="removePersonButton"><a onclick="openDeleteCandidateModal(' + id + ',\'' + name + '\')" href="#">';
    toReturn += '<span class="glyphicon glyphicon-remove"/></a>';
    toReturn += '</a></div></span>';
    return toReturn;
}

function caveatsFormatter(value) {
    var toReturn = '<div class="innertd"><textarea class="caveatsArea" id="caveats-'+ value.candidateId + '">' + value.caveats + '</textarea></div>';
    //add remove person button to the right of table
    toReturn = candidateRemoveHtml(value.candidateId, value.candidateName) + toReturn;
    return toReturn;
}

function nameFormatter(value) {
    var nameField = new NameField(value.candidateId, value.candidateName);
    setTimeout(function () { nameField.updateEventListeners() }, 100);
    return nameField;
}

function stateHistoryView(value){
    stateHistory = "<div class='oldStateContainer'><div class='oldStateDate'>(from: "  + value.current_state_started + ")</div></div>";
    value.state_history.forEach(function(oldState) {
        stateHistory += "<div class='oldStateContainer'><div><span class='glyphicon glyphicon-arrow-up' aria-hidden='true' style='font-size: 8px'></span></div>";
        stateHistory += "<div class='oldStateName'>" + oldState.state + "</div>";
        stateHistory += "<div class='oldStateDate'>(from " + oldState.startDate + " to " + oldState.changeDate + ")</div></div>";
    });
    return stateHistory;
}

function stateFormatter(value){
    return value.state_view + stateHistoryView(value);
}