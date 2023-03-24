import { generateMonthlyChart } from './reportcharts.js';
import { generateCategoryChart } from './reportcharts.js';
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

//toggle notifications

const change_toggle_color = (element) =>{
  if (element.textContent.trim() == "ON"){
    element.style.color = `rgb(${18}, ${158}, ${5})`
  }
  else {
    element.style.color = `rgb(${158}, ${5}, ${5})`
  }
}


const toggle_anchor = Array.from(document.getElementsByClassName("toggle_anchor"));

toggle_anchor.forEach( ( button, index ) =>
{
  const element = toggle_anchor[index]  
    button.addEventListener("click",  
      change_toggle_color(element)
    )
  });  

if(document.getElementById("monthly-chart")){
  generateMonthlyChart("monthly-chart")
}

//===============================sidebar
window.onload = function(){
  const sidebar = document.querySelector(".sidebar");
  const closeBtn = document.querySelector("#btn");

  closeBtn.addEventListener("click",function(){
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

// transaction modal
const transaction = {
  date: "",
  title: "",
  amount: "",
  category: "",
  notes: "",
  receipt: "",
  points: "",
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

const items = Array.from(document.getElementsByClassName("transaction-detail-container"));

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
          case "transaction-points":
            transaction.points = child.textContent;
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
      changeInnerText("transaction-points-modal",transaction.points)
      changeInnerText("transaction-created-modal",transaction.created)

    })
    })

// call swiper from swiper.js
swiper

// generate doughnut chart
const spendingCategorySelector = document.getElementsByClassName("category-in-range")
if (spendingCategorySelector.length > 0){
const doughnutLabel=[]
const doughnutData=[]
const rangeCategorySelector = Array.from(spendingCategorySelector);
rangeCategorySelector.forEach((item)=>{
  for (let i = 0; i < item.children.length; i++){
    if (i<1){
      doughnutLabel.push(item.children[i].textContent)
    }
    else{
      doughnutData.push(item.children[i].textContent)
    }
  }
})
generateCategoryChart("category-chart",doughnutLabel,doughnutData,"doughnut")
}

// generate pie chart
const incomeCategoryElements = document.getElementsByClassName("income-category-hidden")
if(incomeCategoryElements.length > 0){
const pieLabel=[]
const pieData=[]
const incomeCategorySelector = Array.from(incomeCategoryElements);
incomeCategorySelector.forEach((item)=>{
  for (let i = 0; i < item.children.length; i++){
    if (i<1){
      pieLabel.push(item.children[i].textContent)
    }
    else{
      pieData.push(item.children[i].textContent)
    }
  }
})

generateCategoryChart("income-chart",pieLabel,pieData,"pie")
}