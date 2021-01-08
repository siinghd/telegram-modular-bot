class ImgFlip:
    username = 'imOX'
    assword = 'stolemypass1234'   
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'

    def getMeme(self, link):
        #Fetch the available memes
        data = requests.get(link).json()['data']['memes']
        images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

        return images;
    