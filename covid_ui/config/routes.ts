export default [
  {
    path: '/topics',
    name: 'Hot Topics',
    icon: 'aim',
    component: './topics',
  },
  {
    path: '/sentiment',
    name: 'Sentiment Analysis',
    icon: 'smile',
    component: './sentiment',
  },
  {
    path: '/covid_data',
    name: 'Covid Data',
    icon: 'fund',
    component: './covid_data',
  },
  {
    path: '/',
    redirect: '/topics',
  },
  {
    component: './404',
  },
];
