from glob import glob
import os
import re

import dotenv

import mailall


def main():
  dotenv.load_dotenv('smtpconfig')
  mails = map(
    lambda path: mailall.Mail.from_file(path, os.getenv('FROM_HEADER')),
    glob('data/accounts/*.txt'))

  folder = 'data/texts'
  extension = '.txt'
  mail_template = target_mail_template(folder, extension)
  subject = re.sub('#.*$', '', mail_template)

  for mail in mails:
    body_text = mailall.parse(os.path.join(folder, mail_template + extension), mail)
    mail.message(subject, body_text)
    for atch in glob('data/attachments/*'):
      mail.attach(atch)
    mail.send(
      os.getenv('HOST'),
      os.getenv('PORT'),
      os.getenv('MAIL_USER'),
      os.getenv('PASSWORD'))


def target_mail_template(folder, extension):
  print()
  print('【使用可能なメール文】')
  for txt in glob(os.path.join(folder, '*' + extension)):
    print(os.path.basename(txt)[:len(extension) * -1])
  print()
  return input('どれを送信しますか？：')


if __name__ == '__main__':
  main()
