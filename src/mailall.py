import argparse
from glob import glob
import os
import re
import sys

import dotenv

import mailall


def mail(args):
  if args.list:
    folder = 'data/texts'
    extension = '.txt'
    return print_mail_template_list(folder, extension)
  else:
    dotenv.load_dotenv('smtpconfig')

    folder = 'data/texts'
    extension = '.txt'
    mail_template = args.mail_title[0] if len(args.mail_title) > 0 else select_mail_template(folder, extension)
    subject = re.sub('#.*$', '', mail_template)

    mails = map(
      lambda path: mailall.Mail.from_file(path, os.getenv('FROM_HEADER')),
      glob('data/accounts/*.txt'))

    for mail in mails:
      body_text = mailall.parse_mail(os.path.join(folder, mail_template + extension), mail)
      mail.message(subject, body_text)
      for atch in glob('data/attachments/*'):
        mail.attach(atch)
      mail.send(
        os.getenv('HOST'),
        os.getenv('PORT'),
        os.getenv('MAIL_USER'),
        os.getenv('PASSWORD'))


def print_mail_template_list(folder, extension):
  print()
  print('使用可能なメール文')
  print()
  for txt in glob(os.path.join(folder, '*' + extension)):
    print(os.path.basename(txt)[:len(extension) * -1])
  print()


def select_mail_template(folder, extension):
  print_mail_template_list(folder, extension)
  return input('どれを送信しますか？：')


def print_account_list(folder, extension):
  pass


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='メールを一斉送信するためのツール。下記はサブコマンドの一覧です。')

  # サブコマンドの設定
  subparsers = parser.add_subparsers()
  mail_parser = subparsers.add_parser('mail', help='メール送信コマンド')
  mail_parser.add_argument('-l', '--list', action='store_true', help='送信可能なメールの件名一覧を表示する')
  mail_parser.add_argument('mail_title', nargs='*', help='送信するメール')
  mail_parser.set_defaults(handler=mail)

  account_parser = subparsers.add_parser('account', help='メール送信先管理コマンド')

  # コマンド実行
  args = parser.parse_args()
  if hasattr(args, 'handler'):
    args.handler(args)
  else:
    parser.print_help()
