from jinja2 import Template

def parse_mail(template_path, mail):
  with open(template_path, 'r', encoding='cp932') as f:
    template = Template(f.read())
  account = {
    'to': '、'.join(map(lambda a: a['name'] + '様', mail.find_account_by_method('to'))),
    'cc': '、'.join(map(lambda a: a['name'] + '様', mail.find_account_by_method('cc')))
  }
  account['filename'] = mail.find_account_by_method('to')[0]['filename']
  arg = {
    'account': account
  }
  return template.render(arg)


def parse_account(account_file:str) -> dict:
  with open(account_file, 'r', encoding='utf-8') as f:
    content = f.read()
  organization_name, *rest = content.split('\n\n')
  mail_account_list_str = '\n'.join(rest)
  mail_account_list = map(
    lambda zipped: { x[0]:x[1] for x in zipped },
    map(
      lambda line_elements: zip(['method', 'name', 'address'], line_elements),
      map(
        lambda line: line.split(':'),
        filter(
          lambda line: line,
          map(
            lambda line: line.strip(),
            mail_account_list_str.split('\n')
  )))))
  return {
    'name': organization_name,
    'accounts': list(mail_account_list),
  }
