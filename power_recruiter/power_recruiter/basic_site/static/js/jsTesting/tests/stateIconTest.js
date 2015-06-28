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

QUnit.test("stateIcon", function( assert ) {
  name = "Jan Kowalski";
  name2 = "Krzysztof Nowak";
  linkedinLink = "http://linkedin.com/testlink";
  linkedinImg = "img.png";
  linkedinIcon = new stateIcon(linkedinImg, linkedinLink, 'linkedin', 123, name);
  emailIcon = new stateIcon("imgemail.png", "test@test.com", 'email', 33, name2);
  emptyEmailIcon = new stateIcon("imgemail.png", null, 'email', 33, name2);
  emptyGoldenIcon = new stateIcon("img.png", null, 'goldenline', 1, name);

  //google link
  assert.ok(linkedinIcon.googleLink() == "http://google.pl/#q=" + name + " linkedin", "googleLink linkedin");
  assert.ok(emailIcon.googleLink() == "http://google.pl/#q=" + name2 + " email", "googleLink email");

  //image tag
  assert.ok(linkedinIcon.imageTag() == '<img class="source-icon" src="img.png">', "existing img");
  assert.ok(emptyGoldenIcon.imageTag() == '<img class="source-icon icon-hidden" src="img.png">', "non-existing img");

  //mail link
  assert.ok(emptyEmailIcon.mailLink() == '<a href="#"><img class="source-icon icon-hidden" src="imgemail.png"></a>', "socialLink empty");

  //social link
  assert.ok(emptyGoldenIcon.socialLink().search(emptyGoldenIcon.googleLink()) >= 0, "socialLink empty");
  assert.ok(linkedinIcon.socialLink() == '<a href="' + linkedinLink + '"><img class="source-icon" src="' + 'img.png' + '"></a>', "socialLink goldenline");

  //toString
  assert.ok(emailIcon+"" == '<a href="mailto:test@test.com"><img class="source-icon" src="imgemail.png"></a>', "email to string");
  assert.ok(linkedinIcon+"" == '<a href="http://linkedin.com/testlink"><img class="source-icon" src="img.png"></a>', "social to string");
});
