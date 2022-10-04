import requests,json,csv,re
from  bs4 import BeautifulSoup
s = requests.Session()
base_headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'http://joonbud.com',
    'Pragma': 'no-cache',
    'Referer': 'http://joonbud.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

def get_xfToken(url):
    kk = s.get(url)
    soup = BeautifulSoup(kk.text,'lxml')
    _xfToken = soup.select_one('[name="_xfToken"]')['value']
    return _xfToken

def postReview(professorURI,comment,rattings):
    professorRateURL = 'http://joonbud.com' +professorURI+ 'rate'
    _xfToken = get_xfToken(professorRateURL)
    data = f'------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{_xfToken}\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="rating"\r\n\r\n{rattings}\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="message"\r\n\r\n{comment}\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[strategy]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[quality]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[time]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[difficulty]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[yourgrade]"\r\n\r\na\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[availability]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[cost]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="custom_fields[attendance]"\r\n\r\n\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="_xfRequestUri"\r\n\r\n/professors/freshwater-eng.1874/\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="_xfWithData"\r\n\r\n1\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{_xfToken}\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5\r\nContent-Disposition: form-data; name="_xfResponseType"\r\n\r\njson\r\n------WebKitFormBoundaryjUm6cjNJC9eqRev5--\r\n'
    s.headers.update({'Referer':'http://joonbud.com'+professorURI,'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryjUm6cjNJC9eqRev5','X-Requested-With': 'XMLHttpRequest',})
    rateResp = s.post(professorRateURL,data=data) # post comment/Reviews
    if rateResp.status_code == 200:
        print(f'{rattings} start ratting posted --> statusCode {rateResp.status_code}')
        print(f'Posted:: {comment[:30]}....')

def login(student_id,student_pass):
    xfToken = get_xfToken('http://joonbud.com/login/login')  
    loginUrl = 'http://joonbud.com/login/login'
    payload = {
        '_xfToken':xfToken,
        'login':student_id,
        'password':student_pass,
        'remember':1,
        '_xfRedirect':'http://joonbud.com/'
    }
    res = s.post(loginUrl,data=payload,verify=False)
    
    if res.status_code == 200 or res.status_code == 303:
        cookies = res.history[0].headers.get('Set-Cookie')
        print(f'{student_id}@{student_pass} login --> statusCode {res.status_code}')
        xf_user = re.findall(r'xf_user.+?(?=;)',cookies)[0].removeprefix('xf_user=')
        xf_session = re.findall(r'xf_session.+?(?=;)',cookies)[0].removeprefix('xf_session=')
        # s.headers.update({'Cookie':cookies})
        cookies = {"xf_user":xf_user,"xf_session":xf_session}
        s.cookies.update(cookies)

def QuerySearch(query):
    xfToken = get_xfToken('http://joonbud.com/professors/categories/saddleback-college.2/')
    data = {'title':query,'_xfToken':xfToken}
    s.headers.update({'Referer': 'http://joonbud.com/professors/categories/saddleback-college.2/','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With': 'XMLHttpRequest',})
    quickSearch = s.post('http://joonbud.com/resources/categories/quicksearch?category_id=2',data=data)
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
    global s
    with open('std_accounts.txt') as stdFile:
        for line in stdFile:
            s = requests.Session()
            s.headers.update(base_headers)
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


# print(login("mutest2","mustafadevupwork"))
readRattingsInput(showSkip=True) # print skipped comment on terminal.
runRattingBot()


# print(get_xfToken('http://joonbud.com/login/login') )

