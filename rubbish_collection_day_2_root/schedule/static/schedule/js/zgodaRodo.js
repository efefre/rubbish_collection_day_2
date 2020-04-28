function areCookiesEnabled() {
    var cookieEnabled = (navigator.cookieEnabled) ? true : false;
    if (typeof navigator.cookieEnabled == "undefined" && !cookieEnabled) {
        document.cookie = "testcookie";
        cookieEnabled = (document.cookie.indexOf("testcookie") != -1) ? true : false;
    }
    return (cookieEnabled);
}

function getCookie(CookieName) {
    var i, x, Ciastka = document.cookie.split(";");
    var y = "";
    for (i = 0; i < Ciastka.length; i++) {
        x = Ciastka[i].substr(0, Ciastka[i].indexOf("="));
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == CookieName) {
            y = Ciastka[i].substr(Ciastka[i].indexOf("=") + 1);
        }
    }
    return unescape(y);
}

function setCookie(CookieName, Value, Days) {
    var ExpDate = new Date();
    ExpDate.setDate(ExpDate.getDate() + Days);
    var CookieString = escape(Value) + ((Days == null) ? "" : "; expires=" + ExpDate.toUTCString());
    document.cookie = CookieName + "=" + CookieString;
}

function HideCookiesBlock() {
    var divBlock = document.getElementById("cookies-blok");
    divBlock.style.display = "none";
}
