#! python
# -*- coding: utf-8 -*- 
import config,json,requests
from tools import sign,send_comment

def handler(event, context):
	# print(request.args)
	arg = dict(request.args)
	state = event['queryParameters']['state']
	content = event['queryParameters']['content']
	code = event['queryParameters']['code']

	# 不验证state
	if(not (state and content and code)):
		return '[!] arg error'

	content = json.loads(content)
		
	r = requests.post('https://github.com/login/oauth/access_token',
		data={'client_id':config.client_id,
		'client_secret':config.client_secret,
		'code':code,
		'state':state},
		headers={'Accept':'application/json'})
	r = r.json()
	if 'access_token' not in r:
		return '[!] OAuth failed. code:5'
	token = r['access_token']
	r = requests.get('https://api.github.com/user',auth=('token',token))
	# print(r.json())
	r = r.json()

	try:
		content['email'] = r['email']
		content['website'] = r['avatar_url'] or 'http://www.gravatar.com/avatar/'+r['gravatar_id']
		content['website'] += ' '+r['html_url']
		content['author'] = r['name']
	except Exception as e:
		return '[!] OAuth data error. code:6'
	r['access_token'] = token

	# # save content and r
	# print(r)
	# print(content)
	try:
		send_comment(content['uri'],content)
	except Exception as e:
		return '[!] OAuth link error. code:7'

	return ''
	return {
        'isBase64Encoded':False,
        'statusCode': 200,
        'headers': {
        "x-powered-by" : "Aliyun FC"
        },
        'body': '<html><head><meta charset="utf-8" /><title>Success!</title></head><body>Success.发表成功，谢谢~<script>setTimeout(function() {window.close()}, 100);</script></body></html>'
    }
