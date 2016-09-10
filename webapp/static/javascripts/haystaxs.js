$(function () {
    /********************************************/
    // Initialize Semantic Modules
    /********************************************/
    //dropdown
    $('.ui.dropdown').dropdown();

    /********************************************/
    // Haystaxs Modules
    /********************************************/
    $(".filter .text").click(function () {
        $(this).parent().toggleClass("opened");
    });
    $(".collapse-btn").click(function () {
        $(".ui.content.container").toggleClass("expand-content");
    });
});