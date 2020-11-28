export const genChart = (sentiment_counts) => {
  const pos = sentiment_counts ? sentiment_counts.pos : 0
  const neg = sentiment_counts ? sentiment_counts.neg : 0
  const neu = sentiment_counts ? sentiment_counts.neu : 0
  return {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 10,
        data: ['positive', 'negative', 'natural']
    },
    series: [
        {
            name: 'Sentiment Proportion',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: true
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '30',
                    fontWeight: 'bold'
                }
            },
            data: [
                {value: pos, name: 'positive'},
                {value: neg, name: 'negative'},
                {value: neu, name: 'natural'},
            ]
        }
    ]
  }
}