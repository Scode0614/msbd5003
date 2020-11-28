import React from 'react';
import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-layout';

export default () => (
  <DefaultFooter
    copyright="2020"
    links={[
      {
        key: 'Covid-19 Public Opinion Analysis',
        title: 'Covid-19 Public Opinion Analysis',
        href: '',
        blankTarget: true,
      }
    ]}
  />
);
