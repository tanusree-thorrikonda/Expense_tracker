document.addEventListener("DOMContentLoaded", function () {

    createCategoryExpenseChart();

    createMonthlyTransactionChart();

});


function readChartData(elementId) {

    const dataElement = document.getElementById(elementId);


    if (!dataElement) {

        return null;

    }


    try {

        return JSON.parse(
            dataElement.textContent
        );

    } catch (error) {

        console.error(
            `Could not parse chart data: ${elementId}`,
            error
        );

        return null;

    }

}



function createCategoryExpenseChart() {

    const canvas = document.getElementById(
        "categoryExpenseChart"
    );


    if (!canvas) {

        return;

    }


    const chartData = readChartData(
        "expense-chart-data"
    );


    if (!chartData) {

        return;

    }


    new Chart(canvas, {

        type: "doughnut",


        data: {

            labels: chartData.labels,


            datasets: [

                {

                    label: "Expenses",

                    data: chartData.values

                }

            ]

        },


        options: {

            responsive: true,

            maintainAspectRatio: false,


            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}



function createMonthlyTransactionChart() {

    const canvas = document.getElementById(
        "monthlyTransactionChart"
    );


    if (!canvas) {

        return;

    }


    const chartData = readChartData(
        "monthly-chart-data"
    );


    if (!chartData) {

        return;

    }


    new Chart(canvas, {

        type: "bar",


        data: {

            labels: chartData.labels,


            datasets: [

                {

                    label: "Income",

                    data: chartData.income

                },


                {

                    label: "Expenses",

                    data: chartData.expenses

                }

            ]

        },


        options: {

            responsive: true,

            maintainAspectRatio: false,


            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

}