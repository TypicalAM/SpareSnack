$(document).ready(function(){

	$('[data-bss-chart]').each(function(index, elem) {
		console.log('firing')
		this.chart = new Chart($(elem), $(elem).data('bss-chart'));
	});

});
