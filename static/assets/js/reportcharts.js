// Create chart
const month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
                "Sep","Oct","Nov","Dec"];

//Get previous 5 months including current
const currentDate = new Date();
const previousFiveMonths = []
let j = 11;
for (let i = 0; i < 5; i++){
  if(currentDate.getMonth()-i < 0){
    previousFiveMonths[i] = month[j];
    j--;
  }
  else{
  previousFiveMonths[i] = month[currentDate.getMonth()-i];
  }
}

const myData = [65, 59, 80, 81, 56]

export const generateMonthlyChart= (templateId) => {
const labels = previousFiveMonths.reverse();
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