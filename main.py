"""Tool to generate the framework of an Minecraft RTX Resouce Pack"""
import urllib.request
import zipfile
import os
import shutil
import uuid
import json
from PIL import Image

SHOULD_CLEAN_INSTALL = True

if os.path.exists('pack'):
    shutil.rmtree('pack')

if os.path.exists('current-pack.zip') and SHOULD_CLEAN_INSTALL:
    os.remove("current-pack.zip")

URL = 'https://aka.ms/resourcepacktemplate'

if SHOULD_CLEAN_INSTALL:
    urllib.request.urlretrieve(URL, 'current-pack.zip')

with zipfile.ZipFile('current-pack.zip', 'r') as zip_ref:
    os.mkdir('pack')
    zip_ref.extractall('pack')




if SHOULD_CLEAN_INSTALL:

    manifestFile = open('pack/manifest.json', 'r', encoding='utf-8')
    manifest = json.loads(manifestFile.read())
    manifestFile.close()

    manifest['header']['description'] = 'Ray tracing enabled texture pack!'
    manifest['modules'][0]['description'] = 'Ray tracing enabled texture pack!'
    manifest['capabilities'] = ['raytraced']

    manifest['header']['uuid'] = str(uuid.uuid1())
    manifest['modules'][0]['uuid'] = str(uuid.uuid1())

    manifestFile = open('pack/manifest.json', 'w+', encoding='utf-8')
    manifestFile.write(json.dumps(manifest))
    manifestFile.close()

textureSetSampleFile = open('sample.texture_set.json', 'r', encoding='utf-8')
textureSetSample = textureSetSampleFile.read()
textureSetSampleFile.close()

for (path, directories, files) in os.walk('pack/textures/blocks/'):
    for file in files:
        filePath = path + '/' + file

        merPath = filePath.replace('.png', '_mer.png')
        hmPath = filePath.replace('.png', '_heightmap.png')

        merImage = Image.new('RGB', (16, 16), (0, 0, 255)) # Fill with roughness
        hmImage = Image.new('L', (16, 16), 127) # Fill with half height to create base

        merImage.save(merPath)
        hmImage.save(hmPath)

        tsPath = filePath.replace('.png', '.texture_set.json')
        tsFile = open(tsPath, 'w+', encoding='utf-8')
        tsFile.write(textureSetSample.replace('name', file))
