let modal = document.createElement('div')
modal.setAttribute('id','modal-window')
modal.setAttribute('class','modal')
modal.innerHTML = ` 
  <span class="close">&times;</span>
  <img class="modal-content" id="modal-image">
  <div id="caption"></div>
` 
document.body.appendChild(modal) 

document.querySelectorAll("img").forEach( (el,idx) => {
  el.setAttribute('title','Klik om te vergroten')
  el.addEventListener ('click', (el) => {
      document.querySelector("#modal-image").src = el.target.currentSrc
      document.querySelector("#modal-image").setAttribute('title','Klik om te sluiten')
      document.querySelector("#caption").innerHTML = el.target.alt
      modal.style.display = "block";
    })
})


modal.addEventListener('click', () => modal.style.display = "none" ) 
