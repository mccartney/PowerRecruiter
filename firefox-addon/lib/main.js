var contextMenu = require('sdk/context-menu');
var menuItem = contextMenu.Item({
  label: 'Load LinkedIn profile to PowerRecruiter',
  context: contextMenu.URLContext('https://www.linkedin.com/profile/*'),
  contentScript: 'self.on("click", function () {' +
	    		 '    function getContentInContainer(matchClass) { ' +
	        	 '        var elems = document.getElementsByTagName(\'*\'), i;' +
	        	 '        for (i in elems) { ' +
	             '            if((\' \' + elems[i].className + \' \').indexOf(\' \' + matchClass + \' \') ' +
	             '              > -1) { ' +
	             '                return elems[i].innerHTML; ' +
	             '            }' +
	             '        }' +
	             '    }' +
	             '    console.log(getContentInContainer(\'full-name\')) ' +
                 '});'
});
