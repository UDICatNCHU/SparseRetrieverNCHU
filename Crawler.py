from bs4 import BeautifulSoup
import requests

url = "https://web.tari.gov.tw/techcd/稻作/水稻/病害/水稻-稻熱病.htm"
# url = "https://web.tari.gov.tw/techcd/%E7%A8%BB%E4%BD%9C/%E6%B0%B4%E7%A8%BB/%E7%97%85%E5%AE%B3/%E6%B0%B4%E7%A8%BB-%E6%B0%B4%E7%A8%BB%E5%BE%92%E9%95%B7%E7%97%85.htm"

response = requests.get(url)
html_content = response.content.decode('big5')

soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.find_all('table', {'class': 'MsoNormalTable'})

table_contents = []
# for i, table in enumerate(tables):    
#     table_content = table.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
#     print('table', i)
#     print(table_content)


ps = soup.find_all('p', {'class': 'MsoNormal'})
for i, p in enumerate(ps):
    p_content = p.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
    # print('p', i)
    # print(p_content)    

    # Check if p is followed by a table
    if p.find_next_sibling('table', {'class': 'MsoNormalTable'}):
        print('p', i)
        print(p_content)
        table = p.find_next_sibling('table', {'class': 'MsoNormalTable'})
        
        # table_content = table.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
        # print('table', i)
        # print(table_content)

        table_dict = {}
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 2:
                key = columns[0].get_text().replace('\n', '').replace('\r', '').replace('\t', '')   
                value = columns[1].get_text().replace('\n', '').replace('\r', '').replace('\t', '')
                table_dict[key] = value

        print(table_dict)
                
                
        # table_content = table.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
                
