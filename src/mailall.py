from glob import glob
import os

import dotenv

from mailall import Mail


def main():
  dotenv.load_dotenv('smtpconfig')
  mails = map(lambda path: Mail.from_file(path), glob('data/accounts/*.txt'))
  print()
  print('【使用可能なメール文】')
  for txt in glob('data/texts/*.txt'):
    print(os.path.basename(txt)[:-4])
  print()
  subject = input('どれを送信しますか？：')
  with open(os.path.join('data/texts', subject + '.txt')) as f:
    body_message = f.read()
  mails = map(lambda m: m.message(subject, body_message), mails)
  for atch in glob('data/attachments/*'):
    mails = map(lambda m: m.attach(atch), mails)
  for m in mails:
    m.send()


if __name__ == '__main__':
  main()
