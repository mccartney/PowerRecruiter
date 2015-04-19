var CLICK_TIMEOUT = 1200;
//We can have only one test in one file
QUnit.test("simple Test", function( assert ) {
    $( document ).ready(function(){
        assert.ok(1 == 1, "simple test");
        assert.ok($(".statsli.active").length > -1, "statsli menu index");
        setTimeout(function(){
            assert.ok($(".c3-bars-First-meeting").length == 2, "lineChart generated");
            start();
        }, CLICK_TIMEOUT)
    });
});
