var no_photo_url = "https://static.licdn.com/scds/common/u/images/themes/katy/ghosts/person/ghost_person_200x200_v1.png";
var CLICK_TIMEOUT = 1200;

//We can have only one test in one file
QUnit.test("simple Test", function( assert ) {
    $( document ).ready(function(){
        assert.ok(1 == 1, "simple test");
        assert.ok($(".homeli.active").length > -1, "active menu index");
        test_initial_notifications(assert);
        test_initial_candidates(assert);
        test_images(assert);
        test_row_expanding(assert);
        test_change_state(assert);
    });
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
    $("tr[data-index=0] td .imageDiv").trigger( "click" );
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
            test_filter(assert); // TRIGGER test_filter
        }, CLICK_TIMEOUT);
    }, CLICK_TIMEOUT);
}
function test_filter ( assert ){
    assert.ok(count_candidates() == 6, "no filter");
    assert.ok($("ul .dropdown-menu").css('display') == 'none', "filters not visible");
    $(".top-tooltip-inner-left div button").trigger( "click" );
    setTimeout(function(){
        assert.ok($(".top-tooltip-inner-left div ul").css('display') == "block", "filters visible");
        assert.ok($("#state10").is(':checked'), "state checked");
        $("#state10").prop('checked', false);
        assert.ok(!$("#state10").is(':checked'), "state unchecked");
        $("#state10").trigger("change");
        setTimeout(function(){
            assert.ok(count_candidates() == 4, "filter without hired");
            $("#state10").prop('checked', true);;
            assert.ok($("#state10").is(':checked'), "state checked again");
            $("#state10").trigger("change");
            setTimeout(function(){
                assert.ok(count_candidates() == 6, "restore after filitration");
                test_caveats(assert);
            }, CLICK_TIMEOUT);
        }, CLICK_TIMEOUT);
    }, CLICK_TIMEOUT);
}

function test_caveats ( assert ){
    assert.ok($("#caveats-6").val() == "", "no value");
    $("#caveats-6").val("xyz");
    assert.ok($("#caveats-6").val() === "xyz", "xyz value before reload");
    $("#caveats-6").trigger("propertychange");
    setTimeout(function(){
        $("tr th:nth-child(3) .sortable").trigger("click"); //re-sort to reload
        setTimeout(function(){
            assert.ok($("#caveats-6").val() == "xyz", "xyz value after reload");
            $("#caveats-6").val("");
            $("#caveats-6").trigger("propertychange");
            setTimeout(function(){
                assert.ok($("#caveats-6").val() == "", "no value again");
                test_sort(assert);
            }, CLICK_TIMEOUT*2);
        }, CLICK_TIMEOUT);
    }, CLICK_TIMEOUT*2);
}

function test_sort ( assert ){
    assert.ok($("tbody tr:nth-child(1) td:nth-child(3) div").html().indexOf("Wojtek Wawelski") > -1, "sorted once");
    $("tr th:nth-child(3) .sortable").trigger("click"); //re-sort to reload
    setTimeout(function(){
        assert.ok( $("tbody tr:nth-child(1) td:nth-child(3) div").html().indexOf("Jan Kowalski") > -1, "sorted twice");
        test_name_edit(assert);
    }, CLICK_TIMEOUT);
}

function test_name_edit ( assert ){
    assert.ok($("tr[data-index=1] td:nth-child(3) div").html().indexOf("Kamila Kruk") > -1, "name not changed");
    assert.ok($("#nameContainerOk-2").length == 0, "edit-mode off");
    $("#nameContainerPencil-2").trigger( "click" );
    setTimeout(function(){
        assert.ok($("#nameContainerOk-2").length == 1, "edit-mode on");
        $("#changeNameInputUnique-2").val("Kamila Zmieniona");
        $("#nameContainerOk-2").trigger( "click" );
        setTimeout(function(){
            $("tr th:nth-child(3) .sortable").trigger("click"); //reload but don't change order
            setTimeout(function(){
                $("tr th:nth-child(3) .sortable").trigger("click");
                setTimeout(function(){
                    assert.ok($("tr[data-index=1] td:nth-child(3) div").html().indexOf("Kamila Zmieniona") > -1, "name changed");
                    $("#nameContainerPencil-2").trigger( "click" );
                    $("#changeNameInputUnique-2").val("Kamila Kruk");
                    $("#nameContainerOk-2").trigger( "click" );
                    setTimeout(function(){
                        $("tr th:nth-child(3) .sortable").trigger("click"); //reload but don't change order
                        setTimeout(function(){
                            $("tr th:nth-child(3) .sortable").trigger("click");
                            assert.ok($("tr[data-index=1] td:nth-child(3) div").html().indexOf("Kamila Kruk") > -1, "name changed again");
                            $("#nameContainerPencil-2").trigger( "click" );
                            $("#changeNameInputUnique-2").val("Kamila Zmieniona");
                            $("#nameContainerRemove-2").trigger( "click" );
                            $("tr th:nth-child(3) .sortable").trigger("click"); //reload but don't change order
                            $("tr th:nth-child(3) .sortable").trigger("click");
                            assert.ok($("tr[data-index=1] td:nth-child(3) div").html().indexOf("Kamila Kruk") > -1, "name not changed (rejected)");
                            test_add_new_candidate(assert);
                        }, CLICK_TIMEOUT);
                    }, CLICK_TIMEOUT);
                }, CLICK_TIMEOUT);
            }, CLICK_TIMEOUT);
        }, CLICK_TIMEOUT);
    }, CLICK_TIMEOUT);
}

function test_add_new_candidate ( assert ){
    assert.ok(count_candidates() == 6, "not added");
    assert.ok($("#creation-modal").css('display') == "none", "creation modal hidden");
    $(".top-tooltip-inner-right a").trigger( "click" );
    setTimeout(function(){
        assert.ok($("#creation-modal").css('display') == "block", "creation modal showed");
        $("#input-first-name").val("Nowa");
        $("#input-last-name").val("Osoba");
        $("#linkedin-link").val("http://linkedin.com/abc");
        $("#save-candidate").trigger( "click" );
        setTimeout(function(){
            assert.ok(count_candidates() == 7, "candidate added");
            $("tr th:nth-child(2) .sortable").trigger("click"); //sort by id
            setTimeout(function(){
                assert.ok($("tr[data-index=0] td:nth-child(3) div").html().indexOf("Nowa Osoba") > -1, "new candidate name");
                $("tr[data-index=0] .removePersonButton a").trigger( "click" );
                setTimeout(function(){
                    assert.ok($("#confirm-delete").css('display') == "block", "remove modal showed");
                    $("#confirmDeleteButton").trigger( "click" );
                    setTimeout(function(){
                        assert.ok(count_candidates() == 6, "removed candidate");
                        start();
                    }, CLICK_TIMEOUT);
                }, CLICK_TIMEOUT);
            }, CLICK_TIMEOUT);
        }, CLICK_TIMEOUT);
    }, CLICK_TIMEOUT);
}
