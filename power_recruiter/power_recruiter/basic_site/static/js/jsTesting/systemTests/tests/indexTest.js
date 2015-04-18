var no_photo_url = "https://static.licdn.com/scds/common/u/images/themes/katy/ghosts/person/ghost_person_200x200_v1.png";

//We can have only one test in one file
QUnit.test("simple Test", function( assert ) {
    assert.ok(1 == 1, "simple test");
    test_initial_notifications(assert);
    test_initial_candidates(assert);
    test_images(assert);
    test_row_expanding(assert);
    test_change_state(assert);
});

function test_initial_notifications(assert){
    assert.ok($(".alert-danger").text().indexOf("There is one notification") > -1, "notification bar test");
    assert.ok($(".notification-icon").length == 1, "Notifications number");
    assert.ok($(".notification-icon span").attr('data-content').indexOf("Coś za długo nie ma spotkania<br>") > -1, "Notification icon text");
}

function test_initial_candidates(assert){
    assert.ok(count_candidates() == 6, "number of initial candidates");
}

function test_images(assert){
    assert.ok($("td .imageDiv img[src='" + no_photo_url + "']").length == 4, "no photo test")
}

function count_candidates(){
    return $('#maintable tbody tr').length;
}

function test_row_expanding( assert ){
    assert.ok($("tr[data-index=0]").height() == 42, "tr not expanded height");
    assert.ok($("tr[data-index=0] td div img").height() == 25, "img not expanded height");
    assert.ok($("tr[data-index=0] td div img").width() == 25, "img not expanded width");
    assert.ok($("tr[data-index=0] td .oldStateContainer").css('display') == 'none', "img not expanded width");
    $("tr[data-index=0] td").trigger( "click" );
    assert.ok($("tr[data-index=0]").attr('class') == "maintable-row-large", "tr expanded class");
    assert.ok($("tr[data-index=0]").height() == 92, "tr expanded height");
    assert.ok($("tr[data-index=0] td div img").height() == 50, "img not expanded height");
    assert.ok($("tr[data-index=0] td div img").width() == 50, "img not expanded width");
    assert.ok($("tr[data-index=0] td .oldStateContainer").css('display') == 'inline', "img not expanded width");
}

function test_change_state ( assert ){
    assert.ok($("tr[data-index=1] td:nth-child(5) span:nth-child(2)").text().indexOf("Hired") > -1, "original state is hired");
    assert.ok($("tr[data-index=1] td span .popover-content").length == 0, "state_change popover not visible");
    $("tr[data-index=1] td span #leftButton5").trigger( "click" );
    assert.ok($("tr[data-index=1] td span .popover-content").length == 1, "state_change popover visible");
    assert.ok($("tr[data-index=1] td span .popover-content").text().indexOf("More than one") > -1, "state_change popover content");
    $("tr[data-index=1] td span .popover-content p span").trigger("click");
    //Return to old state xD
    stop();
    setTimeout(function(){
        assert.ok($("tr[data-index=1] td span .popover-content").length == 0, "state_change popover not visible");
        assert.ok($("tr[data-index=1] td:nth-child(5) span:nth-child(2)").text().indexOf("More than one") > -1, "new state is More than one..");
        $("tr[data-index=1] td span #rightButton5").trigger( "click" );
        assert.ok($("tr[data-index=1] td span .popover-content").length == 1, "state_change popover visible");
        $("tr[data-index=1] td span .popover-content p:nth-child(3) span").trigger("click");
        setTimeout(function(){
            assert.ok($("tr[data-index=1] td:nth-child(5) span:nth-child(2)").text().indexOf("Hired") > -1, "new state is hired");
            start();
        }, 500);
    }, 500);
}