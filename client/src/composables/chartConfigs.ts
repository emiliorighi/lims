import { defineAsyncComponent } from 'vue';
import { ChartTypes } from '../data/types';


export const colors = [
    '#2c82e0', '#ef476f', '#ffd166', '#06d6a0', '#8338ec', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff',
    '#c9cbcf', '#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#e67e22', '#1abc9c', '#9b59b6', '#34495e', '#95a5a6',
    '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#f39c12', '#d35400', '#2c3e50', '#bdc3c7', '#7f8c8d', '#e74c3c',
    '#2980b9', '#f1c40f', '#2ecc71', '#9b59b6'
];



function toDate(dateString: string): Date {
    const [year, month] = dateString.split('-').map(Number);
    return new Date(year, month);
}

export function useDateChart(data: Record<string, number>, label: string, color: string) {
    const submissionDatesByMonth: Record<string, number> = Object.keys(data)
        .filter((key) => key.includes('-'))
        .reduce((acc: Record<string, number>, key: string) => {
            const [year, month, _report] = key.split('-');
            const date = `${year}-${month}`;
            acc[date] = acc[date] ? acc[date] + data[key] : data[key];
            return acc;
        }, {});
    console.log(submissionDatesByMonth)
    // Sort the dates
    const sortedDates = Object.keys(submissionDatesByMonth)
        .sort((a, b) => toDate(a).getTime() - toDate(b).getTime());

    const datasets = [
        {
            label: label,
            backgroundColor: 'rgba(75,192,192,0.4)',
            data: sortedDates.map((date) => submissionDatesByMonth[date]),
            fill: true,
            pointRadius: 0,
            borderWidth: 2,
            borderColor: color,
        },
    ];

    const options = {
        scales: {
            x: {
                type: 'category',
            },
            y: {
                display: false,
            },
        },
        interaction: {
            intersect: false,
            mode: 'index',
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                enabled: true,
            },
        },
        datasets: {
            line: {
                tension: 0.3,
            },
        },
        maintainAspectRatio: false,
    };
    return { labels: sortedDates, datasets, options }
}


export function processChartData(data: Record<string, number>, label: string) {
    const orderedValues = Object.fromEntries(Object.entries(data).sort(([, v], [, v1]) => v - v1));
    return {
        labels: Object.keys(orderedValues),
        datasets: [
            {
                label,
                backgroundColor: colors,
                data: Object.values(orderedValues),
            },
        ],
    };
}

export function getChartOptions(type: ChartTypes) {
    let legend
    let datalabels = {
        color: '#000000',
        display: 'auto',
        font: {
            size: 14,
        }
    }
    let scales
    if (type === 'pie' || type == 'doughnut') {
        legend = {
            position: 'bottom',
            labels: {
                font: {
                    color: '#34495e',
                    family: 'sans-serif',
                    size: 14,
                },
                usePointStyle: true,
            },
        }
    }
    else {
        legend = {
            display: false
        }
        scales = {
            y: { type: 'category' },
            x: { display: false },
        }
    }
    return {
        scales,
        plugins: {
            legend,
            datalabels,
        },
        datasets: {
            bar: {
                borderColor: 'transparent',
            },
        },
        maintainAspectRatio: false,
    };
}


export const chartTypesMap = {
    pie: defineAsyncComponent(() => import('../components/charts/PieChart.vue')),
    doughnut: defineAsyncComponent(() => import('../components/charts/DoughnutChart.vue')),
    bubble: defineAsyncComponent(() => import('../components/charts/BubbleChart.vue')),
    line: defineAsyncComponent(() => import('../components/charts/LineChart.vue')),
    bar: defineAsyncComponent(() => import('../components/charts/BarChart.vue')),
    'horizontal-bar': defineAsyncComponent(() => import('../components/charts/HorizontalBarChart.vue')),
}
