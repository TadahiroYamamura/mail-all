from email import encoders
from email.message import EmailMessage
from email.utils import formatdate
import mimetypes
from smtplib import SMTP
import os


class Mail:
  def __init__(self):
    self.to = []
    self.cc = []


  def message(self, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg.set_content(body)
    msg['From'] = os.getenv('SEND_FROM')
    msg['To'] = ', '.join(self.to)
    msg['Cc'] = ', '.join(self.cc)
    msg['Date'] = formatdate()
    self._msg = msg
    return self


  def attach(self, attachment_path):
    mime = mimetypes.guess_type(attachment_path)[0]
    (mime_main, mime_sub) = mime.split('/')
    filename = os.path.basename(attachment_path)
    with open(attachment_path, 'rb') as r:
      self._msg.add_attachment(r.read(),
                         maintype=mime_main,
                         subtype=mime_sub,
                         filename=filename)
    return self


  def send(self):
    with SMTP(os.getenv('HOST'), os.getenv('PORT')) as smtp:
      smtp.starttls()
      smtp.login(os.getenv('SEND_FROM'), os.getenv('PASSWORD'))
      smtp.send_message(self._msg)


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
