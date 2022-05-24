"""Tool to generate the framework of an Minecraft RTX Resouce Pack"""
import urllib.request
import zipfile
import os
import shutil
import uuid
import json
from PIL import Image
from block_operations import create_height_map

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

        mer_path = ''
        hm_path = ''
        ts_path = ''

        if not filePath.find('.png') == -1:
            mer_path = filePath.replace('.png', '_mer.png')
            hm_path = filePath.replace('.png', '_heightmap.png')
            ts_path = filePath.replace('.png', '.texture_set.json')

        if not filePath.find('.tga') == -1:
            mer_path = filePath.replace('.tga', '_mer.png')
            hm_path = filePath.replace('.tga', '_heightmap.png')
            ts_path = filePath.replace('.tga', '.texture_set.json')
        

        colorImage = Image.open(filePath)

        merImage = Image.new('RGB', (colorImage.size[0], colorImage.size[1]), (0, 0, 255)) # Fill with roughness
        hmImage = Image.new('L', (colorImage.size[0], colorImage.size[1]), 127) # Fill with half height to create base

        merImage.save(mer_path)
        hmImage.save(hm_path)

        tsFile = open(ts_path, 'w+', encoding='utf-8')
        tsFile.write(textureSetSample.replace('name', file.replace('.png', '').replace('.tga', '')))

        create_height_map(filePath, hm_path)



# Take grey scale as heightmap
# Take color as emmisive for ore
# set metallic and roughness for blocksof
# set emmisive for light sections of emmissive blocks
