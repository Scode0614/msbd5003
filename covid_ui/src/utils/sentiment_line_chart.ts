export const genChart = (sentiment_daily_counts) => {
  const dates = sentiment_daily_counts ? sentiment_daily_counts.neg.date : []
  const neg = sentiment_daily_counts ? sentiment_daily_counts.neg.count : []
  const pos = sentiment_daily_counts ? sentiment_daily_counts.pos.count : []
  const neu = sentiment_daily_counts ? sentiment_daily_counts.neu.count : []
  return {
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['positive', 'negative', 'natural']
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
        data: dates
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: 'positive',
            type: 'line',
            data: pos
        },
        {
            name: 'negative',
            type: 'line',
            data: neg
        },
        {
            name: 'natural',
            type: 'line',
            data: neu
        }
    ]
};

}