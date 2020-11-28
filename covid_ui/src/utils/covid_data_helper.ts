export const format_data = (covid_data, key) => {
  const date_list_ = covid_data && covid_data['date'] ? covid_data['date'].map(it => {return new Date(it).toLocaleDateString()}) : []
  const location_list_ = covid_data && covid_data['location'] ? covid_data['location'] : []
  const data_list_ = covid_data && covid_data[key] ? covid_data[key] : []

  var date_list = []
  var region_list = []
  var data_list = {}


  date_list_.forEach((it, index) => {
    if (!date_list.includes(it)) {
      date_list.push(it)
    }
    var region = location_list_[index]
    if (!region_list.includes(region)) {
      region_list.push(region)
    }
    var data = data_list_[index]
    if (data_list[region]) {
      data_list[region].push(data)
    } else {
      data_list[region] = [data]
    }
  })

  return [date_list, region_list, data_list]
}

export const format_predict_data = (covid_data, key) => {
  const date_list_ = covid_data && covid_data['date'] ? covid_data['date'].map(it => {return new Date(it).toLocaleDateString()}) : []
  const location_list_ = covid_data && covid_data['location'] ? covid_data['location'] : []

  var data_key = key == "0" ? "real_cases" : "real_deaths"
  var predict_data_key = key == "0" ? "predicted_cases" : "predicted_deaths"
  const data_list_ = covid_data && covid_data[data_key] ? covid_data[data_key] : []
  const predict_data_list_ = covid_data && covid_data[predict_data_key] ? covid_data[predict_data_key] : []

  var date_list = []
  var region_list = []
  var data_list = {}
  var predict_data_list = {}

  date_list_.forEach((it, index) => {
    if (!date_list.includes(it)) {
      date_list.push(it)
    }
    var region = location_list_[index]
    if (!region_list.includes(region)) {
      region_list.push(region)
    }
    var data = data_list_[index]
    if (data_list[region]) {
      data_list[region].push(data)
    } else {
      data_list[region] = [data]
    }
    var data_ = predict_data_list_[index]
    if (predict_data_list[region]) {
      predict_data_list[region].push(data_)
    } else {
      predict_data_list[region] = [data_]
    }
  })

  return [date_list, region_list, data_list, predict_data_list]
}