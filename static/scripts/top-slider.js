$(document).ready(function(){
	var animation = false;
	var user_active = false;
	var interval;
	var set_time_interval = 5000;
	var max_count = 5;
	var index = 0;

	function start_animation(){
		interval = setInterval(myTimer, set_time_interval); 
		animation = true; 
	}

	function hide_all_images(){
		for(let i=1; i < max_count+1; i++){
			let button = document.getElementById('button'+i);
			let image = document.getElementById('image'+i);
			$(button).removeClass('active_state_control_button');
			$(image).addClass('hiden');
		}
	}

	function show_image(index){
		/**/
		hide_all_images()

		if (index == 1){
			last_index = max_count;
		}

		let next_button = document.getElementById('button'+index);
		let next_image = document.getElementById('image'+index);
		$(next_button).addClass('active_state_control_button');
		$(next_image).removeClass('hiden');
	}

	function myTimer(){
		index++;

		if (index == max_count+1){
			index = 1;
		}

		show_image(index);
	}

	if (animation == false){
		if(user_active == false){
			start_animation();
		}
	}

	function stop(){
	    clearInterval(interval);
	    animation = false;
	}

	$('.image').mouseenter(function(){
		user_active = true;
		stop();	
	});

	$('.image').mouseleave(function(){
		start_animation();
	});

	$('.control_button').mouseenter(function(){
		$(this).addClass('active_state_control_button');	
		user_active = true;
		stop();	
	});

	$('.control_button').mouseleave(function(){
		$(this).removeClass('active_state_control_button');
		start_animation();
	});

	$('.control_button').click(function(){
		show_image(parseInt($(this).index())+1);
		user_active = true;
		stop();
	});

});