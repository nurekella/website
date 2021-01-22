$(function() {
	$(window).scroll(function(){	
		if($(this).scrollTop() >= 175){
			$('#toTop').fadeIn();
			$('.st_nav').addClass('float');
	 	}

	 	else{
	 		$('#toTop').fadeOut();
			$('.st_nav').removeClass('float');	
	 	}

});
 
$('#toTop').click(function() {
	$('body, html').animate({scrollTop:0}, 800);
});
 
});