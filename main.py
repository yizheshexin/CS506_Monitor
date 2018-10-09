from bs4 import BeautifulSoup
import requests as re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
url1 = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1533488353?ModuleName=univschr.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S&KeySem=20193&ViewSem=Fall+2018&College=CAS&Dept=cs&Course=506&Section='
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
response = re.get(url1,headers = headers)
content = response.content
soup = BeautifulSoup(content, 'html.parser')
cs506a1 = soup.body.find_all('table',recursive=False)[3].find_all('tr',recursive=False)[2].find_all('td',recursive=False)[6]
openseat = int(cs506a1.string)
print(openseat)

my_sender = ''  # 发件人邮箱账号
my_pass = ''  # 发件人邮箱密码
my_user = ''  # 收件人邮箱账号，我这边发送给自己
def mail():
    ret = True
    try:
        msg = MIMEText('CS506剩余座位数大于0', 'plain', 'utf-8')
        msg['From'] = formataddr(["cc163", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["ccgmail", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "BU教务系统选课提醒"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
if openseat > 0:
    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
else:
    print('邮件未发送')
