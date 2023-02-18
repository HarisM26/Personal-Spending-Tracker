
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

// Create chart
const month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
                "Sep","Oct","Nov","Dec"];

//Get previous 5 months including current
const currentDate = new Date();
const previousFiveMonths = []
for (let i = 0; i < 5; i++){
  if(currentDate.getMonth()-i < 0){
    previousFiveMonths[i] = month[13-i];
  }
  else{
  previousFiveMonths[i] = month[currentDate.getMonth()-i];
  }
}

const generateMonthlyChart= (templateId) => {
const labels = previousFiveMonths.reverse();
const data = {
  labels: labels,
  datasets: [{
    label: 'Monthly Transactions',
    data: [ 65, 59, 80, 81, 56],
    backgroundColor: [
      'rgba(54, 162, 235, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(54, 162, 235, 0.2)',
    ],
    borderColor: [
      'rgb(54, 162, 235)',
      'rgb(54, 162, 235)',
      'rgb(54, 162, 235)',
      'rgb(54, 162, 235)',
      'rgb(3, 4, 96)',
    ],
    borderWidth: 2,
    borderRadius: 100
  }]
};

const config = {
  type: 'bar',
  data: data,
  options: {
    responsive: true,
    scales: {
        y: {
         beginAtZero: true,
         display: false
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: ((tooltipItem, data) => {
              return ' £' + tooltipItem.formattedValue
            })
          }
        }
      }
    }
    };

const chartArea = document.getElementById(`${templateId}`);

  return new Chart(chartArea,config);
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