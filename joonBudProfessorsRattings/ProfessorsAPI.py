import requests,json,csv
from  bs4 import BeautifulSoup
s = requests.Session()




def queryProfessor(query):

    '''Query Search'''
    payload = {'title':query,'_xfToken':'1664618475,ef58242045356eda55e1908585590cbd'}
    headers = {
        'Accept':'text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'xf_csrf=J0u7z4HE5RdgS4y4; xf_user=57,DC8JcRksYrF_Rlf-DEj_rkJfi3FXSgOPnKpFEQsa; xf_session=8vP1v9KwDALcA0uVj4JYhI9qi0BmFXcq',
        'Referer':'http://joonbud.com/professors/categories/saddleback-college.2/',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'

    }
    quickSearch = requests.post('http://joonbud.com/resources/categories/quicksearch?category_id=2',data=payload,headers=headers)
    soup = BeautifulSoup(quickSearch.text,'lxml')
    queryResults = soup.select('td[class="dataList-cell dataList-cell--link"]>a')

    for tag in queryResults:
        if query == tag.text:
            return tag['href']

def get_xfToken(url):
    kk = requests.get(url)
    soup = BeautifulSoup(kk.text,'lxml')
    _xfToken = soup.select_one('[name="_xfToken"]')['value']
    return _xfToken
    
def loginTojobBud(student_id,student_pass):
    # _xfTokenNew = self.get_xfToken('http://joonbud.com/login/login')
    # _xfToken = _xfTokenNew if _xfTokenNew else '1664616373,43a506e3fa3a5fde6aa193e1d16daae8'
    s = requests.Session()
    loginUrl = 'http://joonbud.com/login/login'
    payload = {
        '_xfToken':'1664616373,43a506e3fa3a5fde6aa193e1d16daae8',
        'login':student_id,
        'password':student_pass,
        'remember':1,
        '_xfRedirect':'http://joonbud.com/'
    }
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        'Cookie': 'xf_session=cGnw86N9fN4mHsumlSNat0mJ1iCDM5pw; xf_csrf=J0u7z4HE5RdgS4y4',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection':'keep-alive'
    }
    logres = s.post(loginUrl,data=payload,headers=headers) # login
    print(logres)
    # return s

def postReview(professorURI,comment,rattings):
    # http://joonbud.com/professors/john-allen-m.694/rate
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
    print(rattings, type(rattings))
    reatres = s.post(professorRateURL,data=ratePayload) # post comment/Reviews
    print(reatres)

def runRattingBot():
    student_id ='mutest1',
    student_pass = 'mustafadevupwork',
    comment = 'good'
    rattings = 5
    query = 'John Allen MATH253'
    professorURI = queryProfessor(query)
    if professorURI:
        print(professorURI)
        loginTojobBud(student_id,student_pass)
        postReview(professorURI,comment,rattings)
    else:
        print('Professor URI not found')


if __name__ == '__main__':
    runRattingBot()
