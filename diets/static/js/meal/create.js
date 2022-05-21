const endpoint = '/d/meals/create/'
let typingTimer;
let doneTypingInterval = 50
let previousQuery = ''
let items_added = new Array();
let amounts = new Array();

function arrayRemove(arr, value)
{
   return arr.filter(function(test){
       return test != value;
   });
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
		const image 	= document.createElement('img')
		const heading = document.createElement('h3')
		const button 	= document.createElement('button')

		ingr_div.id = result.fields['pk']
		heading.textContent = result.fields['name']
		image.src = '/media/'+result.fields['image']

		button.textContent = 'Add the ingrdient'
		button.onclick = function() {
			addMeal(result)
			results_div.textContent = ''
		}
		ingr_div.append(image)
		ingr_div.append(heading)
		ingr_div.append(button)
		results_div.append(ingr_div)
	})
	return results_div
}

function addMeal(result)
{
	items_added.push(result)
	amounts.push('0')
	const index = items_added.indexOf(result)

	const ingredients = document.getElementById('ingredients')
	const ingr_div 		= document.createElement('div')
	const image				= document.createElement('div')
	const name				= document.createElement('h3')
	const amount			= document.createElement('input')
	const cancel			= document.createElement('button')

	ingr_div.append(image)
	ingr_div.append(name)
	ingr_div.append(amount)
	ingr_div.append(cancel)
	ingredients.append(ingr_div)

	name.textContent = result.fields['name']
	image.src = '/media/'+result.fields['image']

	amount.onkeyup = function() {
		amounts[index] = amount.value
	}
	cancel.textContent= 'Remove'
	cancel.onclick 		= function() {
		items_added = delete items_added[index]
		amounts 		= delete amounts[index]
		console.log(amount.value)
		ingredients.removeChild(ingr_div)
	}
	console.log(items_added)
	console.log(amounts)
}

async function get_search_result(query) {
	const data = {
		headers : {
			'Accept' : 'application/json'
		}
	}
	let params = { q:query }
	let url = endpoint + '?' + (new URLSearchParams(params)).toString();
  const response = await fetch(url, data);
  return await response.json();
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
	search_results_div.textContent=''
	}
}

function search(query) {
	const search_results_div = document.getElementById('search_results')
	get_search_result(query).then(response => {
		const results = JSON.parse(response['results'])
		search_results_div.textContent = ''
		search_results_div.append(fill_results(results))
	})
}

function test() {
	const amounts_field = document.getElementById('amounts_form')
	const ingredients_field = document.getElementById('ingredients_form')
	fillFields()
	console.log(items_added)
	console.log(amounts)
	console.log(amounts_field.value)
	console.log(ingredients_field.value)
}

function fillFields() {
	const amounts_field = document.getElementById('amounts_form')
	const ingredients_field = document.getElementById('ingredients_form')
	amounts_field.value = amounts
	ingredients_field.value = JSON.stringify(items_added)
}
