export const genChart = (topic_counts) => {
    const series_data = topic_counts ? topic_counts.map((it, index) => {
        return {value: it, name: 'topic ' + (index + 1)}
    }) : []
    return {
      tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
          orient: 'vertical',
          left: 10
      },
      series: [
          {
              name: 'Topic Proportion',
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
              data: series_data
          }
      ]
    }
  }