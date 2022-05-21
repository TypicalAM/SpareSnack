const endpoint = '/d/day/create/'
let typingTimer;
let doneTypingInterval = 50;
let previousQuery = '';
let now_day = formatDate(new Date());
let meals = new Array();
let meal_nums = new Array();
let input_test = document.getElementById('date');

function padTo2Digits(num) {
  return num.toString().padStart(2, '0');
}

function formatDate(date) {
  return [
    date.getFullYear(),
    padTo2Digits(date.getMonth() + 1),
    padTo2Digits(date.getDate()),
  ].join('-');
}

function fill_results(results) {
	const results_div = document.createElement('div')
	if (!results.length) {
		const p = document.createElement('p')
		p.textContent = 'Nothin found'
		results_div.append(p)
		return results_div
	}

	results.forEach(result => {
		const ingr_div= document.createElement('div')
		const heading = document.createElement('h3')
		const button 	= document.createElement('button')

		heading.textContent = result.fields['name']
		button.textContent 	= 'meal'
		button.onclick 			= function() { addMeal(result) }
		ingr_div.append(heading)
		ingr_div.append(button)
		results_div.append(ingr_div)
	})
	return results_div
}

function addMeal(result) {
	meals.push(result)
	meal_nums.push(0)
	fill_day()
}

function searchKeyUp() {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(doneTyping, doneTypingInterval);
}

function searchKeyDown() {
 clearTimeout(typingTimer);
}

function doneTyping() {
	const user_input = document.querySelector('input')
	let query_res = user_input.value
	if (query_res) {
		if (query_res !== previousQuery) {
			search(query_res)
			previousQuery = query_res
		}
	} else {
	const search_results_div = document.getElementById('search_results')
	search_results_div.textContent='Nothin'
	}
}

function search(query) {
	const search_results_div = document.getElementById('search_results')
	get_search_result(query,true).then(response => {
		const results = JSON.parse(response['search_results'])
		search_results_div.textContent = ''
		search_results_div.append(fill_results(results))
	})
}

async function get_search_result(query, search) {
	const data = {
		headers : {
			'Accept' : 'application/json'
		}
	}
	let params = (search) ? { q:query } : { d:query }
	let url = endpoint + '?' + (new URLSearchParams(params)).toString();
  const response = await fetch(url, data);
  return await response.json();
}

function removeMeal(id) {
	console.log(id)
	console.log(meals)
	meals.splice(id, 1)
	meal_nums.splice(id, 1)
	console.log(meals)
	// Redraw
	fill_day()
}

function moveMeal(id, direction) {
	if (direction === 'up' && meal_nums[id] != 0) {
		meal_nums[id]-=1
	} else if (direction === 'down' && meal_nums[id] != 4) {
		meal_nums[id]+=1
	}
	// Redraw
	fill_day()
}

function fill_day() {
	const meal_div = document.getElementById('meals')
	for (i = 0; i < 5; i++)	meal_div.children[i].textContent = ''
	for (i = 0; i < meals.length; i++) {
		const recipe_div 	= document.createElement('div')
		const text 				= document.createElement('h2')
		const button_rem	= document.createElement('button')
		const button_up		= document.createElement('button')
		const button_down	= document.createElement('button')

		recipe_div.id 					= `${i}`
		text.textContent 				= meals[i].fields['name']
		button_rem.textContent 	= 'remove'
		button_up.textContent		= 'up'
		button_down.textContent = 'down'
		button_rem.onclick 			= function() { removeMeal(recipe_div.id) }
		button_up.onclick 			= function() { moveMeal(recipe_div.id, 'up') }
		button_down.onclick 		= function() { moveMeal(recipe_div.id, 'down') }

		recipe_div.append(text)
		recipe_div.append(button_rem)
		recipe_div.append(button_up)
		recipe_div.append(button_down)
		meal_div.children[meal_nums[i]].append(recipe_div)
	}
	post_day(now_day).then(response => {
		console.log(response)
	})
}

function get_day_result(day) {
	now_day = day
	get_search_result(day,false).then(response => {
		meals = JSON.parse(response['meals'])
		meal_nums = JSON.parse(response['meal_nums'])
		fill_day()
	})
}

async function post_day(date) {
	const response = await fetch(endpoint, {
    method		: "POST",
    headers		: { "Content-type": "application/json" },
		body 			: JSON.stringify({
			meals 		: JSON.stringify(meals),
			meal_nums : JSON.stringify(meal_nums),
			date 			: date
		})
	})
  return await response.json()
}

new DatePicker(input_test, {
	outputFormat: input_test.getAttribute('data-format'),
	onPick: function(date){
	const search_results_div = document.getElementById('search_results')
	search_results_div.textContent='Nothin'
	get_day_result(formatDate(date))
	}
});

get_day_result(now_day)

