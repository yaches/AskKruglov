$('.js-like-question').on('click', function() {
	var $btn = $(this);
	$.ajax({
		url: '/like_question/',
		method: 'POST',
		data: {
			id: $btn.data('id'),
			type: $btn.data('type'),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		}
	}).done(function(resp) {
		if(resp && resp.status == 'ok') 
		{
			document.getElementById('question-' + $btn.data('id') + '-likes').innerHTML = resp.likes;
		}
	})
	return false;
});

$('.js-like-answer').on('click', function() {
	var $btn = $(this);
	$.ajax({
		url: '/like_answer/',
		method: 'POST',
		data: {
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
			id: $btn.data('id'),
			type: $btn.data('type')
		}
	}).done(function(resp) {
		if(resp && resp.status == 'ok') 
		{
			document.getElementById('answer-' + $btn.data('id') + '-likes').innerHTML = resp.likes;
		}
	})
	return false;
});

$('.correct').on('click', function() {
	var $check = $(this);
	$.ajax({
		url: '/correct/',
		method: 'POST',
		data: {
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
			id: $check.data('id')	
		}
	}).done(function(resp) {
		if (resp && resp.status == 'ok')
		{
			// if (resp.correct == true)
			// {
			// 	// $(this).css('color', 'green');
			// 	// document.getElementsByClassName('correct')[0].style.color = 'green';
			// 	document.getElementById($check.data('id') + '-correct').innerHTML = 'lalala';
			// 	console.log('222');
			// }
			// console.log('111');
		}
	})
});