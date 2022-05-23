import urllib.request
import zipfile
import os
import shutil
import json

if os.path.exists('pack'):
    shutil.rmtree('pack')
if os.path.exists('current-pack.zip'):
    os.remove("current-pack.zip")

url = 'https://aka.ms/resourcepacktemplate'
urllib.request.urlretrieve(url, 'current-pack.zip')

with zipfile.ZipFile('current-pack.zip', 'r') as zip_ref:
    os.mkdir('pack')
    zip_ref.extractall('pack')

manifestFile = open('pack/manifest.json', 'r')

manifest = json.loads(manifestFile.read())

manifestFile.close()

manifest['header']['description'] = 'Ray tracing enabled texture pack!'
manifest['modules'][0]['description'] = 'Ray tracing enabled texture pack!'
manifest['capabilities'] = ['raytraced']

manifestFile = open('pack/manifest.json', 'w+')
manifestFile.write(json.dumps(manifest));
manifestFile.close()

for (path, directories, files) in os.walk('pack/textures/blocks/'):
     for file in files:
          print('found %s' % os.path.join(path, file))

