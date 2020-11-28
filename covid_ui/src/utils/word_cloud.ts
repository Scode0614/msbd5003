export const genWords = (list) => {
  const word_count_list = list ? list['word'].map((it,index) => {
    return {
      value: list['count'][index],
      text: it
    }
  }) : []

  return word_count_list
}