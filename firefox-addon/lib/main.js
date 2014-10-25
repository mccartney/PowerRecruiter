function loadProfile(elem) {
    var Request = require("sdk/request").Request;
    Request({
      url: "http://localhost:8000/candidate/add",
      content: {'args':elem},
      onComplete: function (response) {
        console.log('load status: ' + response);
      }
    }).post();
    console.log(elem);
}

var contextMenu = require('sdk/context-menu');
var linkedInMenuItem = contextMenu.Item({
  label: 'Load LinkedIn profile to PowerRecruiter',
  context: contextMenu.URLContext('https://www.linkedin.com/profile/*'),
  contentScript: 'self.on("click", function () {' +
                 '    self.postMessage([document.getElementsByClassName(\'full-name\')[0].innerHTML, document.getElementsByClassName(\'profile-picture\')[0].getElementsByTagName(\'img\')[0].src, document.URL]' +
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