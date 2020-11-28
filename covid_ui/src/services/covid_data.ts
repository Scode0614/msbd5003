import { request } from 'umi';

export async function getCovidDataInfo(date_from: string, date_to: string, regions: string) {
  return request(`/api/covid_data/info?date_from=${date_from}&date_to=${date_to}&regions=${regions}`);
}
