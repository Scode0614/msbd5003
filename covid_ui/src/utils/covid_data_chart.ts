import { random } from "lodash"

export const genMapChart = (format_data_part1) => {
  const country_list = format_data_part1[1]
  var min = 100000
  var max = 0
  const data = country_list.map(it => {
    var value = 0
    var dataList = format_data_part1[2][it]
    if (dataList) {
      dataList.forEach(it => {
        if (!isNaN(it)) {
          value += Number(it)
        }
      })
    }
    if (it != "World" && value < min) min = value
    if (it != "World" && value > max) max = value
    return {
      name: it,
      value: value
    }
  });

  return {
    tooltip: {
        trigger: 'item',
        showDelay: 0,
        transitionDuration: 0.2,
    },
    visualMap: {
        left: 'right',
        min: min,
        max: max,
        inRange: {
            color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        },
        text: ['High', 'Low'],           // 文本，默认为数值文本
        calculable: true
    },
    series: [
        {
            name: 'Covid data',
            type: 'map',
            roam: true,
            map: 'World',
            emphasis: {
                label: {
                    show: true
                }
            },
            data: data
        }
    ]
  }
}

export const genLineChartCompare = (covid_data, filter_regions) => {
  
  const serie_list = Object.keys(covid_data[2]).filter(it => {return filter_regions.includes(it)}).map(it => {
      return {
        name: it,
        type: 'line',
        data: covid_data[2][it]
    }
  })

  return {
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        show: true
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
        data: covid_data[0]
    },
    yAxis: {
        type: 'value'
    },
    series: serie_list
  };

}

export const genPredictLineChartCompare = (covid_data, filter_regions) => {
  
  const data_list = filter_regions.map(it => {
    return {
      name: it + '_real',
      type: 'line',
      data: covid_data[2][it]
    }
  })
  const predict_data_list = filter_regions.map(it => {
    return {
      name: it + '_predict',
      type: 'line',
      data: covid_data[3][it]
    }
  })

  return {
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        show: true
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
        data: covid_data[0]
    },
    yAxis: {
        type: 'value'
    },
    series: data_list.concat(predict_data_list)
  };

}