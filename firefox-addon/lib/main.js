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

function loadProfile(elem) {
    var Request = require("sdk/request").Request;
    var url = require("sdk/simple-prefs").prefs.serverAddr;

    Request({
	    url: (!/^(f|ht)tps?:\/\//i.test(url) ? "http://" + url : url) + "/candidate/add",
      content: {'args':elem},
      onComplete: function (response) {
        console.log('load status: ' + response.text);
        if(response.status === 200) {
          var notifications = require("sdk/notifications");
          notifications.notify({
            title: "PowerRecruiter",
            text: "Użytkownik dodany"
          });
        } else if (response.status === 418) {
          var notifications = require("sdk/notifications");
          notifications.notify({
            title: "PowerRecruiter",
            text: "Użytkownik istnieje, status: " + response.text
          });
        }
       }
    }).post();
    console.log(elem);
}

var contextMenu = require('sdk/context-menu');
var linkedInMenuItem = contextMenu.Item({
  label: 'Load LinkedIn profile to PowerRecruiter',
  context: contextMenu.URLContext('https://www.linkedin.com/profile/*'),
  contentScript: 'self.on("click", function () {' +
                 '    self.postMessage([document.getElementsByClassName(\'full-name\')[0].innerHTML, document.getElementsByClassName(\'profile-picture\')[0] == undefined ? \'\' : document.getElementsByClassName(\'profile-picture\')[0].getElementsByTagName(\'img\')[0].src, document.URL]' +
                    ');' +
                 '});',
  onMessage: function(elem) {
    loadProfile(elem);
  }
});

var goldenLineMenuItem = contextMenu.Item({
  label: 'Load GoldenLine profile to PowerRecruiter',
  context: contextMenu.URLContext('http://www.goldenline.pl/*'),
  contentScript: 'self.on("click", function () {' +
                 '    self.postMessage([document.getElementsByClassName(\'nameSurname\')[0].innerHTML, document.getElementsByClassName(\'avatar\')[0].getElementsByTagName(\'img\')[0].src, document.URL]' +
                    ');' +
                 '});',
  onMessage: function(elem) {
    loadProfile(elem);
  }
});
