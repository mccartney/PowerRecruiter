function loadLinkedIn(elem) {
    console.log(elem);
}

var contextMenu = require('sdk/context-menu');
var linkedInMenuItem = contextMenu.Item({
  label: 'Load LinkedIn profile to PowerRecruiter',
  context: contextMenu.URLContext('https://www.linkedin.com/profile/*'),
  contentScript: 'self.on("click", function () {' +
                 '    self.postMessage([document.getElementsByClassName(\'full-name\')[0].innerHTML, document.getElementsByClassName(\'profile-picture\')[0].getElementsByTagName(\'img\')[0].src, document.URL]);' +
                 '});',
  onMessage: function(elem) {
    loadLinkedIn(elem);
  }
});
