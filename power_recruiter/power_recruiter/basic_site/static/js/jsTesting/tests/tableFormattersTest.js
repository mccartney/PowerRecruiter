QUnit.test("notifyFormatter", function( assert ) {
  //Empty notification
  assert.ok(notifyFormatter([]) == "", "Empty notification");

  //One notification
  notificationNode = notifyFormatter([{message: "One notification"}]);
  assert.ok(
    /One notification/.test(notificationNode)
    && /div class="notification-icon"/.test(notificationNode)
    && /data-toggle="popover"/.test(notificationNode)
    && !/id/.test(notificationNode)
    && /data-html="true"/.test(notificationNode)
    , "One notification"
  );

  //3 notifications
  notificationNode = notifyFormatter([{message: "123"}, {message: "456"}, {message: "789"}]);
  assert.ok(
    /123<br>/.test(notificationNode)
    && /456<br>/.test(notificationNode)
    && /789/.test(notificationNode)
    , "Three notifications"
  );
});

QUnit.test("photoFormatter", function( assert ) {
  //No photo
  src = "https://static.licdn.com/scds/common/u/images/themes/katy/ghosts/person/ghost_person_200x200_v1.png";
  assert.ok(photoFormatter({dumbObject: "xD"}).search('<div class="imageDiv"><img src="' + src + '"/></div>') >= 0, "No photo");

  //Photo
  src = "http://test.photo.pl/png.png";
  assert.ok(photoFormatter({photo: src}).search('<div class="imageDiv"><img src="' + src + '"/></div>') >= 0, "Photo");

  //Photo with notifications
  src = "http://test.photo.pl/png.png";
  assert.ok(photoFormatter({photo: src, notifications: [{message: "notify that"}]}).search('<div class="imageDiv"><img src="' + src + '"/></div>') > 0, "Photo with notifications");
});

QUnit.test("idFormatter", function( assert ) {
  assert.ok(idFormatter({id: 3}) == 3, "idFormatter");
});

QUnit.test("Shorten name", function( assert ) {
  assert.ok(shortenName("Plik1111234.zip", 13) == "Plik1111234.zip", "full name");
  assert.ok(shortenName("NNPlik1111234.zip", 13) == "NNPlik1111234...", "shorten name");
});

QUnit.test("attachmentsListFormatterWithoutCSRF", function( assert ) {
  value = {attachments: []};
  uploadUrl = "http://upload";
  csrfToken = "12345";
  divNode = '<div class="innertd blockTableEvent"><form id="my-awesome-dropzone" class="dropzone" action="http://upload" method="post" enctype="multipart/form-data">(0) attachment(s)12345<input type="hidden" name="person" value="undefined"></form></div>';
  assert.ok(divNode == attachmentsListFormatterWithoutCSRF(value, uploadUrl, csrfToken), "0 attachements");

  first_name = "first.jpg";
  third_name = "third.pdf";
  value = {attachments: [{pk: 1, display_name: first_name}, {pk: 2, display_name: "second.zip"}, {pk: 3, display_name: third_name}]};
  divNode = attachmentsListFormatterWithoutCSRF(value, uploadUrl, csrfToken)
  assert.ok(
    divNode.search(first_name) >= 0
    && divNode.search(third_name) >= 0
    && divNode.search("get/1") >= 0
    && divNode.search("get/2") >= 0
    && divNode.search(/javascript\:removeAttachment\(2/) >= 0
    && divNode.search(/javascript\:removeAttachment\(3/) >= 0
   , "3 attachements");
});

QUnit.test("contactFormatter", function( assert ) {
  candidate = {
    candidate_id : 1,
    candidate_name : "Jan Kowalski",
    linkedin : "http://linkedin.com/link",
    goldenline : "http://goldenline.com/link",
    email : "jankowalski@testmail.com"
  }
  validContact = '<div class="blockTableEvent contactIcons"><a href="http://linkedin.com/link"><img class="source-icon" src="static/img/icon_linkedin.png"></a><a href="http://goldenline.com/link"><img class="source-icon" src="static/img/icon_goldenline.png"></a><a href="mailto:jankowalski@testmail.com"><img class="source-icon" src="static/img/icon_email.png"></a></div>';
  assert.ok(contactFormatter(candidate) == validContact, "contact");
});

QUnit.test("candidateRemoveHtml", function( assert ){
  validRemoveHtml = '<span class="blockTableEvent"><div class="removePersonButton"><a onclick="openDeleteCandidateModal(3,\'Jan Kowalski\')" href="#"><span class="glyphicon glyphicon-remove"/></a></a></div></span>';
  assert.ok(candidateRemoveHtml(3, "Jan Kowalski") == validRemoveHtml, "candidateRemoveHtml");
});

QUnit.test("caveatsFormatter", function( assert ){
  validCandidateRemoveHtml = '<div class="innertd"><textarea class="caveatsArea" id="caveats-5">ABC</textarea></div>';
  caveatsCandidate = {
    candidate_id : 5,
    candidate_name : "Jan Kowalski",
    caveats : "ABC"
  }
  assert.ok(
    candidateRemoveHtml(caveatsCandidate.candidate_id, caveatsCandidate.candidate_name) + validCandidateRemoveHtml == caveatsFormatter(caveatsCandidate),
    "caveats test"
  );
});

QUnit.test("nameFormatter", function( assert ){
  id = 3;
  name = "Jan Kowalski";
  nameField = new NameField(id, name);
  candidate = { candidate_id : id, candidate_name : name }
  assert.ok(nameFormatter(candidate) + "" == nameField + "", "nameFormatter");
});