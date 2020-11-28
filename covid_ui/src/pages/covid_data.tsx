import React, { useState, useRef } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Tag, Button, Row, Col, DatePicker, Form, Select, Radio, Table } from 'antd';
import styles from './covid_data.less';
import ReactEcharts from 'echarts-for-react'
import { chart_map_data, filtered_list } from "../utils/covid_data_map";
import { genMapChart as covid_map_chart, genLineChartCompare as covid_line_compare_chart , genPredictLineChartCompare as covid_predict_line_compare_chart} from "../utils/covid_data_chart";
import { format_data as format_covid_data, format_predict_data as format_covid_data_predict } from "../utils/covid_data_helper";
import echarts from 'echarts/lib/echarts';

import { getCovidDataInfo } from '@/services/covid_data';

const { RangePicker } = DatePicker;
const { Option } = Select;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 24 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

const onMapSelectionChange = (value) => {
  alert(value.target.value)
}
const onRegionSelectionChange = (value) => {
  alert(value.target.value)
}
const onPredictSelectionChange = (value) => {
  alert(value.target.value)
}

const onFinish = async (values, updateInfo, updateLoading, handlePart2RegionOption) => {
  if (values.regions) {
    handlePart2RegionOption(values.regions)
  }
  updateLoading(true)
  const date_from = values.dates[0].format("YYYY-MM-DD");
  const date_to = values.dates[1].format("YYYY-MM-DD");
  const regions = values.regions ? values.regions.join("|") : ""
  const result = await getCovidDataInfo(date_from, date_to, regions);
  updateInfo(result)
  updateLoading(false)
};

const region_option = filtered_list.map(it => { return [<Option key={it}>{it}</Option>]})
const sir_region_list = ["United States", "China", "India"];
const sir_region_option = sir_region_list.map(it => { return [<Option key={it}>{it}</Option>]})

export default (): React.ReactNode => {

  const [info, updateInfo] = useState<object>({});
  const [loading, updateLoading] = useState<boolean>(false);


  const [mapShowOption, handleMapShowOption] = useState<string>("total_cases");
  const [regionShowOption, handleRegionShowOption] = useState<string>("total_cases");
  const [predictShowOption, handlePredictShowOption] = useState<string>("0");

  const [part2RegionOption, handlePart2RegionOption] = useState<list>([]);
  const [part3RegionOption, handlePart3RegionOption] = useState<list>([]);

  const format_data_part1 = format_covid_data(info['covid_data_list'], mapShowOption)
  const format_data_part2 = format_covid_data(info['covid_data_list'], regionShowOption)
  const format_data_part3 = format_covid_data_predict(info['covid_predict_list'], predictShowOption)

  const regionOptionsPart2 = format_data_part2[1].map(it => { return [<Option key={it}>{it}</Option>]})
  const regionOptionsPart3 = format_data_part3[1].map(it => { return [<Option key={it}>{it}</Option>]})

  echarts.registerMap('World', chart_map_data)
  
  return <PageContainer loading={loading}>
    <Form
      {...layout}
      name="basic"
      initialValues={{
        remember: true,
      }}
      onFinish={(e) => {onFinish(e, updateInfo, updateLoading, handlePart2RegionOption)}}
    >
      <Row>
        <Col span={8}>
          <Form.Item
            label="Dates"
            name="dates"
            
            rules={[
              {
                required: true,
              },
            ]}
          >
            <RangePicker />
          </Form.Item>
        </Col>
        <Col span={10}>
          <Form.Item
            label="Regions"
            name="regions"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Select mode="tags" placeholder="">
              {region_option}
            </Select>
          </Form.Item>
        </Col>
        <Col span={2}>
          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              Search
            </Button>
          </Form.Item>
        </Col>
      </Row>
    </Form>

    <Card className={styles.sectionList}>
      <Row className={styles.section}>
        <Col span={24} style={{height: "100%"}}>
          <Card title="Map" extra={<Radio.Group onChange={(e) => handleMapShowOption(e.target.value)} value={mapShowOption} defaultValue="0" buttonStyle="solid">
                                                      <Radio.Button value="total_cases">Total Cases</Radio.Button>
                                                      <Radio.Button value="new_cases">New Cases</Radio.Button>
                                                      <Radio.Button value="total_deaths">Total Deaths</Radio.Button>
                                                      <Radio.Button value="new_deaths">New Deaths</Radio.Button>
                                                      <Radio.Button value="icu_patients">ICU Patients</Radio.Button>
                                                      <Radio.Button value="hosp_patients">Hosp Patients</Radio.Button>
                                                      <Radio.Button value="total_tests">Total Tests</Radio.Button>
                                                      <Radio.Button value="new_tests">New Tests</Radio.Button>
                                                      <Radio.Button value="positive_rate">Positive Rate</Radio.Button>
                                                    </Radio.Group>}>
            <ReactEcharts
              option={covid_map_chart(format_data_part1)}
              style={{width: '100%', height: '350px'}}
            />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={24} style={{height: "100%"}}>
          <Card title="Chart" extra={<Radio.Group onChange={(e) => handleRegionShowOption(e.target.value)} value={regionShowOption} defaultValue="0" buttonStyle="solid">
                                                      <Radio.Button value="total_cases">Total Cases</Radio.Button>
                                                      <Radio.Button value="new_cases">New Cases</Radio.Button>
                                                      <Radio.Button value="total_deaths">Total Deaths</Radio.Button>
                                                      <Radio.Button value="new_deaths">New Deaths</Radio.Button>
                                                      <Radio.Button value="icu_patients">ICU Patients</Radio.Button>
                                                      <Radio.Button value="hosp_patients">Hosp Patients</Radio.Button>
                                                      <Radio.Button value="total_tests">Total Tests</Radio.Button>
                                                      <Radio.Button value="new_tests">New Tests</Radio.Button>
                                                      <Radio.Button value="positive_rate">Positive Rate</Radio.Button>
                                                    </Radio.Group>}>
            <Select style={{width: '100%'}} onChange={(e) => { handlePart2RegionOption(e)}} value={part2RegionOption} mode="tags" placeholder="">
              {regionOptionsPart2}
            </Select>
            <ReactEcharts
              option={covid_line_compare_chart(format_data_part2, part2RegionOption)}
              style={{width: '100%', height: '350px'}}
            />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={24} style={{height: "100%"}}>
          <Card title="Prediction" extra={<Radio.Group onChange={(e) => handlePredictShowOption(e.target.value)} value={predictShowOption} defaultValue="0" buttonStyle="solid">
                                                      <Radio.Button value="0">Total Cases</Radio.Button>
                                                      <Radio.Button value="1">Total Deaths</Radio.Button>
                                                    </Radio.Group>}>
            <Select style={{width: '100%'}} onChange={(e) => { handlePart3RegionOption(e)}} value={part3RegionOption} mode="tags" placeholder="">
              {regionOptionsPart3}
            </Select>
            <ReactEcharts
              option={covid_predict_line_compare_chart(format_data_part3, part3RegionOption)}
              style={{width: '100%', height: '350px'}}
            />
          </Card>
        </Col>
      </Row>
    </Card>
  </PageContainer>};
