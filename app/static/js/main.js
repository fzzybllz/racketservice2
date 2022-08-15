// Not working

$(".nav .nav-link").on("click", function(){
    $(".nav").find(".active").removeClass("active");
    $(this).parent().addClass("active");
 });