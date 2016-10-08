//semantic modules
//dropdown
$('.ui.dropdown').dropdown();



//haystaxs modules
$( ".filter .text" ).click(function() {
$( this ).parent().toggleClass( "opened" );
});
$( ".collapse-btn" ).click(function() {
$( ".ui.container.content").toggleClass( "expand-content" );
});