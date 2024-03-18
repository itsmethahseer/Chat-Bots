# import main
import bs4

def beatifulsoup_extract_all(response_content):
    soup = bs4.BeautifulSoup(response_content, 'lxml')
    text = soup.find_all(text=True)
    
    # Remove unwanted elements
    cleaned_text = 'hello <html> world </html> <head> daaa </head>'
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',]
    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)   
            
    print(cleaned_text)
    
    
response_content = {'https://website.understandingdata.com/': '<!doctype html>\n<html data-adblockkey="MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANDrp2lz7AOmADaN8tA50LsWcjLFyQFcb/P2Txc58oYOeILb3vBw7J6f4pamkAQVSQuqYsKx3YzdUHCvbVZvFUsCAwEAAQ==_VCE5pIu+FD6Pv9hc9RhnQLHMfVQyLZPqeFE1c2o/crivHpjG987EyBdGEVgQr2VlrXDEesH0laF2MXqA6R/rLg==" lang="en" style="background: #2B2B2B;">\n<head>\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <link rel="icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC">\n    <link rel="preconnect" href="https://www.google.com" crossorigin>\n</head>\n<body>\n<div id="target" style="opacity: 0"></div>\n<script>window.park = "eyJ1dWlkIjoiMjIwM2IxMWItOGUzNS00OWFhLTgwMTMtZDQxOTJkN2VkMTA1IiwicGFnZV90aW1lIjoxNzA4NDkyMjEzLCJwYWdlX3VybCI6Imh0dHBzOi8vc2VtcGlvbmVlci5jb20vIiwicGFnZV9tZXRob2QiOiJHRVQiLCJwYWdlX3JlcXVlc3QiOnt9LCJwYWdlX2hlYWRlcnMiOnt9LCJob3N0Ijoic2VtcGlvbmVlci5jb20iLCJpcCI6IjEwMy4yMTQuMjMzLjIxIn0K";</script>\n<script src="/bzVHBITvv.js"></script>\n</body>\n</html>\n', 'https://sempioneer.com/': '<!doctype html>\n<html data-adblockkey="MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANDrp2lz7AOmADaN8tA50LsWcjLFyQFcb/P2Txc58oYOeILb3vBw7J6f4pamkAQVSQuqYsKx3YzdUHCvbVZvFUsCAwEAAQ==_VCE5pIu+FD6Pv9hc9RhnQLHMfVQyLZPqeFE1c2o/crivHpjG987EyBdGEVgQr2VlrXDEesH0laF2MXqA6R/rLg==" lang="en" style="background: #2B2B2B;">\n<head>\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <link rel="icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC">\n    <link rel="preconnect" href="https://www.google.com" crossorigin>\n</head>\n<body>\n<div id="target" style="opacity: 0"></div>\n<script>window.park = "eyJ1dWlkIjoiYzJkMjJiZGEtYzYwYi00NTNjLTk4YWUtYTQxZDc3ODJmNDBmIiwicGFnZV90aW1lIjoxNzA4NDkyMjE0LCJwYWdlX3VybCI6Imh0dHBzOi8vc2VtcGlvbmVlci5jb20vIiwicGFnZV9tZXRob2QiOiJHRVQiLCJwYWdlX3JlcXVlc3QiOnt9LCJwYWdlX2hlYWRlcnMiOnt9LCJob3N0Ijoic2VtcGlvbmVlci5jb20iLCJpcCI6IjEyMi4xNjYuNjUuNDkifQo=";</script>\n<script src="/bQnFdEpTr.js"></script>\n</body>\n</html>\n'}
beatifulsoup_extract_all(response_content)