$(".witch>li").click(function (e) { 
    $(this).css("border-bottom","2px solid #fff").siblings().css("border-bottom","none");
    var aid = $(this).attr("id");
    if( aid == "registerButton" ){
        $(".content>.loginOrRegisterBox").css("height","400px");
        $("#login").css("display","none");
        $("#register").css("display","block");
    } else if( aid == "loginButton" ) {
        $(".content>.loginOrRegisterBox").css("height","340px");
        $("#login").css("display","block");
        $("#register").css("display","none");
    }
});
