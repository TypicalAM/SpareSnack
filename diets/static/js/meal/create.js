const endpoint = '/meals/create/'
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
		const h5 = document.createElement('h5')
		h5.textContent = 'Nothing found'
		h5.style.fontFamily = "'Merriweather Sans', sans-serif";
		h5.style.marginLeft = '5%'
		h5.style.color = '#757575';
		results_div.append(h5)
		return results_div
	}

	results.forEach(result => {
		const div_VCYJb = document.createElement('div');
		results_div.appendChild(div_VCYJb)
		div_VCYJb.classList.add('result');
		div_VCYJb.id = result.fields['pk'];
		div_VCYJb.style.background = '#e9edf7';
		div_VCYJb.style.border = '1px solid #f2f2f2';
		div_VCYJb.style.fontFamily = "'Merriweather Sans', sans-serif";
		div_VCYJb.style.borderRadius = '10px';
		div_VCYJb.style.padding = '3%';
		div_VCYJb.style.alignItems = 'center';
		div_VCYJb.style.display = 'flex';
		div_VCYJb.style.marginBottom = '3%';
		div_VCYJb.style.boxShadow = '6px 6px 4px #e5e5e5';
		div_VCYJb.style.height = '70px';
		const a_zffOL = document.createElement('button');
		a_zffOL.style.background = '#e9edf7';
		a_zffOL.onclick = function() {
			addIngredient(result)
			results_div.textContent = ''
			document.querySelector('#search__input').value=''
		}
		a_zffOL.style.color = '#757575';
		a_zffOL.style.fontSize = '22px';
		a_zffOL.style.borderBottomStyle = 'none';
		a_zffOL.style.borderStyle = 'none';
		a_zffOL.style.textAlign = 'left';
		a_zffOL.style.fontFamily = "'Josefin Sans', sans-serif";
		a_zffOL.style.width = '95%';
		a_zffOL.style.paddingLeft = '1%';
		div_VCYJb.appendChild(a_zffOL);
		a_zffOL.textContent += result.fields['name'];
		const img_CorHn = new Image();
		img_CorHn.style.width = '45px';
		img_CorHn.style.height = '45px';
		img_CorHn.style.marginLeft = '2%';
		img_CorHn.style.marginRight = 'initial';
		img_CorHn.src = '/media/'+result.fields['image'];
		div_VCYJb.appendChild(img_CorHn);
	})
	return results_div
}



function addIngredient(result)
{
	items_added.push(result)
	amounts.push('0')
	const index = items_added.indexOf(result)
	const ingredients = document.getElementById('ingredients')

	const div_KViTv = document.createElement('div');
	div_KViTv.style.borderRadius = '9px';
	div_KViTv.style.background = '#e9f4f4';
	div_KViTv.style.display = 'grid';
	div_KViTv.style.padding = '3%';
	div_KViTv.style.border = 'hidden';
	div_KViTv.style.marginBottom = '2%';
	div_KViTv.style.boxShadow = '6px 6px 4px #e5e5e5';
	ingredients.appendChild(div_KViTv)
	const div_glsxM = document.createElement('div');
	div_glsxM.classList.add('info');
	div_glsxM.style.height = '70px';
	div_glsxM.style.display = 'flex';
	div_glsxM.style.alignItems = 'center';
	div_KViTv.appendChild(div_glsxM);
	const img_LCAIy = new Image();
	img_LCAIy.style.width = '60px';
	img_LCAIy.style.height = '60px';
	img_LCAIy.style.marginLeft = '2%';
	img_LCAIy.style.marginRight = '3%';
	img_LCAIy.src = '/media/'+result.fields['image'];
	div_glsxM.appendChild(img_LCAIy);
	const div_CNEbD = document.createElement('div');
	div_CNEbD.style.display = 'grid';
	div_CNEbD.style.width = '60%';
	div_glsxM.appendChild(div_CNEbD);
	const span_GwEsQ = document.createElement('span');
	span_GwEsQ.style.fontSize = '25px';
	span_GwEsQ.style.fontFamily = "'Josefin Sans', sans-serif";
	div_CNEbD.appendChild(span_GwEsQ);
	span_GwEsQ.textContent += result.fields['name'];
	const div_FOLJX = document.createElement('div');
	div_CNEbD.appendChild(div_FOLJX);
	const i_xGBIH = document.createElement('i');
	i_xGBIH.classList.add('fa', 'fa-fire');
	i_xGBIH.style.marginRight = '3%';
	i_xGBIH.style.color = '#ff9900';
	div_FOLJX.appendChild(i_xGBIH);
	const small_ldxfa = document.createElement('small');
	small_ldxfa.style.fontSize = '14.8px';
	small_ldxfa.style.fontFamily = "'Josefin Sans', sans-serif";
	small_ldxfa.style.marginRight = '4%';
	small_ldxfa.style.color = '#757575';
	div_FOLJX.appendChild(small_ldxfa);
	small_ldxfa.textContent += `113 kcal`;
	const i_IPNxO = document.createElement('i');
	i_IPNxO.classList.add('fa', 'fa-balance-scale');
	i_IPNxO.style.color = 'rgb(255,29,124)';
	i_IPNxO.style.marginRight = '3%';
	div_FOLJX.appendChild(i_IPNxO);
	const small_KuESt = document.createElement('small');
	small_KuESt.style.fontSize = '14.8px';
	small_KuESt.style.fontFamily = "'Josefin Sans', sans-serif";
	small_KuESt.style.color = '#757575';
	div_FOLJX.appendChild(small_KuESt);
	small_KuESt.textContent += `100g`;
	small_KuESt.onkeyup =function() {
		amounts[index] = small_KuESt.value
	}
	const textarea_zTyxd = document.createElement('textarea');
	textarea_zTyxd.classList.add('form-control', 'grams');
	textarea_zTyxd.style.textAlign = 'center';
	textarea_zTyxd.style.fontSize = '21px';
	textarea_zTyxd.style.fontFamily = "'Josefin Sans', sans-serif";
	textarea_zTyxd.style.width = '15%';
	textarea_zTyxd.style.border = 'hidden';
	textarea_zTyxd.style.backgroundColor = 'white';
	textarea_zTyxd.style.borderRadius = '13px';
	textarea_zTyxd.style.height = '35px';
	textarea_zTyxd.style.resize = 'none!important';
	textarea_zTyxd.style.overflow = 'hidden!important';
	textarea_zTyxd.style.padding = '1%';
	textarea_zTyxd.style.color = '#757575';
	textarea_zTyxd.setAttribute(`placeholder`, `100`);
	div_glsxM.appendChild(textarea_zTyxd);
	const span_Irlvd = document.createElement('span');
	span_Irlvd.style.marginLeft = '1%';
	span_Irlvd.style.color = '#757575';
	div_glsxM.appendChild(span_Irlvd);
	span_Irlvd.textContent += `G`;
	const i_WxUia = document.createElement('i');
	i_WxUia.classList.add('fa', 'fa-close');
	i_WxUia.style.fontSize = 'x-large';
	i_WxUia.style.marginLeft = '2%';
	i_WxUia.style.color = 'var(--vector__tertiary)';
	i_WxUia.onclick = function() {
		items_added = delete items_added[index]
		amounts 		= delete amounts[index]
		console.log(small_KuESt.value)
		ingredients.removeChild(div_KViTv)
	}

	div_glsxM.appendChild(i_WxUia);
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
	const user_input = document.querySelector('#search__input')
	let query_res = user_input.value
	if (query_res) {
		if (query_res !== previousQuery) {
			search(query_res)
			previousQuery = query_res
		}
	} else {
	const search_results_div = document.getElementById('search_results')
	search_results_div.textContent=''
	user_input.textContent = ''
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
