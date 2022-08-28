const endpoint = '/day/create/'
const search_results_div = document.getElementById('search-content')
const date_picker = document.querySelector('input[type="date"]')
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

function addDay() {
	const date_picker = document.querySelector('input[type="date"]')
	day = date_picker.value
	result = new Date(day)
	result.setDate(result.getDate() + 1)
	date_picker.value = formatDate(result)
	date_changed()
}

function removeDay() {
	const date_picker = document.querySelector('input[type="date"]')
	day = date_picker.value
	result = new Date(day)
	result.setDate(result.getDate() - 1)
	date_picker.value = formatDate(result)
	date_changed()
}

function fill_results(results) {
	const results_div = document.createElement('div')
	if (!results.length) {
		const search_div= document.createElement('div')
		const link 			= document.createElement('a')
		const link_add 	= document.createElement('a')
		const icon 			= document.createElement('i')

		search_div.classList.add('search__result')

		link.classList.add('search__result__text')
		link.href = "/meals/create"
		link.textContent = 'Not found... Create a new meal?'
		link.style.overflow = 'hidden'
		link.style.whiteSpace = 'nowrap'
		link.style.textOverflow = 'ellipsis'

		link_add.style.cursor = 'pointer'

		icon.classList.add('fa')
		icon.classList.add('fa-arrow-up')
		icon.classList.add('search__button')

		link_add.append(icon)

		search_div.append(link)
		search_div.append(link_add)
		results_div.appendChild(search_div)

		const p = document.createElement('p')
		results_div.appendChild(p)
		return results_div
	}

	results.forEach(result => {
		const search_div= document.createElement('div')
		const link 			= document.createElement('a')
		const link_add 	= document.createElement('a')
		const icon 			= document.createElement('i')

		search_div.classList.add('search__result')

		link.classList.add('search__result__text')
		link.href = result.fields['url']
		link.textContent = result.fields['name']
		link.style.overflow = 'hidden'
		link.style.whiteSpace = 'nowrap'
		link.style.textOverflow = 'ellipsis'

		icon.onclick = function() { addMeal(result) }
		link_add.style.cursor = 'pointer'

		icon.classList.add('fa')
		icon.classList.add('fa-plus')
		icon.classList.add('search__button')

		link_add.append(icon)

		search_div.append(link)
		search_div.append(link_add)
		results_div.append(search_div)
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
	console.log('doen')
	const user_input = document.querySelector('input[type="text"]')
	let query_res = user_input.value
	if (query_res) {
		if (query_res !== previousQuery) {
			search(query_res)
			previousQuery = query_res
		}
	} else {
	const search_results_div = document.getElementById('search-content')
	search_results_div.textContent=''
	}
}

function search(query) {
	const search_results_div = document.getElementById('search-content')
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
	console.log(meal_nums)
	console.log(id)
	if (direction === 'up' && meal_nums[id] != 0) {
		meal_nums[id]-=1
	} else if (direction === 'down' && meal_nums[id] != 4) {
		meal_nums[id]+=1
	}
	console.log(meal_nums)
	// Redraw
	fill_day()
}

function fill_day() {
	const meal_div = document.getElementById('meal__box')
	for (i = 0; i < 5; i++)	{
		text = meal_div.children[i].querySelector('.meal__name__div')
		meal_div.children[i].textContent=''
		meal_div.children[i].append(text)
}
	for (i = 0; i < meals.length; i++) {
	var container = document.createDocumentFragment();
	var recipe_div = document.createElement("div");
	recipe_div.id = i
	var e_1 = document.createElement("div");
	e_1.setAttribute("class", "row d-xl-flex justify-content-xl-start align-items-xl-center drag");
	e_1.setAttribute("style", "margin: 3%;background-color: #fff;");
	var e_2 = document.createElement("div");
	e_2.setAttribute("class", "col d-flex d-sm-flex d-md-flex d-lg-flex d-xl-flex align-items-center align-items-sm-center align-items-md-center justify-content-lg-center align-items-lg-center align-items-xl-center");
	var e_3 = document.createElement("img");
	e_3.setAttribute("class", "rounded-circle");
	e_3.setAttribute("style", "object-fit: cover;margin: 2%;width: 66px;height: 66px;");
		console.log(meals[i].fields['image'])
	e_3.setAttribute("src", "/media/"+meals[i].fields['image']);
	e_2.appendChild(e_3);
	var e_4 = document.createElement("div");
	e_4.setAttribute("style", "width: 45%;margin-left: 2%;");
	var e_5 = document.createElement("span");
	e_5.setAttribute("class", "meal_text");
	e_5.appendChild(document.createTextNode(meals[i].fields['name']));
	e_4.appendChild(e_5);
	e_2.appendChild(e_4);
	var e_6 = document.createElement("a");
	e_6.setAttribute("style", "margin-right: 2%;margin-left: auto;");
	var e_7 = document.createElement("i");
	e_7.setAttribute("class", "fa fa-chevron-down meal__button");
	e_7.setAttribute("style", "cursor: pointer;");
e_7.onclick = function() { moveMeal(recipe_div.id,'down') }
	e_6.appendChild(e_7);
	e_2.appendChild(e_6);
	var e_8 = document.createElement("a");
	e_8.setAttribute("style", "margin-right: 2%;margin-left: 2%;");
	var e_9 = document.createElement("i");
	e_9.setAttribute("class", "fa fa-chevron-up meal__button");
	e_9.setAttribute("style", "cursor: pointer;");
		e_9.onclick 			= function() { moveMeal(recipe_div.id, 'up') }
	e_8.appendChild(e_9);
	e_2.appendChild(e_8);
	var e_10 = document.createElement("a");
	e_10.setAttribute("style", "margin-right: 2%;margin-left: 2%; cursor: pointer;");
	var e_11 = document.createElement("i");
	e_11.onclick = function() {removeMeal(recipe_div.id)}
	e_11.setAttribute("class", "fa fa-remove meal_remove");
	e_11.setAttribute("style", "cursor: pointer;");
	e_10.appendChild(e_11);
	e_2.appendChild(e_10);
	e_1.appendChild(e_2);
	recipe_div.appendChild(e_1);
	container.appendChild(recipe_div);
		const text 				= document.createElement('h2')
		const button_rem	= document.createElement('button')
		const button_up		= document.createElement('button')
		const button_down	= document.createElement('button')

		text.textContent 				= meals[i].fields['name']
		button_rem.onclick 			= function() { removeMeal(recipe_div.id) }
		button_up.onclick 			= function() { moveMeal(recipe_div.id, 'up') }
		button_down.onclick 		= function() { moveMeal(recipe_div.id, 'down') }

meal_div.children[meal_nums[i]].append(container)
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

function date_changed() {
	const date_picker = document.querySelector('input[type="date"]')
  search_results_div.textContent=''
	get_day_result(date_picker.value)
}

search_results_div.textContent=''
date_picker.value = now_day
get_day_result(now_day)
