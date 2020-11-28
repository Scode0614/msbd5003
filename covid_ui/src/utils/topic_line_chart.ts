export const genChart = () => {
  return {
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['mask', 'vaccine']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: 'mask',
            type: 'line',
            data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
            name: 'vaccine',
            type: 'line',
            data: [220, 182, 191, 234, 290, 330, 310]
        }
    ]
};

}