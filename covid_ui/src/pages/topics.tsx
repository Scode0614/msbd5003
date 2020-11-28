import React, { useState, useRef } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Tag, Button, Row, Col, DatePicker, Form, Select, Input, Table } from 'antd';
import styles from './topics.less';
import ReactEcharts from 'echarts-for-react'
import { genChart as gen_topic_pie_chart } from "../utils/topic_pie_chart";
import { genChart as gen_topic_line_chart } from "../utils/topic_line_chart";
import { genWords as gen_topic_word_cloud } from "../utils/word_cloud";
import ReactWordcloud from 'react-wordcloud';
import { getTopicInfo } from '@/services/topic';

const { RangePicker } = DatePicker;
const { Option } = Select;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 24 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

const onFinish = async (values, updateInfo, updateLoading) => {
  updateLoading(true)
  const date_from = values.dates[0].format("YYYY-MM-DD");
  const date_to = values.dates[1].format("YYYY-MM-DD");
  const keywords = values.keywords ? values.keywords.join("|") : ""
  const similar_sentence = values.similar_sentence
  const result = await getTopicInfo(date_from, date_to, keywords, similar_sentence);
  updateInfo(result)
  updateLoading(false)
};

const key_words = ['mask', 'vaccine', 'pandemic', 'social distancing', 'quarantine', 'epidemic', 'ventilator']
const keyWordsOptions = key_words.map(it => { return [<Option key={it}>{it}</Option>]})

export default (): React.ReactNode => {

  const [topicNumPart1, handleTopicNumPart1] = useState<int>(0);


  const [info, updateInfo] = useState<object>({});
  const [loading, updateLoading] = useState<boolean>(false);

  const topic_selection_options = Array.from(Array(10).keys()).map(it => {
    return <Option value={it}>Topic {it+1}</Option>
  })

  const topic_key_words = info && info.topic_keywords ? {
    'word': info.topic_keywords[topicNumPart1][1].map(it => {return it[1]}),
    'count': info.topic_keywords[topicNumPart1][1].map(it => {return it[0]})} : null

  const similarTweets = info && info.similar_tweets ? info.similar_tweets['text'].map((it, index) => {return {'tweet': it, 'score': info.similar_tweets['score'][index]}}) : []

  const topic_tweets = info && info.topic_distribution ? info.topic_distribution[topicNumPart1].text.map((it, index) => {
    return {
      'contribution': info.topic_distribution[topicNumPart1]['score'][index],
      'date': info.topic_distribution[topicNumPart1]['date'][index],
      'tweet': it
    }
  }) : []

  return <PageContainer loading={loading}>
    <Form
      {...layout}
      name="basic"
      initialValues={{
        remember: true,
      }}
      onFinish={(e) => {onFinish(e, updateInfo, updateLoading)}}
    >
      <Row>
        <Col span={10}>
          <Form.Item
            label="Tweet Dates"
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
            label="Key Words"
            name="keywords"
          >
            <Select mode="tags" placeholder="">
              {keyWordsOptions}
            </Select>
          </Form.Item>
        </Col>
        <Col span={10}>
          <Form.Item
            label=""
            name="similar_sentence"
          >
            <Input placeholder="relative sentence search"/>
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
        <Col span={10} style={{height: "100%"}}>
          <Card title="Hot Topics Top 10" style={{height: "400px"}} 
            extra={<Select onChange={(e) => handleTopicNumPart1(e)} value={topicNumPart1} defaultValue="0" style={{ width: 120 }}>
                    {topic_selection_options}
                   </Select>}>
            
            <ReactWordcloud words={gen_topic_word_cloud(topic_key_words)} />
          </Card>
        </Col>
        <Col span={14} style={{height: "100%"}}>
          <Card>
            <ReactEcharts
              option={gen_topic_pie_chart(info.topic_counts)}
              style={{width: '100%', height: '350px'}}
            />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={24}>
          <Card title="Word Cloud" style={{height: '450px'}}>
            <ReactWordcloud words={gen_topic_word_cloud(info.top_words ? info.top_words : null)} />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={24}>
          <Card title="Topic Tweets">
          < Table 
              bordered={true}
              size="small"
              style={{width: '100%'}}
              pagination={{pageSize:10}}
              columns={[{
                title: 'Contribution',
                dataIndex: 'contribution',
                width: 100,
              },
              {
                title: 'Date',
                dataIndex: 'date',
                width: 100,
              },
              {
                title: 'Tweet',
                dataIndex: 'tweet',
                width: 500,
              },]}
              dataSource={topic_tweets}
            />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={24}>
          <Card title="Similar Tweets">
          < Table 
              bordered={true}
              size="small"
              style={{width: '100%'}}
              pagination={{pageSize:10}}
              columns={[{
                title: 'Score',
                dataIndex: 'score',
                width: 100,
              },
              {
                title: 'Tweet',
                dataIndex: 'tweet',
                width: 500,
              },]}
              dataSource={similarTweets}
            />
          </Card>
        </Col>
      </Row>
    </Card>
    
    
  </PageContainer>
};