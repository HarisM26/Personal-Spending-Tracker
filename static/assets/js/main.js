import { generateMonthlyChart } from './reportcharts.js';
import { swiper } from './swiper.js';

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
  created: "",
}

const changeInnerText = (tagId,value) => {
  let transactionItem=document.getElementById(`${tagId}`)
  if(transactionItem !== null && transactionItem.tagName !== 'IMG'){
  transactionItem.innerText=value
  }
  else if(transactionItem !== null && transactionItem.tagName === 'IMG'){
  transactionItem.src = value
  }
}
const items = Array.from(document.getElementsByClassName("transaction_list"));

items.forEach( ( button, index ) =>
{
    button.addEventListener("click", () =>
    {  
      const element = items[index]
      transaction.receipt = ""
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
            console.log(transaction.receipt)
            transaction.receipt = child.src;
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

// call swiper from swiper.js
swiper

  
//console.log(totalTransactions[0].textContent)