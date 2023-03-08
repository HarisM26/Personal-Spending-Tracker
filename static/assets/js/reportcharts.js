// Create chart
const allMonths = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
                "Sep","Oct","Nov","Dec"];
//Get previous 5 months including current
const currentDate = new Date();
const previousFiveMonths = []
let j = 11;
for (let i = 0; i < 5; i++){
  if(currentDate.getMonth()-i < 0){
    previousFiveMonths[i] = allMonths[j];
    j--;
  }
  else{
  previousFiveMonths[i] = allMonths[currentDate.getMonth()-i];
  }
}
//get content of tags
const totalTransactionSelector = Array.from(document.getElementsByClassName("total-transaction-by-month"))
const months = []
const totalTransactions=[]

totalTransactionSelector.forEach( (item) =>
{
    let elemChildren = item.children;
    for (let i = 0; i < elemChildren.length; i++){
      if(i===0){
        months.push(elemChildren[i].textContent.substring(0,3));
      }
      else{
        totalTransactions.push(elemChildren[i].textContent);
      }
    }
  });

const mapped = months.map((e,i) =>{
  return [e,totalTransactions[i]];
});
//===========

const myData = [0,0,0,0,0,0,0,0,0,0,0,0]

const addData = () => {
  for (let i=0; i < mapped.length; i++){
  let temp = 0;
  for(let j=0; j < mapped[i].length; j++){
    if(j===0){
      temp = allMonths.indexOf(mapped[i][j]);
    }
    else{
      myData[temp] = mapped[i][j];
    }
  }
}
}
addData();

export const generateMonthlyChart= (templateId) => {
const labels = allMonths;
const data = {
  labels: labels,
  datasets: [{
    label: 'Monthly Transactions',
    data: myData,
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