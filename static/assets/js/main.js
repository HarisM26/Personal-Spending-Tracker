import { generateMonthlyChart } from './reportcharts.js';

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

generateMonthlyChart("monthly-chart")

/*moved from script.js in css folder*/
window.onload = function(){
  const sidebar = document.querySelector(".sidebar");
  const closeBtn = document.querySelector("#btn");
  const searchBtn = document.querySelector(".bx-search")

  closeBtn.addEventListener("click",function(){
      sidebar.classList.toggle("open")
      menuBtnChange()
  })

  searchBtn.addEventListener("click",function(){
      sidebar.classList.toggle("open")
      menuBtnChange()
  })

  function menuBtnChange(){
      if(sidebar.classList.contains("open")){
          closeBtn.classList.replace("bx-menu","bx-menu-alt-right")
      }else{
          closeBtn.classList.replace("bx-menu-alt-right","bx-menu")
      }
  }
}


const transaction = {
  date: "",
  title: "",
  amount: "",
  category: "",
  notes: "",
  receipt: "",
  created: ""
}

const changeInnerText = (tagId,value) => {
  let transactionItem=document.getElementById(`${tagId}`)
  transactionItem.innerText=value
}
const items = Array.from(document.getElementsByClassName("transaction_list"));

items.forEach( ( button, index ) =>
{
    button.addEventListener("click", () =>
    {  
      const element = items[index]
      for (const child of element.children){
        switch(child.id){
          case "transaction-date":
            transaction.date = child.textContent;
            break;
          case "transaction-title":
            transaction.title = child.textContent;
            break;
          case "transaction-amount":
            transaction.amount = child.textContent;
            break;
          case "transaction-category":
            transaction.category = child.textContent;
            break;
          case "transaction-notes":
            transaction.notes = child.textContent;
            break;
          case "transaction-image":
            transaction.receipt = getFileName(child.src);
            break;
          case "transaction-created":
          transaction.created = child.textContent;
          break;
          default:
            break;
        }
      }
      changeInnerText("transaction-title-modal",transaction.title)
      changeInnerText("transaction-date-modal",transaction.date)
      changeInnerText("transaction-amount-modal",transaction.amount)
      changeInnerText("transaction-category-modal",transaction.category)
      changeInnerText("transaction-notes-modal",transaction.notes)
      changeInnerText("transaction-receipt-modal",transaction.receipt)
      changeInnerText("transaction-created-modal",transaction.created)
    })
    })

/** Inspiration taken from
* https://stackoverflow.com/questions/29182283/javascript-onclick-get-image-name-without-path
**/
function getFileName(fullPath) {
  var filename = fullPath.replace(/^.*[\\\/]/, '');
  // or, try this, 
  // var filename = fullPath.split("/").pop();
  return filename
}
