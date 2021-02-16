import json
import os

import requests

import ModuleCommandChecker
from Modules.Base import Mod_Base
from Modules.UsefulMethods import WORNGMSG, tryTosendMsg


class Mod_Photo(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_Photo,self).__init__("Photo",["/upscaleimage","/colorbwphoto","/modifyphoto"],
                                        [])

    def handleOnCommand(self,message,name):
        try:
            if name == "/upscaleimage":
                if  message.reply_to_message is not None and  message.reply_to_message.content_type=="photo":
                    self.user_step.append(message.from_user.id)
                    self.send_modified_photo(message)
                else:
                    self.send_photoMsg(message,"Please send me photo",self.send_modified_photo)
            elif name=="/modifyphoto":
                if message.reply_to_message is not None and message.reply_to_message.content_type=="photo":
                    self.user_step.append(message.from_user.id)
                    self.send_photoToonify(message)
                else:
                    self.send_photoMsg(message, "Please send me photo with visible face!", self.send_photoToonify)
            elif name=="/colorbwphoto":
                if message.reply_to_message is not None and message.reply_to_message.content_type == "photo":
                    self.user_step.append(message.from_user.id)
                    self.send_photobw(message)
                else:
                    self.send_photoMsg(message, "Please send me Black and white photo", self.send_photobw)
        except Exception as e:
            self.bot.reply_to(message,WORNGMSG)



    def getEveryMessageMethod(self,message):
        pass

    def send_photoMsg(self, message,msg,method):
        self.user_step.append(message.from_user.id)
        tryTosendMsg(message,msg,self.bot)
        self.bot.register_next_step_handler_by_chat_id(message.chat.id, method)

    def send_modified_photo(self,message):
        try:
            if message.from_user.id in self.user_step:
                self.user_step.remove(message.from_user.id)
                if (message.reply_to_message is not None and message.reply_to_message.content_type != 'photo') and message.content_type != 'photo':
                    tryTosendMsg(message, "Message sent isn't a photo , cancelling photo modification command!", self.bot)
                else:
                    self.send_photo_message(message,'image',"https://api.deepai.org/api/torch-srgan",self.getImageUrl(message))
            else:
                if message.content_type == 'text':
                    ModuleCommandChecker.checkCommand(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_modified_photo)
        except Exception as e:
            print(e)

    def send_photoToonify(self,message):
        try:
            if message.from_user.id in self.user_step:
                self.user_step.remove(message.from_user.id)
                if (message.reply_to_message is not None and message.reply_to_message.content_type != 'photo') and message.content_type != 'photo':
                    tryTosendMsg(message, "Message sent isn't a photo , cancelling photo modification command!",
                                 self.bot)

                else:
                    self.send_photo_message(message,'image',"https://api.deepai.org/api/toonify",self.getImageUrl(message))
            else:
                if message.content_type == 'text':
                    ModuleCommandChecker.checkCommand(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_photoToonify)

        except Exception as e:
            print(e)
    def send_photobw(self,message):
        try:

            if message.from_user.id in self.user_step:
                self.user_step.remove(message.from_user.id)
                if (message.reply_to_message is not None and message.reply_to_message.content_type != 'photo') and message.content_type != 'photo':
                    tryTosendMsg(message, "Message sent isn't a photo , cancelling photo modification command!",
                                 self.bot)

                else:
                    self.send_photo_message(message,'image',"https://api.deepai.org/api/colorizer",self.getImageUrl(message))
            else:
                if message.content_type == 'text':
                    ModuleCommandChecker.checkCommand(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_photobw)

        except Exception as e:
            print(e)
    def getImageUrl(self,message):
        if message.content_type == 'photo':
            if len(message.photo) == 1:
                url = self.bot.get_file_url(message.photo[0].file_id)
            elif len(message.photo) == 2:
                url = self.bot.get_file_url(message.photo[1].file_id)
            elif len(message.photo) == 3:
                url = self.bot.get_file_url(message.photo[2].file_id)
            elif len(message.photo) == 4:
                url = self.bot.get_file_url(message.photo[3].file_id)
            elif len(message.photo) == 5:
                url = self.bot.get_file_url(message.photo[4].file_id)
            return url
        elif message.reply_to_message.content_type == 'photo':
            if len(message.reply_to_message.photo) == 1:
                url = self.bot.get_file_url(message.reply_to_message.photo[0].file_id)
            elif len(message.reply_to_message.photo) == 2:
                url = self.bot.get_file_url(message.reply_to_message.photo[1].file_id)
            elif len(message.reply_to_message.photo) == 3:
                url = self.bot.get_file_url(message.reply_to_message.photo[2].file_id)
            elif len(message.reply_to_message.photo) == 4:
                url = self.bot.get_file_url(message.reply_to_message.photo[3].file_id)
            elif len(message.reply_to_message.photo) == 5:
                url = self.bot.get_file_url(message.reply_to_message.photo[4].file_id)
            return url
    def send_photo_message(self,message,type,urlService,url):
        try:
            r = requests.post(
                urlService,
                data={
                    type: url,
                },
                headers={'api-key': '282bb452-77d1-4561-a7d2-d750058fffd6'}
            )
            response = r.text
            dictionary = json.loads(response)
            if 'err' in dictionary:
                tryTosendMsg(message,  f"An error occurred processing photo", self.bot)
            else:
                apiurl = dictionary['output_url']
                saveImg = dictionary['id'] + ".jpg"
                r = requests.get(apiurl, allow_redirects=True)
                open(saveImg, 'wb').write(r.content)
                photo = open(saveImg, 'rb')
                self.bot.send_photo(message.chat.id, photo, "Here is your photo!", message.id)
                photo.close()
                if os.path.exists(saveImg):
                    os.remove(saveImg)
        except Exception as e:
            print(e)

    def help_mod(self):
        help_string =f"Help of {self.mod_name}\n"+\
              f"/upscaleimage - upscale image without losing details\n"+\
              f"/colorbwphoto - black and white photo to color\n"+\
              f"/modifyphoto - modify photo to cartoony"

        return help_string