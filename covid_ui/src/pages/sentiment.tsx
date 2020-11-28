import React, { useState, useRef } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Tag, Button, Row, Col, DatePicker, Form, Select, Radio, Table } from 'antd';
import styles from './sentiment.less';
import ReactEcharts from 'echarts-for-react'
import { genChart as gen_sentiment_pie_chart } from "../utils/sentiment_pie_chart";
import { genChart as gen_sentiment_line_chart } from "../utils/sentiment_line_chart";
import { genWords as gen_topic_word_cloud } from "../utils/word_cloud";
import ReactWordcloud from 'react-wordcloud';

import { getSentimentInfo } from '@/services/sentiment_analysis';

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
  const result = await getSentimentInfo(date_from, date_to, keywords);
  updateInfo(result)
  updateLoading(false)
};

export default (): React.ReactNode => {
  
  const [sentimentTweetOption, handleSentimentTweetOption] = useState<string>("0");
  const [info, updateInfo] = useState<object>({});
  const [loading, updateLoading] = useState<boolean>(false);


  const key_words = ['mask', 'vaccine', 'pandemic', 'social distancing', 'quarantine', 'epidemic', 'ventilator']
  const keyWordsOptions = key_words.map(it => { return [<Option key={it}>{it}</Option>]})

  // Top Sentiment Word
  const topSentimentWordList = info['top_sentiment_words']

  const posTopSentimentWordList = topSentimentWordList ? topSentimentWordList['pos']['word'].map((it,index) => {
    return <Tag className={styles.topicItem} color="#334553"><strong>{topSentimentWordList['pos']['count'][index]}</strong>{it}</Tag>}) : []
  
  const negTopSentimentWordList = topSentimentWordList ? topSentimentWordList['neg']['word'].map((it,index) => {
    return <Tag className={styles.topicItem} color="#334553"><strong>{topSentimentWordList['neg']['count'][index]}</strong>{it}</Tag>}) : []

  const topSentimentTweets = info['top_sentiment_tweets']
  const topSentimentTweetsPOS = topSentimentTweets ? topSentimentTweets['pos']['text'].map((it, index) => {
    return {
      date: topSentimentTweets['pos']['date'][index],
      text:it,
      score: topSentimentTweets['pos']['score'][index]
    }
  }) : []
  const topSentimentTweetsNEG = topSentimentTweets ? topSentimentTweets['neg']['text'].map((it, index) => {
    return {
      date: topSentimentTweets['neg']['date'][index],
      text:it,
      score: topSentimentTweets['neg']['score'][index]
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
        <Col span={8}>
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
          <Card title="Top Positive Words" style={{height: "200px", overflow: 'scroll'}}>
            {posTopSentimentWordList}
          </Card>
          <Card title="Top Negative Words" style={{height: "200px", overflow: 'scroll'}}>
            {negTopSentimentWordList}
          </Card>
        </Col>
        <Col span={14} style={{height: "100%"}}>
          <Card>
            <ReactEcharts
              option={gen_sentiment_pie_chart(info.sentiment_counts)}
              style={{width: '100%', height: '350px'}}
            />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={12}>
          <Card title="Word Cloud Positive Tweets" style={{height: '450px'}}>
            <ReactWordcloud words={gen_topic_word_cloud(topSentimentWordList ? topSentimentWordList['pos'] : null)} size={[500, 400]}/>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Word Cloud Negative Tweets" style={{height: '450px'}}>
            <ReactWordcloud words={gen_topic_word_cloud(topSentimentWordList ? topSentimentWordList['neg'] : null)} size={[500, 400]}/>
          </Card>
        </Col>
      </Row>

      <Row className={styles.section}>
        <Col span={24}>
          <Card title="Sentiment Changes by Dates">
            <ReactEcharts
              option={gen_sentiment_line_chart(info.sentiment_daily_counts)}
              style={{width: '100%', height: '300px'}}
            />
          </Card>
        </Col>
      </Row>
      <Row className={styles.section}>
        <Col span={24}>
          <Card title="Key Sentiment Tweets" extra={<Radio.Group onChange={(e) => handleSentimentTweetOption(e.target.value)} value={sentimentTweetOption} defaultValue="0" buttonStyle="solid">
                                                      <Radio.Button value="0">Top 100 Positive</Radio.Button>
                                                      <Radio.Button value="1">Top 100 Negative</Radio.Button>
                                                    </Radio.Group>}>
            <Table 
              bordered={true}
              size="small"
              style={{width: '100%'}}
              pagination={{pageSize:10}}
              columns={[{
                title: 'Sentiment Score',
                dataIndex: 'score',
                width: 100,
              },
              {
                title: 'Date',
                dataIndex: 'date',
                width: 100,
              },
              {
                title: 'Tweet',
                dataIndex: 'text',
                width: 500,
              },]}
              dataSource={sentimentTweetOption == "0" ? topSentimentTweetsPOS : topSentimentTweetsNEG}
            />
          </Card>
        </Col>
      </Row>
    </Card>
    
    
  </PageContainer>
};
