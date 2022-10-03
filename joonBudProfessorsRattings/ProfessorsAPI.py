import requests,json,csv
from  bs4 import BeautifulSoup
import httpx
s = requests.Session()

def get_xfToken(url):
    kk = s.get(url)
    soup = BeautifulSoup(kk.text,'lxml')
    _xfToken = soup.select_one('[name="_xfToken"]')['value']
    return _xfToken

def postReview(professorURI,comment,rattings):
    professorRateURL = 'http://joonbud.com' +professorURI+ 'rate'
    _xfToken = get_xfToken(professorRateURL)
    ratePayload = {
        '_xfToken':_xfToken,
        'rating':rattings,
        'message':comment,
        '_xfRequestUri':professorURI+'rate',
        '_xfWithData':1,
        '_xfResponseType':'json',
        '_xfToken':_xfToken
    }
    rateResp = s.post(professorRateURL,data=ratePayload) # post comment/Reviews
    if rateResp.status_code == 200:
        print(f'{rattings} start ratting posted --> statusCode {rateResp.status_code}')
        print(f'Posted:: {comment[:30]}....')

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
    res = s.post(loginUrl,data=payload,headers=headers)
    if res.status_code == 200 or res.status_code == 303:
        print(f'{student_id}@{student_pass} login --> statusCode {res.status_code}')

def QuerySearch(query):
    xfToken = get_xfToken('http://joonbud.com/professors/categories/saddleback-college.2/')
    payload = {'title':query,'_xfToken':xfToken}

    quickSearch = s.post('http://joonbud.com/resources/categories/quicksearch?category_id=2',data=payload)
    print(f'QuerySearch statusCode is {quickSearch.status_code}')
    soup = BeautifulSoup(quickSearch.text,'lxml')
    queryResults = soup.select('td[class="dataList-cell dataList-cell--link"]>a')
    for tag in queryResults:
        if query == tag.text:
            return tag['href']

def readTrackLog():
    with open('TrackLogg.txt') as trackLoggFile:
        trackRows = [line.strip() for line in trackLoggFile]
        return trackRows
def updateTrackLogger(comment):
    with open('TrackLogg.txt', 'a',encoding='utf-8') as file:
        file.write(comment+'\n')

def readRattingsInput(showSkip=False):
    trackRows = readTrackLog()
    for row in csv.DictReader(open('RattingsInput.csv')):
        comment = row['Comment']
        if comment not in trackRows:
            return row
        else:
            if showSkip: print(f'Skipped:: {comment[:30]}....')

def runRattingBot():
    with open('std_accounts.txt') as stdFile:
        for line in stdFile:
            student_id = line.strip().split(':')[0]
            student_pass = line.strip().split(':')[1]
            row = readRattingsInput()
            query = row['Teacher Name']
            rattings = int(row['Rating'])
            comment = row['Comment']
                
            login(student_id,student_pass)
            professorURI = QuerySearch(query)
            if professorURI:
                  
                postReview(professorURI,comment,rattings)
                updateTrackLogger(comment)
            else:
                print('Professor URI not found')


readRattingsInput(showSkip=True) # print skipped comment on terminal.
runRattingBot()

