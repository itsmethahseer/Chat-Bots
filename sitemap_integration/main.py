import requests

urls = ['https://website.understandingdata.com/',
      'https://sempioneer.com/']

data = {}

for url in urls:
    # 1. Obtain the response:
    response = requests.get("https://sempioneer.com", verify=False)
    
    # 2. If the response content is 200 - Status Ok, Save The HTML Content:
    if response.status_code == 200:
        data[url] = response.text
        print("data extracted successfully")
    else:
        print("some error occured")
        
print(data)