import { request } from 'umi';

export async function getSentimentInfo(date_from: string, date_to: string, keywords: string) {
  return request(`/api/sentiment_analysis/info?date_from=${date_from}&date_to=${date_to}&keywords=${keywords}`);
}
