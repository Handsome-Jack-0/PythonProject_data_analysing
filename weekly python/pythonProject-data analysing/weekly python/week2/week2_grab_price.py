import requests
from bs4 import BeautifulSoup
import csv
import time

# 定义请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 定义 CSV 文件的列名
csv_columns = ['名称', '评分', '评价人数', '导演', '主演', '上映日期', '类型', '简介']
# 定义存储电影信息的列表
movies = []

# 最大重试次数
max_retries = 3
# 请求间隔时间（秒）
request_interval = 2

# 循环处理每一页的数据
for start in range(0, 250, 25):
    # 构造当前页的 URL
    url = f'https://movie.douban.com/top250?start={start}'
    retries = 0
    while retries < max_retries:
        try:
            # 发送 HTTP 请求
            response = requests.get(url, headers=headers)
            # 检查请求是否成功
            response.raise_for_status()
            # 解析 HTML 内容
            soup = BeautifulSoup(response.text, 'html.parser')
            # 找到所有电影项
            items = soup.find_all('div', class_='item')

            # 遍历每个电影项，提取所需信息
            for item in items:
                # 提取电影名称
                title = item.find('span', class_='title').text
                # 提取电影评分
                rating = item.find('span', class_='rating_num').text
                # 提取评价人数
                num_reviews = item.find('div', class_='star').find_all('span')[-1].text.strip('人评价')

                # 提取导演、主演、上映日期、类型
                info = item.find('div', class_='bd').p.text.strip().split('\n')
                director_and_actors = info[0].strip()
                director = director_and_actors.split('导演: ')[1].split('主演: ')[0].strip()
                if '主演: ' in director_and_actors:
                    actors = director_and_actors.split('主演: ')[1].strip()
                else:
                    actors = '暂无主演信息'
                date_and_type = info[1].strip().split('/')
                release_date = date_and_type[0].strip()
                movie_type = date_and_type[-1].strip()

                # 提取电影简介
                quote = item.find('span', class_='inq')
                if quote:
                    quote_text = quote.text
                else:
                    quote_text = '暂无简介'

                # 将提取的信息存储为字典
                movie = {
                    '名称': title,
                    '评分': rating,
                    '评价人数': num_reviews,
                    '导演': director,
                    '主演': actors,
                    '上映日期': release_date,
                    '类型': movie_type,
                    '简介': quote_text
                }
                # 将电影信息添加到列表中
                movies.append(movie)

            # 请求成功，跳出重试循环
            break
        except requests.RequestException as e:
            print(f"请求出错，第 {retries + 1} 次重试: {e}")
            retries += 1
            time.sleep(request_interval)
        except Exception as e:
            print(f"发生未知错误，第 {retries + 1} 次重试: {e}")
            retries += 1
            time.sleep(request_interval)

    if retries == max_retries:
        print(f"达到最大重试次数，跳过页面: {url}")

    # 每次请求完成后等待一段时间，避免请求过于频繁
    time.sleep(request_interval)

# 保存数据到 CSV 文件
csv_file = 'douban_top250_extended.csv'
try:
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        # 写入 CSV 文件的列名
        writer.writeheader()
        # 写入每一行电影信息
        for movie in movies:
            writer.writerow(movie)
    print(f"数据已成功保存到 {csv_file}")
except IOError:
    print("写入 CSV 文件时出错")