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
