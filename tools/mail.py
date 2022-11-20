import smtplib
import traceback
from email.header import Header
from email.mime.text import MIMEText

from utils import print_suc, print_err

mail_user = "2928109164@qq.com"  # 用户名
mail_pass = "tmsqsjkmvybkdgfh"  # 口令


# 邮件发送函数
def sendmail(recv: list, content: str, subject='自动化扫描工具'):
    mail_host = "smtp.qq.com"  # 设置服务器
    sender = mail_user
    receivers = recv  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("自动扫描工具", 'utf-8')
    message['To'] = Header("客户端", 'utf-8')

    subject = subject
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print_suc('邮件发送成功')
    except smtplib.SMTPException:
        print_err('邮件发送失败')
        traceback.print_exc()


# 设置邮件任务已经处理
def set_mail_is_auth(id):
    # a = open('auth.list', 'w+')
    # a.close()
    do_list = open('auth.list', 'a')
    do_list.write(str(id) + '\n')
    do_list.close()


def check_mail_is_auth(id: str):
    do_list = open('auth.list', 'r').readlines()
    for it in do_list:
        it = it.replace('\n', '')
        it = it.replace('\r', '')
        it = it.replace('\t', '')
        it = it.replace(' ', '')
        # print(id)
        # print(it)
        if str(id) == str(it):
            return True
    return False


# 检查邮件任务是否处理
def check_mail_is_do(id: str):
    do_list = open('do.list', 'r').readlines()
    for it in do_list:
        it = it.replace('\n', '')
        it = it.replace('\r', '')
        it = it.replace('\t', '')
        it = it.replace(' ', '')
        # print(id)
        # print(it)
        if str(id) == str(it):
            return True
    return False


# 设置邮件任务已经处理
def set_mail_is_do(id):
    # a = open('do.list', 'w+')
    # a.close()
    do_list = open('do.list', 'a')
    do_list.write(str(id) + '\n')
    do_list.close()
