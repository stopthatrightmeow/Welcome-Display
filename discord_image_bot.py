from os import remove
import discord
import requests
import logging
import shutil
import magic
import os 

# For logging purposes
logger = logging.getLogger("Discord-Downloads")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler("./download.log")
fh.setFormatter(formatter)
logger.addHandler(fh)

# Instantiate the discord client
client = discord.Client()

# Probably need to move this to the if __name__ == '__main__'
@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Log all commands sent, will pull in all URLs etc... 
    logger.info(message.content)

    image_types = ['image/jpeg', 'image/png', 'image/pjpeg']

    try:
        # Help Menu
        if message.content.startswith('$help'):
            await message.channel.send('Help menu for Pickles the Wallpaper Mage:\n'
                'There are five folders you can save to: `america`, `birthday`, `christmas`, `halloween` and `normal`.\n'
                'Currently there are only two supported file types: `.jpg`, `.jpeg`, or `.png`.\n'
                'Select a folder to download to by running `$d<beginning letter of folder name> <imageurl>`.\n'
                'For example if you wanted to download an image to the `normal` folder you would run the following comand:\n\n'
                '`$dn <url to image>`')

        # General unsupported commands
        elif len(message.content.split(' ')) >2 and message.content.startswith('$'):
            logger.error(f"Non supported command: {message.content}")
            await message.channel.send(f"I'm sorry, there was an issue with that command: `{message.content}`. Try `$help` to get more information.")

        # Unsupported link types
        elif message.content.startswith('$') and not (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
                logger.error(f'Unsupported URL type found: {message.content}')
                await message.channel.send(f'Unsupported URL type. Ensure the URL ends with `.jpg`, `.jpeg`, or `.png`.')

        # Normal Photos
        elif message.content.startswith('$dn') and (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
            image_url = message.content.split(' ')[1]
            filename = image_url.split('/')[-1]
            file_path = './static/Backgrounds/normal/'
            
            # The file already exists
            if os.path.exists(file_path + filename):
                await message.channel.send(f'File {filename} already already exists!!')
                logger.error(f'File already exists: {filename}.')
            # Download the image
            else:
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    r.raw.decode_content=True
                    with open(file_path + filename, mode='wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    logger.error(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                    await message.channel.send(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                
                # Test file magic for safety
                mime_type = magic.from_file(file_path + filename, mime=True)
                if mime_type not in image_types:
                    await message.channel.send(f"{filename} is not an image file, you should check your logs...")
                    logger.critical(f'{file_path} was {mime_type} type, not an image.')
                    os.remove(file_path)
                else:                            
                    await message.channel.send(f'Saved {filename}!')
                    logger.info(f'Saved {filename}')

        # Christmas Photos
        elif message.content.startswith('$dc') and (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
            image_url = message.content.split(' ')[1]
            filename = image_url.split('/')[-1]
            file_path = './static/Backgrounds/christmas/'
            
            # The file already exists
            if os.path.exists(file_path + filename):
                await message.channel.send(f'File {filename} already already exists!!')
                logger.error(f'File already exists: {filename}.')
            # Download the image
            else:
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    r.raw.decode_content=True
                    with open(file_path + filename, mode='wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    logger.error(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                    await message.channel.send(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                
                # Test file magic for safety
                mime_type = magic.from_file(file_path + filename, mime=True)
                if mime_type not in image_types:
                    await message.channel.send(f"{filename} is not an image file, you should check your logs...")
                    logger.critical(f'{file_path} was {mime_type} type, not an image.')
                    os.remove(file_path)
                else:                            
                    await message.channel.send(f'Saved {filename}!')
                    logger.info(f'Saved {filename}')

        # America Photos
        elif message.content.startswith('$da') and (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
            image_url = message.content.split(' ')[1]
            filename = image_url.split('/')[-1]
            file_path = './static/Backgrounds/america/'

            # The file already exists
            if os.path.exists(file_path + filename):
                await message.channel.send(f'File {filename} already already exists!!')
                logger.error(f'File already exists: {filename}.')
            # Download the image
            else:
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    r.raw.decode_content=True
                    with open(file_path + filename, mode='wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    logger.error(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                    await message.channel.send(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                
                # Test file magic for safety
                mime_type = magic.from_file(file_path + filename, mime=True)
                if mime_type not in image_types:
                    await message.channel.send(f"{filename} is not an image file, you should check your logs...")
                    logger.critical(f'{file_path} was {mime_type} type, not an image.')
                    os.remove(file_path)
                else:                            
                    await message.channel.send(f'Saved {filename}!')
                    logger.info(f'Saved {filename}')

        # Halloween Photos
        elif message.content.startswith('$dh') and (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
            image_url = message.content.split(' ')[1]
            filename = image_url.split('/')[-1]
            file_path = './static/Backgrounds/halloween/'

            # The file already exists
            file_path = file_path + 'halloween/'
            if os.path.exists(file_path + filename):
                await message.channel.send(f'File {filename} already already exists!!')
                logger.error(f'File already exists: {filename}.')
            # Download the image
            else:
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    r.raw.decode_content=True
                    with open(file_path + filename, mode='wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    logger.error(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                    await message.channel.send(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                
                # Test file magic for safety
                mime_type = magic.from_file(file_path + filename, mime=True)
                if mime_type not in image_types:
                    await message.channel.send(f"{filename} is not an image file, you should check your logs...")
                    logger.critical(f'{file_path} was {mime_type} type, not an image.')
                    os.remove(file_path)
                else:                            
                    await message.channel.send(f'Saved {filename}!')
                    logger.info(f'Saved {filename}')

        # Birthday Photos
        elif message.content.startswith('$db') and (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
            image_url = message.content.split(' ')[1]
            filename = image_url.split('/')[-1]
            file_path = './static/Backgrounds/birthday/'

            # The file already exists
            file_path = file_path + 'birthday/'
            if os.path.exists(file_path + filename):
                await message.channel.send(f'File {filename} already already exists!!')
                logger.error(f'File already exists: {filename}.')
            # Download the image
            else:
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    r.raw.decode_content=True
                    with open(file_path + filename, mode='wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    logger.error(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                    await message.channel.send(f'Unable to download image - {filename} - site returned status code: {r.status_code}')
                
                # Test file magic for safety
                mime_type = magic.from_file(file_path + filename, mime=True)
                if mime_type not in image_types:
                    await message.channel.send(f"{filename} is not an image file, you should check your logs...")
                    logger.critical(f'{file_path} was {mime_type} type, not an image.')
                    os.remove(file_path)
                else:                            
                    await message.channel.send(f'Saved {filename}!')
                    logger.info(f'Saved {filename}')

    except Exception as e:
        await message.channel.send(f'I have failed you: {e}')
        logger.error(f'Unable to download photo: {message.content}: {e}')


client.run('<YOUR CLIENT SECRET HERE>')