import requests,json,csv
from  bs4 import BeautifulSoup
s = requests.Session()


class ProfessorRatting:

    # def __init__(self,student_id,student_pass):
    #     pass
        # self.student_id = student_id
        # self.student_pass = student_pass

    def queryProfessor(self,query):

        '''Query Search'''
        print(s.cookies)
        xfToken = self.get_xfToken('http://joonbud.com/professors/categories/saddleback-college.2/')
        payload = {'title':query,'_xfToken':xfToken}
        quickSearch = s.post('http://joonbud.com/resources/categories/quicksearch?category_id=2',data=payload)
        soup = BeautifulSoup(quickSearch.text,'lxml')
        queryResults = soup.select('td[class="dataList-cell dataList-cell--link"]>a')

        for tag in queryResults:
            print(tag.text)
            if query == tag.text:
                return tag['href']

    def get_xfToken(self,url):
        kk = requests.get(url)
        soup = BeautifulSoup(kk.text,'lxml')
        _xfToken = soup.select_one('[name="_xfToken"]')['value']
        return _xfToken
    
    def loginTojobBud(self,student_id,student_pass):
        
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
        logres = s.post(loginUrl,data=payload,headers=headers) # login
        with open('kk.html', 'wb') as f: f.write(logres.content)
        print(logres)


    def postReview(self,professorURI,comment,rattings):
        # http://joonbud.com/professors/john-allen-m.694/rate
        professorRateURL = 'http://joonbud.com' +professorURI+ 'rate'
        _xfToken = self.get_xfToken(professorRateURL)
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
        print(reatres)

    def runRattingBot(self):
        student_id ='mutest1',
        student_pass = 'mustafadevupwork',
        comment = 'good'
        rattings = 5
        query = '. Reyes HIST17'
        self.loginTojobBud(student_id,student_pass)
        professorURI = self.queryProfessor(query)
        if professorURI:
            print(professorURI)
            self.postReview(professorURI,comment,rattings)
        else:
            print('Professor URI not found')


if __name__ == '__main__':
    bot = ProfessorRatting()
    bot.runRattingBot()
