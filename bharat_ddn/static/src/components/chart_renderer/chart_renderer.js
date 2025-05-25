// import { loadJS } from "@web/core/assets";
// import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";  // Corrected import for `useRef`
// import { loadJS } from "@web/core/assets";

// export class ChartRenderer extends Component {
//     static components = {};  // No `KpiCard` here as it's not defined in the snippet you provided.

//     setup() {
//         // Reference to the chart element
//         this.chartRef = useRef("chart");

//         // Load Chart.js library on component startup
//         onWillStart(async () => {
//             await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");
//         });

//         // Initialize the chart after the component is mounted
//         onMounted(() => this.renderChart());
//     }

//     renderChart() {
//         // Ensure Chart.js is available before using it
//         if (typeof Chart !== 'undefined') {
//             new Chart(
//                 this.chartRef.el,
//                 {
//                     type: 'doughnut',
//                     data: {
//                         labels: ['Red', 'Blue', 'Yellow'],
//                         datasets: [
//                             {
//                                 label: 'My First Dataset',
//                                 data: [300, 50, 100],
//                                 backgroundColor: [
//                                     'rgb(255, 99, 132)',
//                                     'rgb(54, 162, 235)',
//                                     'rgb(255, 205, 86)'
//                                 ],
//                                 hoverOffset: 4
//                             },
//                             {
//                                 label: 'My Second Dataset',
//                                 data: [300, 70, 160],
//                                 backgroundColor: [
//                                     'red',
//                                     'green',
//                                     'orange'
//                                 ],
//                                 hoverOffset: 4
//                             }
//                         ]
//                     },
//                     options: {
//                         responsive: true,
//                         plugins: {
//                             legend: {
//                                 position: 'bottom'
//                             },
//                             title: {
//                                 display: true,
//                                 text: 'Chart.js Doughnut Chart',
//                                 position: 'bottom'
//                             }
//                         }
//                     },
//                 }
//             );
//         } else {
//             console.error("Chart.js is not loaded.");
//         }
//     }
// }

// // Define the template for the component
// ChartRenderer.template = 'ddn.ChartRenderer';


import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";  // Corrected import for `useRef`

export class ChartRenderer extends Component {
    static components = {};  // No `KpiCard` here as it's not defined in the snippet you provided.

    setup() {
        // Reference to the chart element
        this.chartRef = useRef("chart");

        // Load Chart.js library on component startup
        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");
        });

        // Initialize the chart after the component is mounted
        onMounted(() => this.renderChart());
    }

    renderChart() {
        // Ensure Chart.js is available before using it
        if (typeof Chart !== 'undefined') {
            new Chart(
                this.chartRef.el,
                {
                    type: this.props.type,
                    data: {
                        labels: ['Red', 'Blue', 'Yellow'],
                        datasets: [
                            {
                                label: 'My First Dataset',
                                data: [300, 50, 100],
                                
                                hoverOffset: 4
                            },
                            {
                                label: 'My Second Dataset',
                                data: [300, 70, 160],
                                backgroundColor: [
                                    'red',
                                    'green',
                                    'orange'
                                ],
                                hoverOffset: 4
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            },
                            title: {
                                display: true,
                                text: this.props.title,
                                position: 'bottom'
                            }
                        }
                    },
                }
            );
        } else {
            console.error("Chart.js is not loaded.");
        }
    }
}

// Define the template for the component
ChartRenderer.template = 'ddn.ChartRenderer';
