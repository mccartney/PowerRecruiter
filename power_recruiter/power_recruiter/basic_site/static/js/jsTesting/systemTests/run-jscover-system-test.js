//Sample modified from PhantomJS 1.8.2 examples
var system = require('system');

/**
 * Wait until the test condition is true or a timeout occurs. Useful for waiting
 * on a server response or for a ui change (fadeIn, etc.) to occur.
 *
 * @param testFx javascript condition that evaluates to a boolean,
 * it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
 * as a callback function.
 * @param onReady what to do when testFx condition is fulfilled,
 * it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
 * as a callback function.
 * @param timeOutMillis the max amount of time to wait. If not specified, 10 sec is used.
 */
function waitFor(testFx, onReady, timeOutMillis) {
    var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 10001, //< Default Max Timout is 10s
        start = new Date().getTime(),
        condition = false,
        interval = setInterval(function() {
            if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                // If not time-out yet and condition not yet fulfilled
                condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            } else {
                if(!condition) {
                    // If condition still not fulfilled (timeout but condition is 'false')
                    console.log("'waitFor()' timeout");
                    phantom.exit(1);
                } else {
                    // Condition fulfilled (timeout and/or condition is 'true')
                    console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                    typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    clearInterval(interval); //< Stop this interval
                }
            }
        }, 100); //< repeat check every 250ms
};


if (system.args.length !== 3) {
    console.log('Usage: run-jscover-system-test.js DJANGO-URL TEST-SCRIPT');
    phantom.exit(1);
}

var page = require('webpage').create();

page.viewportSize = {
  width: 1600,
  height: 900
};

// Route "console.log()" calls from within the Page context to the main Phantom context (i.e. current "this")
page.onConsoleMessage = function(msg) {
    console.log(msg);
};

page.open(system.args[1], function(status){
    if (status !== "success") {
        console.log("Unable to access network");
        phantom.exit(1);
    } else {
        page.injectJs('../lib/qunit/qunit.js');
        page.injectJs('../lib/qunit-reporter/qunit-reporter-junit.js');
        if (page.injectJs(system.args[2])) {
            page.evaluate(function(){
                //Setup qUnit test
                var reportNum = 0;
                $("body").prepend('<div id="qunit"></div><div id="qunit-fixture"></div>');
                QUnit.jUnitReport = function(report) {
                    reportNum++;
                    //Dunno why on Django sites test execute two time - second time with error
                    if (reportNum == 1)
                        console.log(report.xml);
                };
                QUnit.load();
            });
            waitFor(function(){
                return page.evaluate(function(){
                    var el = document.getElementById('qunit-testresult');
                    if (el && el.innerText.match('completed')) {
                        return true;
                    }
                    return false;
                });
            }, function(){
                var failedNum = page.evaluate(function(){
                    var el = document.getElementById('qunit-testresult');
                    console.log(el.innerText);
                    try {
                        return el.getElementsByClassName('failed')[0].innerHTML;
                    } catch (e) { }
                    return 10000;
                });
                page.evaluate(function(){
                    if (window.jscoverage_report) {
                        jscoverage_report("djangoIntegration");
                    }
                });
                phantom.exit((parseInt(failedNum, 10) > 0) ? 1 : 0);
            });
        }
        else {
            console.log("Cannot load test script")
        }
    }
});