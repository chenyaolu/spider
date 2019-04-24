import requests
from bs4 import BeautifulSoup
import pymongo
import csv

client = pymongo.MongoClient('localhost', 27017)
shixiseng = client['shixiseng']
intern_info = shixiseng['intern_info']
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
headers = {
    'User-Agent': User_Agent,
}
url = 'https://www.shixiseng.com'
#urls = 'https://www.shixiseng.com/interns/c-310100_?k=&p={}'.format(str(i))
#https://www.shixiseng.com/interns/c-310100_st-company_?k={}&p={}   搜公司
#https://www.shixiseng.com/interns/c-310100_st-intern_?k={}&p={}   搜职位
intern_data = []
company_data = []
position_data = []
def get_item_url(urls):
    joburl = []
    wb_data = requests.get(urls, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('div.info1 a.position-name')
    #print(links)
    for link in links:
        item_url = url + link.get('href')
        joburl.append(item_url)
    #print(joburl)
    return joburl

def get_item_info(item_url,data):
    wb_data = requests.get(item_url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    company = soup.select('div.job-com div.com-name')
    #print(company[0].get_text())
    acad = soup.select('div.job_msg span.job_academic')
    #print(acad[0].get_text())
    position = soup.select('div.new_job_name')
    #print(position[0].get_text().strip())
    requirement = soup.select('div.job_detail')
    renew = ' '.join(requirement[0].text.split())
    #print(renew)
    job_data = {
        '公司':company[0].get_text(),
        '职位': position[0].get_text().strip(),
        '学历':acad[0].get_text(),
        '要求':renew,
        '链接':item_url
    }
    data.append(job_data)
    print(job_data)
'''
    intern_info.insert_one({
        '公司':company[0].get_text(),
        '职位': position[0].get_text().strip(),
        '学历':acad[0].get_text(),
        '要求':renew,
        '链接':item_url
    })
'''
#全局搜索
def job_info():
    for i in range(1,30):
        urls = 'https://www.shixiseng.com/interns/c-310100_?k=&p={}'.format(str(i))
        joburl = get_item_url(urls)
        for item_url in joburl:
            get_item_info(item_url,intern_data)
    with open('intern_info.csv','w',newline='',encoding='utf-8-sig') as f:
        header = ['公司', '职位', '学历', '要求', '链接']
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for value in intern_data:
            writer.writerow(value)

#搜公司
def search_company():
    keywords = input("Enter your keywords: ")
    for i in range(1,30):
        urls = 'https://www.shixiseng.com/interns/c-310100_st-company_?k={}&p={}'.format(str(keywords),str(i))
        joburl = get_item_url(urls)
        for item_url in joburl:
            get_item_info(item_url,company_data)
    with open('intern_info_company.csv','w',newline='',encoding='utf-8-sig') as f:
        header = ['公司', '职位', '学历', '要求', '链接']
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for value in company_data:
            writer.writerow(value)

#搜职位
def search_position():
    keywords = input("Enter your keywords: ")
    for i in range(1,30):
        urls = 'https://www.shixiseng.com/interns/c-310100_st-intern_?k={}&p={}'.format(str(keywords),str(i))
        joburl = get_item_url(urls)
        for item_url in joburl:
            get_item_info(item_url,position_data)
    with open('intern_info_position.csv','w',newline='',encoding='utf-8-sig') as f:
        header = ['公司', '职位', '学历', '要求', '链接']
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for value in position_data:
            writer.writerow(value)

if __name__ == '__main__':
    #job_info()
    search_company()
    #search_position()


#get_item_url('https://www.shixiseng.com/interns/c-310100_?k=&p=1')
#get_item_info("https://www.shixiseng.com/intern/inn_snjesmhmqxvd")