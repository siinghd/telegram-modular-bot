import requests
import urllib
class ImgFlip:
    username = '' #username
    password = '' #user pass
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'

    def getMeme(self, link):
        #Fetch the available memes
        data = requests.get(link).json()['data']['memes']
        images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

        return images;
    def generateMeme(self,text1,text2,id):
        # Fetch the generated meme
        URL = 'https://api.imgflip.com/caption_image'
        params = {
            'username': self.username,
            'password': self.password,
            'template_id': id,
            'text0': text1,
            'text1': text2
        }
        response = requests.request('POST', URL, params=params).json()
        return response