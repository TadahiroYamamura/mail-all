from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from smtplib import SMTP
import os

import dotenv


class Mail:
  def __init__(self):
    self.to = []
    self.cc = []


  def message(self, subject, body):
    msg = MIMEMultipart(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('SEND_FROM')
    msg['To'] = ', '.join(self.to)
    msg['Cc'] = ', '.join(self.cc)
    msg['Date'] = formatdate()
    return msg


  def attach(self, msg, attachment_path):
    part = MIMEBase('application', 'octet-stream')
    with open(attachment_path, 'rb') as r:
      part.set_payload(r.read())
    encoders.encode_base64(part)
    filename = os.path.basename(attachment_path)
    part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
    msg.attach(part)
    return msg


  def send(self, msg):
    with SMTP(os.getenv('HOST'), os.getenv('PORT')) as smtp:
      smtp.starttls()
      smtp.login(os.getenv('SEND_FROM'), os.getenv('PASSWORD'))
      smtp.send_message(msg)


  @staticmethod
  def from_file(account_file):
    with open(account_file) as f:
      accounts = filter(lambda a: a, f.read().split('\n'))
    to_list = []
    cc_list = []
    for account in accounts:
      a = account.split(':')
      m = a[0].strip().lower()
      if m == 'to':
        to_list.append(a[1].strip())
      elif m == 'cc':
        cc_list.append(a[1].strip())
    me = Mail()
    me.to = to_list
    me.cc = cc_list
    return me
