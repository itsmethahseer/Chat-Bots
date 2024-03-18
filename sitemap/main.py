from bs4 import BeautifulSoup
import requests

url = 'https://www.javatpoint.com/automl-workflow'
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)

# Find all <a> tags with class="link"
lists = ['a','div','tr','td','table','iframe','p','h1','h2','h3','h4','h5','h6','ol','tbody']
classes = ['leftmenu','header','headermobile','mobilemenu','leftmenu2','onlycontent','onlycontentad','onlycontentinner','next','h1','h2','points','codeblock','h3','codeblock3','nexttopicdiv']
for i in lists:
    for j in classes:
        links = soup.find_all(i, class_=j)
        for link in links:
            print(link.text)
# print(links)
# Extract and print the href attribute and text of each link