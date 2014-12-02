function idFormatter(value){
    DEFAULT_SRC = 'https://static.licdn.com/scds/common/u/images/themes/katy/ghosts/person/ghost_person_200x200_v1.png';
    src = value.photo == '' ? DEFAULT_SRC : value.photo;
    imageDiv = '<div class="imageDiv"><img src="' + src + '" style="width:50px; height:50px"/></div>';

    return imageDiv + value.id;
}

function shortenDisplayName(name){
    if(name.length > 21) {
        return name.substr(0, 18) + "...";
    }
    return name;
}

function attachmentsListFormatterWithoutCSRF(value, uploadUrl, csrfToken) {
    toReturn = '<div class="innertd">';
    toReturn += '<form id="my-awesome-dropzone" class="dropzone" action="' + uploadUrl +'" method="post" enctype="multipart/form-data">';
    toReturn += 'drop file here to upload';
    toReturn += csrfToken;
    toReturn += '<input type="hidden" class="personid" name="person" value="'+ $() +'">';
    toReturn += '</form>';

    i = 0;
    value.forEach(function(){
        toReturn += '<div id="attachment' + value[i].pk + '">';
        toReturn += '<a href="javascript:removeAttachment(' + value[i].pk + ')">';
        toReturn += '<span class="glyphicon glyphicon-remove btn-xs" aria-hidden="true"></span>';
        toReturn += '</a>';

        toReturn += '<a href="candidate/attachment/get/' + value[i].pk + '">';
        toReturn += shortenDisplayName(value[i].display_name);
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
    return linkedinIcon + goldenlineIcon + emailIcon;
}

function caveatsFormatter(value) {
    toReturn = '<div class="innertd"><textarea class="caveatsArea">' + value + '</textarea></div>';
    return toReturn;
}

function nameFormatter(value) {
    var nameField = new NameField(value.candidateId, value.candidateName);
    setTimeout(function () { nameField.updateEventListeners() }, 100);
    return nameField;
}

function stateFormatter(value){
    return value.state_view;
}