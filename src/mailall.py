import argparse
from glob import glob
import os
import re

import dotenv

import mailall


class MailMetaInfo:
    def __init__(self):
        self.from_header = os.getenv('FROM_HEADER')
        self.host = os.getenv('HOST')
        self.port = os.getenv('PORT')
        self.user = os.getenv('MAIL_USER')
        self.password = os.getenv('PASSWORD')


def mail(args, meta):
    if args.list:
        folder = 'data/texts'
        extension = '.txt'
        return print_mail_template_list(folder, extension)

    dotenv.load_dotenv('smtpconfig')

    folder = 'data/texts'
    extension = '.txt'

    mail_template = select_mail_template(args, folder, extension)
    subject = re.sub('#.*$', '', mail_template)

    mails = map(
        lambda p: mailall.Mail.from_file(p, meta.from_header),
        glob('data/accounts/*.txt'))

    for mail in mails:
        file_path = os.path.join(folder, mail_template + extension)
        body_text = mailall.parse_mail(file_path, mail)
        mail.message(subject, body_text)
        for atch in glob('data/attachments/*'):
            mail.attach(atch)
        mail.send(
            meta.host,
            meta.port,
            meta.user,
            meta.password)


def print_mail_template_list(folder, extension):
    print()
    print('使用可能なメール文')
    print()
    for txt in glob(os.path.join(folder, '*' + extension)):
        print(os.path.basename(txt)[:len(extension) * -1])
    print()


def select_mail_template(args, folder, extension):
    if len(args.mail_title) > 0:
        return args.mail_title[0]
    print_mail_template_list(folder, extension)
    return input('どれを送信しますか？：')


def account(args, meta):
    if args.list:
        folder = 'data/accounts'
        extension = '.txt'
        return print_account_list(folder, extension)


def print_account_list(folder, extension):
    print()
    print('送信先一覧')
    print()
    enabled_companies = list(map(
        lambda txt: '送信可　' + '\t' + txt,
        map(
            lambda txt: os.path.basename(txt)[:len(extension) * -1],
            glob(os.path.join(folder, '*' + extension)))))
    disabled_companies = list(map(
        lambda txt: '送信不可' + '\t' + txt,
        map(
            lambda txt: os.path.basename(txt)[:len(extension) * -1],
            glob(os.path.join(folder, 'disabled', '*' + extension)))))
    for txt in sorted(enabled_companies + disabled_companies):
        print(os.path.basename(txt))
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='メールを一斉送信するためのツール。下記はサブコマンドの一覧です。')

    # sub command - mail
    subparsers = parser.add_subparsers()
    mail_parser = subparsers.add_parser('mail', help='メール送信コマンド')
    mail_parser.set_defaults(handler=mail)
    mail_parser.add_argument('-l',
                             '--list',
                             action='store_true',
                             help='送信可能なメールの件名一覧を表示する')
    mail_parser.add_argument('mail_title',
                             nargs='*',
                             help='送信するメール')

    # sub command - mail
    account_parser = subparsers.add_parser('account',
                                           help='メール送信先管理コマンド')
    account_parser.set_defaults(handler=account)
    account_parser.add_argument('-l',
                                '--list',
                                action='store_true',
                                help='送信先の一覧を表示する')

    args = parser.parse_args()
    meta = MailMetaInfo()
    if hasattr(args, 'handler'):
        args.handler(args, meta)
    else:
        parser.print_help()
