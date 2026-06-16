import requests
import json
import os

BASE = 'http://127.0.0.1:8000'
TEST_IMAGE = 'test_upload.jpg'

s = requests.Session()

print('1) Uploading image...')
with open(TEST_IMAGE,'rb') as f:
    r = s.post(BASE + '/upload', files={'image': f})
print('Status:', r.status_code)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))
resp = r.json()
if resp.get('error'):
    raise SystemExit('Upload error: ' + resp['error'])

if resp.get('matched'):
    print('Image matched existing:', resp.get('match'))
    filename = resp.get('filename')
    phash = resp.get('match', {}).get('phash')
else:
    filename = resp.get('filename')
    phash = resp.get('phash')
    suggested = resp.get('suggested')
    print('Suggested:', suggested)
    # catalog using suggested category if available
    category = suggested['category'] if suggested else 'Equipamentos de informática'
    explanation = suggested['neighbors'][0]['explanation'] if suggested and suggested['neighbors'] and suggested['neighbors'][0].get('explanation') else 'Teste automático'
    payload = {'filename': filename, 'phash': phash, 'category': category, 'explanation': explanation}
    r2 = s.post(BASE + '/catalog', json=payload)
    print('Catalog status:', r2.status_code, r2.text)

print('\n2) Checking catalogs page...')
r = s.get(BASE + '/catalogs')
print('Status:', r.status_code)
if TEST_IMAGE in r.text:
    print('Image appears in catalog page')
else:
    print('Image NOT found in catalog page')

print('\n3) Logging in as admin and removing latest item (if any)')
login = s.post(BASE + '/login', data={'username':'admin','password':'password'})
print('Login status:', login.status_code)
# get admin page to find item id
r = s.get(BASE + '/admin')
if 'Nenhum item cadastrado' in r.text:
    print('No items to delete')
else:
    # crude parse: find /admin/delete/<id>
    import re
    m = re.search(r'/admin/delete/(\d+)', r.text)
    if m:
        item_id = m.group(1)
        print('Deleting item id', item_id)
        rdel = s.post(BASE + f'/admin/delete/{item_id}')
        print('Delete status:', rdel.status_code)
    else:
        print('Could not find item id to delete')

print('\nTests finished')
