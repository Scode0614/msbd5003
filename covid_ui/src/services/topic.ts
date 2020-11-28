import { request } from 'umi';

export async function getTopicInfo(date_from: string, date_to: string, keywords: string, similar_sentence: string) {
  return request(`/api/topic/info?date_from=${date_from}&date_to=${date_to}&keywords=${keywords}&similar_sentence=${similar_sentence}`);
}
