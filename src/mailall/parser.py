from jinja2 import Template

def parse(template_path, mail):
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
