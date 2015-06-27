/*
*Power Recruiter - a browser-based FSM-centered database application profiled for IT recruiters
*Copyright (C) 2015 Krzysztof Fudali, Andrzej Jackowski, Cezary Kosko, Filip Ochnik
*
*This program is free software: you can redistribute it and/or modify
*it under the terms of the GNU General Public License as published by
*the Free Software Foundation, either version 3 of the License, or
*(at your option) any later version.
*
*This program is distributed in the hope that it will be useful,
*but WITHOUT ANY WARRANTY; without even the implied warranty of
*MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*GNU General Public License for more details.
*
*You should have received a copy of the GNU General Public License
*along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

QUnit.test("nameField change mode", function( assert ) {
  var nameField = new NameField(12, "Jan Kowalski");
  assert.ok(nameField.editMode == false, "started false");
  var nameField = new NameField(12, "Jan Kowalski");
  correctNameFieldHtml = '<div id="nameContainerUnique-12"><div id="nameInnerContainer-12">Jan Kowalski<span class="glyphicon glyphicon-pencil edit-pencil" id="nameContainerPencil-12" aria-hidden="true"></span></div></div>';
  assert.ok(nameField + "" == correctNameFieldHtml, "nameField toString");
  nameField.setEditable();
  correctNameFieldHtmlEdited = '<div id="nameContainerUnique-12"><input type="text" class="changeNameInput" id="changeNameInputUnique-12" value="Jan Kowalski"><span class="glyphicon glyphicon-ok edit-ok" id="nameContainerOk-12" aria-hidden="true"></span><span class="glyphicon glyphicon-remove edit-remove" id="nameContainerRemove-12" aria-hidden="true"></span></div>';
  assert.ok(nameField + "" == correctNameFieldHtmlEdited, "nameField edited toString");
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