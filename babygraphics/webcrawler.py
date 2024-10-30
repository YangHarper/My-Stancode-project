"""
File: webcrawler.py
Name: Harper
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10905209
Female Number: 7949058
---------------------------
2000s
Male Number: 12979118
Female Number: 9210073
---------------------------
1990s
Male Number: 14146775
Female Number: 10644698
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html)

        # ----- Write your code below this line ----- #
        male_sum = 0
        female_sum = 0

        table_body = soup.find('tbody')     # 找到<tbody>
        if table_body:
            rows = table_body.find_all('tr')    # 找到所有<tr>標籤
        for row in rows:
            tags = row.find_all('td')   # 找到所有<td>標籤
            # 檢查 tags 是否含足夠元素，即該行 (<tr>) 中是否有 5個<td> 標籤，才嘗試訪問。
            if len(tags) >= 5:
                try:    # 當遇到int()轉換過程無法轉換為數字的情況時，直接跳過
                    # 提取代表男生和女生數字的<td>，去掉逗號並轉成整數
                    male_count = int(tags[2].get_text(strip=True).replace(',', ''))
                    female_count = int(tags[4].get_text(strip=True).replace(',', ''))

                    # 計算男生和女生的總和
                    male_sum += male_count
                    female_sum += female_count
                except ValueError:
                    # 某些單元格不含數字，跳過這行
                    continue

        print(f"Male Number: {male_sum}")
        print(f"Female Number: {female_sum}")


if __name__ == '__main__':
    main()
