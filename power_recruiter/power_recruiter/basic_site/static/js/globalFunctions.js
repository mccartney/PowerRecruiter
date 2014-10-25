/**
 * Created by shadowsword on 25.10.14.
 */

//textEquals jQuery selector
$.expr[':'].textEquals = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().match("^" + arg + "$");
    };
});