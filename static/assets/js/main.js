
/*tree view*/
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}


const toggle_anchor = document.getElementById("toggle_anchor");

const change_toggle_color = () =>{
  if (toggle_anchor.textContent.trim() == "ON"){
    toggle_anchor.style.color = `rgb(${18}, ${158}, ${5})`
  }
  else {
    toggle_anchor.style.color = `rgb(${158}, ${5}, ${5})`
  }
}

// check if html has loaded - then call listener
if(toggle_anchor !== "undefined" && toggle_anchor !== null){
  toggle_anchor.addEventListener('click' , change_toggle_color())
}
