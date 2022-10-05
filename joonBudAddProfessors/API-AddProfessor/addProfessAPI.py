import requests,csv,json,re
from bs4 import BeautifulSoup
s = requests.Session()



class AddProfessorsBot:
    def __init__(self, admin_id, admin_pass,addUrl):
        self.admin_id = admin_id
        self.admin_pass = admin_pass
        self.addUrl = addUrl

    def get_xfToken(self,url):
        kk = s.get(url)
        soup = BeautifulSoup(kk.text,'lxml')
        _xfToken = soup.select_one('[name="_xfToken"]')['value']
        return _xfToken

    def login(self,admin_id,admin_pass):
        xfToken = self.get_xfToken('http://joonbud.com/login/login')  
        loginUrl = 'http://joonbud.com/login/login'
        payload = {
            '_xfToken':xfToken,
            'login':admin_id,
            'password':admin_pass,
            'remember':1,
            '_xfRedirect':'http://joonbud.com/'
        }
        res = s.post(loginUrl,data=payload,verify=False)
        
        if res.status_code == 200 or res.status_code == 303:
            cookies = res.history[0].headers.get('Set-Cookie')
            print(f'{admin_id}@{admin_pass} login --> statusCode {res.status_code}')
            xf_user = re.findall(r'xf_user.+?(?=;)',cookies)[0].removeprefix('xf_user=')
            xf_session = re.findall(r'xf_session.+?(?=;)',cookies)[0].removeprefix('xf_session=')
            # s.headers.update({'Cookie':cookies})
            cookies = {"xf_user":xf_user,"xf_session":xf_session}
            s.cookies.update(cookies)

    def addProfessor(self,row):
        title,tag_line = row[0],row[1]
        xfToken = self.get_xfToken(self.addUrl)
        addPayload = {
            '_xfToken':xfToken,
            'prefix_id':1,
            'title':title,
            'tag_line':tag_line,
            'resource_type':'fileless',
            'description':'-',
            # 'attachment_hash':'a857f76edb39b845ce4439ed61916cde',
            # 'attachment_hash_combined':'{"type":"resource_update","context":{"resource_category_id":2},"hash":"a857f76edb39b845ce4439ed61916cde"}',
            # '_xfRequestUri':'/professors/categories/saddleback-college.2/add',
            
        }
        # addUrl = 'http://joonbud.com/professors/categories/saddleback-college.2/add'
        addresp = s.post(self.addUrl,data=addPayload)
        soup = BeautifulSoup(addresp.content,'lxml')
        restitle = soup.title.text
        if title in restitle:
            print(f'Added:: {title} -----> {tag_line}')
        if 'Oops' in restitle:
            print(f'Already added:: {title} -----> {tag_line}')

    def readTrackLog(self):
        with open('TrackLogg.csv') as trackLoggFile:
            trackRows = list(csv.reader(trackLoggFile))
            return trackRows
        
        
    def updateTrackLogger(self,row):
        with open('TrackLogg.csv', 'a',encoding='utf-8',newline='') as file:
            csv.writer(file).writerow(row)



    def run(self):
        # adminID = 'mustafadev'
        # adminPSW = 'mustafadevupwork'
        self.login(self.admin_id,self.admin_pass)
        trackRows = self.readTrackLog()
        with open('addingInput.csv') as inputDataFile:
            inputRows = list(csv.reader(inputDataFile))
            for row in inputRows:
                if row not in trackRows:
                    self.addProfessor(row)
                    self.updateTrackLogger(row)
                    trackRows = self.readTrackLog()
                else:
                    print(f'skipped::{row}')

if __name__ == '__main__':
    config = json.load(open('config.json'))
    admin_id = config['admin_id']
    admin_pass = config['admin_pass']
    addUrl = config['addUrl']
    addBot = AddProfessorsBot(admin_id,admin_pass,addUrl)
    addBot.run()