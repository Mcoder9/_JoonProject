import requests,json,csv
from  bs4 import BeautifulSoup
import httpx
s = requests.Session()

def get_xfToken(url):
    kk = s.get(url)
    soup = BeautifulSoup(kk.text,'lxml')
    _xfToken = soup.select_one('[name="_xfToken"]')['value']
    return _xfToken
xfToken = get_xfToken('http://joonbud.com/login/login')

def postReview(professorURI,comment,rattings):
    professorRateURL = 'http://joonbud.com' +professorURI+ 'rate'
    _xfToken = get_xfToken(professorRateURL)
    print(_xfToken)
    ratePayload = {
        '_xfToken':_xfToken,
        'rating':rattings,
        'message':comment,
        '_xfRequestUri':professorURI+'rate',
        '_xfWithData':1,
        '_xfResponseType':'json',
        '_xfToken':_xfToken
    }
    reatres = s.post(professorRateURL,data=ratePayload) # post comment/Reviews
    print('post::',reatres)

def login(student_id,student_pass):                 
    loginUrl = 'http://joonbud.com/login/login'
    payload = {
        '_xfToken':'1664711433,06f3d7f969a7ae7a1a21404b3d44d070',
        'login':student_id,
        'password':student_pass,
        'remember':1,
        '_xfRedirect':'http://joonbud.com/'
    }
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        'Cookie': 'xf_session=u2Kjan-hTh1IGHZFodKpWY0-602RJIoD; xf_csrf=FKYM1VKsK-EVPGis',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection':'keep-alive'
    }
    cookies = {'xf_user': '58%2C6PA1cUAPE5c41WdfshPFcfh46eYPkeO8qO4PZt7M',
                'xf_session':'nJmBrPow2LhS1-zghlJy55EKnOXi-mYU',
                'path=/;' : 'HttpOnly'
                }
    res = s.post(loginUrl,data=payload,headers=headers)
    print('login::',res)

def QuerySearch(query):
    xfToken = get_xfToken('http://joonbud.com/professors/categories/saddleback-college.2/')
    print(xfToken)
    payload = {'title':query,'_xfToken':xfToken}

    quickSearch = s.post('http://joonbud.com/resources/categories/quicksearch?category_id=2',data=payload)
    print(quickSearch)
    soup = BeautifulSoup(quickSearch.text,'lxml')
    queryResults = soup.select('td[class="dataList-cell dataList-cell--link"]>a')
    for tag in queryResults:
        if query == tag.text:
            return tag['href']

def runRattingBot():
    for row in open('std_accounts.txt',).readlines():
        student_id = row.split(':')[0],
        student_pass = row.split(':')[1],
        comment = 'selfcoder like it'
        rattings = 5
        query = '. Reyes HIST17'
        login(student_id,student_pass)
        professorURI = QuerySearch(query)
        if professorURI:
            print(professorURI)
            postReview(professorURI,comment,rattings)
        else:
            print('Professor URI not found')


runRattingBot()

