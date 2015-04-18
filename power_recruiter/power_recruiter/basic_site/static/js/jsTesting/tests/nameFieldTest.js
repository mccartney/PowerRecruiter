QUnit.test("nameField toString", function( assert ) {QUnit.test("nameField change mode", function( assert ) {
  var nameField = new NameField(12, "Jan Kowalski");
  assert.ok(nameField.editMode == false, "started false");
  var nameField = new NameField(12, "Jan Kowalski");
  correctNameFieldHtml = '<div id="nameContainerUnique-12"><div id="nameInnerContainer-12">Jan Kowalski<span class="glyphicon glyphicon-pencil edit-pencil" id="nameContainerPencil-12" aria-hidden="true"></span></div></div>';
  assert.ok(nameField + "" == correctNameFieldHtml, "nameField toString");
  nameField.setEditable();
  correctNameFieldHtmlEdited = '<div id="nameContainerUnique-12"><input type="text" class="changeNameInput" id="changeNameInputUnique-12" value="Jan Kowalski"><span class="glyphicon glyphicon-ok edit-ok" id="nameContainerOk-12" aria-hidden="true"></span><span class="glyphicon glyphicon-remove edit-remove" id="nameContainerRemove-12" aria-hidden="true"></span></div>';
  assert.ok(nameField + "" == correctNameFieldHtmlEdited, "nameField edited toString");;
});

QUnit.test("nameField change mode", function( assert ) {
  var nameField = new NameField(12, "Jan Kowalski");
  assert.ok(nameField.editMode == false, "started false");

  nameField.setEditable();
  assert.ok(nameField.editMode == true, "started edition");

  nameField.clickOk();
  assert.ok(nameField.editMode == false, "saved");

  nameField.setEditable();
  assert.ok(nameField.editMode == true, "started edition");

  nameField.clickCancel();
  assert.ok(nameField.editMode == false, "cancelled");
});