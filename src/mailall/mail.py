from email import encoders
from email.message import EmailMessage
from email.utils import formatdate
import mimetypes
from smtplib import SMTP
import os


class Mail:
  def __init__(self, send_from):
    self._accounts = []
    self._send_from = send_from

  def message(self, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg.set_content(body)
    msg['From'] = self._send_from
    msg['To'] = ', '.join(map(lambda a: a['address'], self.find_account_by_method('to')))
    msg['Cc'] = ', '.join(map(lambda a: a['address'], self.find_account_by_method('cc')))
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

  def send(self, host, port, user, password):
    with SMTP(host, port) as smtp:
      smtp.starttls()
      smtp.login(user, password)
      smtp.send_message(self._msg)

  def find_account_by_method(self, method):
    return list(filter(lambda x: x['method'].lower() == method, self._accounts))

  @staticmethod
  def from_file(account_file, send_from):
    with open(account_file, 'r', encoding='utf-8') as f:
      account_data = map(
        lambda a: { x[0]:x[1] for x in a },
        map(
          lambda a: zip(['method', 'name', 'address'], a),
          map(
            lambda a: a.split(':'),
            filter (
              lambda a: a,
              f.read().split('\n')
        ))))
    filename = os.path.splitext(os.path.basename(account_file))[0]
    me = Mail(send_from)
    for a in account_data:
      a['filename'] = filename
      me._accounts.append(a)
    return me
