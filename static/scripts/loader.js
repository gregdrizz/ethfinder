$(window).on("load",function(){
    $(".loader-wrapper").fadeOut("slow");
});

$(window).bind("pageshow", function(event) {
    $(".loading-wrapper").hide();
});

window.onpageshow = function (event) {
    if (event.persisted) {
        window.location.reload();
    }
};