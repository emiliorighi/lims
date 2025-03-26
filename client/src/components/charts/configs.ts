function toDate(dateString: string): Date {
    const [year, month] = dateString.split('-').map(Number);
    return new Date(year, month);
}

export function useDateChart(data: Record<string, number>, label: string, color: string) {
    const submissionDatesByMonth: Record<string, number> = Object.keys(data)
        .filter((key) => key.includes('-'))
        .reduce((acc: Record<string, number>, key: string) => {
            const [year, month] = key.split('-');
            const date = `${year}-${month}`;
            acc[date] = acc[date] ? acc[date] + data[key] : data[key];
            return acc;
        }, {});

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