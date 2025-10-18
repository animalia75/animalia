// FAIT PAR ALAN ET VINCENT
function getRandomInt(max) {
	return Math.floor(Math.random() * max);
}

function simplifiedString(str) {
	return str.normalize("NFD").replace(/\p{Diacritic}/gu, "").replace(" ", "_").replace(/[.,\/#!$%\^&\*;:{}=\-`~()\s]/g, "").toLowerCase()
}

function disable(button) {
	button.disabled = true
}

function enable(button) {
	button.disabled = false
}

class Animal {
	nomVernaculaire
	classification

	constructor(nom) {
		this.nomVernaculaire = nom[0].toUpperCase() + nom.substr(1).replaceAll("_", " ")
		fetch(`data/${nom}.json`)
			.then((response) => response.json())
			.then((json) => {
				this.classification = json.classification
				document.getElementById("photo").setAttribute("src", json.imgUrl)
				for (const [key, _] of [["Nom vernaculaire", ""]].concat(this.classification)) {
					const newLabel = document.createElement("div")
					newLabel.className = "label"
					const newInput = document.createElement("div")
					newInput.className = "value"
					newLabel.textContent = key
					newInput.id = simplifiedString(key)
					const newInputGroup = document.createElement("div")
					newInputGroup.appendChild(newLabel)
					newInputGroup.appendChild(newInput)
					newInputGroup.className = "input-group"
					document.getElementById("inputs").appendChild(newInputGroup)
				}
			console.log(this.classification)
			})
	}
}

window.addEventListener('load',
	async function () {
		const dummysong = this.document.getElementById("dummysong")
		this.document.getElementById("music").play()
		this.document.getElementById("dummy").addEventListener("click", function() {
			dummysong.pause()
			dummysong.currentTime = 0
			dummysong.play()
		})

		const response = await fetch('data/list.json')
		const animals = await response.json()
		let currentAnimal = new Animal(animals[getRandomInt(animals.length)])

		const check = document.getElementById("check")
		const next = document.getElementById("next")

		disable(next)

		const response_2 = await fetch('data/auto_complet_option.json')
		const options = await response_2.json()
		const suggestions = document.getElementById('suggestions')
		const guessInput = document.getElementById("guess")
		guessInput.addEventListener('input', function (event) {
			const guess = simplifiedString(event.target.value)
			const result = guess ? options.filter(item => simplifiedString(item).includes(guess)) : []
			suggestions.innerHTML = ''

			result.forEach(resultItem => {
				const suggestion = document.createElement("li")
				const button = document.createElement("button")
				button.style = "opacity: 0"
				suggestion.innerText = resultItem
				suggestion.className = "suggestion"
				suggestion.addEventListener("click", function() {
					guessInput.value = resultItem
					guessInput.dispatchEvent(new Event("input"))
					guessInput.focus()
				})
				suggestion.appendChild(button)
				suggestions.appendChild(suggestion)
			})
		
			

			
			if (guess === simplifiedString(currentAnimal.nomVernaculaire)) {
				document.getElementById("nom_vernaculaire").innerText = currentAnimal.nomVernaculaire
				guessInput.value = ""
				guessInput.dispatchEvent(new Event("input"))
			}
			for (const [key, value] of currentAnimal.classification) {
				if (guess === simplifiedString(value)) {
					const fieldInput = document.getElementById(simplifiedString(key))
					if (fieldInput.innerText == "") {
						document.getElementById(simplifiedString(key)).innerText = value
						guessInput.value = ""
						guessInput.dispatchEvent(new Event("input"))
					}
				}
			}
			
			
		});
		let score = 0
		check.addEventListener("click", function() {				
			for (const [key, value] of currentAnimal.classification.concat([["nom_vernaculaire", currentAnimal.nomVernaculaire]])) {
				const currentField = document.getElementById(simplifiedString(key))
				if(currentField.innerText !== "") {
					currentField.style="color: green;"
					++score
					document.getElementById("scoreID").innerText = "Score : " + score
				} else {
					currentField.innerText = value
					currentField.style="color: red;"
				}
			}
			disable(check)
			enable(next)
		})

		next.addEventListener("click", function() {
			document.getElementById("inputs").remove()
			const inputs = document.createElement("div")
			inputs.id = "inputs"
			inputs.className = "right"
			guessInput.value = ""
			guessInput.dispatchEvent(new Event("input"))
			document.getElementById("container").appendChild(inputs)
			currentAnimal = new Animal(animals[getRandomInt(animals.length)])
			disable(next)
			enable(check)
		})

		

		
	}

)
