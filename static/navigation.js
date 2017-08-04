
function customTabActivate(element, hash) {
    $(element+" a").each(function () {
        var href = $(this).attr('href');
        if (hash == href) {
            $(this).closest('li').addClass('active');
        }else{
            $(this).closest('li').removeClass('active');
        }
    });
}

function tabActivate(element) {
    var path = window.location.hash;

    $(element+" a").each(function () {
        var href = $(this).attr('href');
        if (path == href) {
            $(this).closest('li').addClass('active');
        }else{
            $(this).closest('li').removeClass('active');
        }
    });
}

function navActivate(element) {
    var path = window.location.pathname;
    path = path.replace(/\/$/, "");
    path = decodeURIComponent(path);

    $(element+" a").each(function () {
        var href = $(this).attr('href');
        if (path == href) {
            $(this).closest('li').addClass('active');
        }
    });
}