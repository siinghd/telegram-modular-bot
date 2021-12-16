import json
import os
# from numpy import asarray
import requests
# from bounding_box import bounding_box as bb
import ModuleCommandChecker
from Modules.Base import Mod_Base
from Modules.UsefulMethods import WORNGMSG, tryTosendMsg
# from PIL import Image
import base64
class Mod_Photo(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_Photo,self).__init__("Photo",["/upscaleimage","/colorbwphoto","/modifyphoto","/toimage",'/restore','/bremove'],
                                        [])

    def handleOnCommand(self,message,name):
        try:
            if name == "/upscaleimage":
                if  message.reply_to_message is not None and  message.reply_to_message.content_type=="photo":
                    self.user_step.append(message.from_user.id)
                    self.send_modified_photo(message)
                else:
                    self.send_photoMsg(message,"Please send me photo",self.send_modified_photo)
            # if name == "/aboutimage":
            #     if message.reply_to_message is not None and message.reply_to_message.content_type == "photo":
            #         self.user_step.append(message.from_user.id)
            #         self.send_aboutImage(message)
            #     else:
            #         self.send_photoMsg(message, "Please send me photo", self.send_aboutImage)
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
            elif name=="/toimage":
                if message.reply_to_message is not None and message.reply_to_message.content_type == "text":
                    self.user_step.append(message.from_user.id)
                    self.send_createImage(message)
                else:
                    self.send_photoMsg(message, "Please send me a text from which you want to create the image", self.send_createImage)
            elif name=="/restore":
                if message.reply_to_message is not None and message.reply_to_message.content_type == "photo":
                    self.user_step.append(message.from_user.id)
                    self.send_restore_image(message)
                else:
                    self.send_photoMsg(message, "Please send me photo that need to be restored", self.send_restore_image)
            elif name=="/bremove":
                if message.reply_to_message is not None and message.reply_to_message.content_type == "photo":
                    self.user_step.append(message.from_user.id)
                    self.send_bremove_image(message)
                else:
                    self.send_photoMsg(message, "Please send me photo that need to be restored", self.send_bremove_image)

        except Exception as e:
            tryTosendMsg(message,WORNGMSG,self.bot)




    def getEveryMessageMethod(self,message):
        pass

    def send_photoMsg(self, message,msg,method):
        self.user_step.append(message.from_user.id)
        tryTosendMsg(message,msg,self.bot)
        self.bot.register_next_step_handler_by_chat_id(message.chat.id, method)

    # def send_aboutImage(self,message):
    #     try:
    #         if message.from_user.id in self.user_step:
    #             self.user_step.remove(message.from_user.id)
    #             if (message.reply_to_message is not None and message.reply_to_message.content_type != 'photo') and message.content_type != 'photo':
    #                 tryTosendMsg(message, "Message sent isn't a photo , cancelling photo modification command!", self.bot)
    #             else:
    #                 self.send_photo_message(message,'image',"https://api.deepai.org/api/demographic-recognition",self.getImageUrl(message))
    #         else:
    #             if message.content_type == 'text':
    #                 ModuleCommandChecker.checkCommand(message)
    #             self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_aboutImage)
    #     except Exception as e:
    #         print(e)
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
    def send_restore_image(self,message):
        try:
            if message.from_user.id in self.user_step:
                self.user_step.remove(message.from_user.id)
                if (message.reply_to_message is not None and message.reply_to_message.content_type != 'photo') and message.content_type != 'photo':
                    tryTosendMsg(message, "Message sent isn't a photo , cancelling photo restoration command!", self.bot)
                else:
                    self.send_photo_message_hotpot(message,'restore',"https://cortex.hotpot.ai/restoration-api-bin",self.getImageUrl(message))
            else:
                if message.content_type == 'text':
                    ModuleCommandChecker.checkCommand(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_modified_photo)
        except Exception as e:
            print(e)
    def send_bremove_image(self,message):
        try:
            if message.from_user.id in self.user_step:
                self.user_step.remove(message.from_user.id)
                if (message.reply_to_message is not None and message.reply_to_message.content_type != 'photo') and message.content_type != 'photo':
                    tryTosendMsg(message, "Message sent isn't a photo , cancelling photo background remove command!", self.bot)
                else:
                    self.send_photo_message_hotpot(message,'bremove',"https://api.hotpot.ai/remove-background",self.getImageUrl(message))
            else:
                if message.content_type == 'text':
                    ModuleCommandChecker.checkCommand(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_modified_photo)
        except Exception as e:
            print(e)
    def send_createImage(self,message):
        try:
            if message.from_user.id in self.user_step:
                self.user_step.remove(message.from_user.id)
                if (message.reply_to_message is not None and message.reply_to_message.content_type != 'text') and message.content_type != 'text':
                    tryTosendMsg(message, "Message sent isn't a text , cancelling /toimage command!", self.bot)
                else:
                    self.send_photo_message(message,'text',"https://api.deepai.org/api/text2img",message.text)
            else:
                if message.content_type == 'text':
                    ModuleCommandChecker.checkCommand(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.send_createImage)
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
                if 'output_url'in dictionary:
                    apiurl = dictionary['output_url']
                    saveImg = dictionary['id'] + ".jpg"
                    r = requests.get(apiurl, allow_redirects=True)
                    open(saveImg, 'wb').write(r.content)
                    photo = open(saveImg, 'rb')
                    self.bot.send_photo(message.chat.id, photo, "Here is your photo!", message.id)
                    photo.close()
                # elif "output" in dictionary:
                #     saveImg = dictionary['id'] + ".jpg"
                #     r = requests.get(url, allow_redirects=True)
                #     open(saveImg, 'wb').write(r.content)
                #     if len(dictionary["output"][ "faces"])!=0:
                #         photo = Image.open(saveImg)
                #         data = asarray(photo).copy()
                #         for face in dictionary["output"][ "faces"]:
                #             print(face["bounding_box"][0])
                #             left= face["bounding_box"][0]
                #             top=face["bounding_box"][1]
                #             right= face["bounding_box"][2]
                #             bottom= face["bounding_box"][3]
                #             label=f"""{face["cultural_appearance"]} , {face["gender"]} , {face["age_range"][0]}- {face["age_range"][1]}"""
                #             bb.add(data,  left, top, right+200, bottom+200, label, "green")
                #         image2 = Image.fromarray(data)
                #         self.bot.send_photo(message.chat.id, image2, "Here is your photo!", message.id)
                #     else:
                #         tryTosendMsg(message,"No face found in this image",self.bot)
                if os.path.exists(saveImg):
                    os.remove(saveImg)
        except Exception as e:
            print(e)
    def send_photo_message_hotpot(self,message,type,urlService,url):
        savedImage = 'imgrestore.jpg'
        restore_savedImage = 'restoredimage.png'
        try:
            if type == 'restore':
                r = requests.get(url, allow_redirects=True)
                open(savedImage, 'wb').write(r.content)
                photo = open(savedImage, 'rb')
                r = requests.post(
                    urlService,
                    data={
                        'requestId':'H2JeH',
                        'withScratch': True
                    },
                    headers={'Authorization': 'yMHw4UidZM1Hha82AZtMjI50bYCfC3sdX7vvB'},files={'image': photo}
                )
            elif type == 'bremove':
                r = requests.get(url, allow_redirects=True)
                open(savedImage, 'wb').write(r.content)
                photo = open(savedImage, 'rb')
                r = requests.post(
                    urlService,
                    data={},
                    headers={'Authorization': '2oay998GQWDsw5YuAwBlC1R8tFVnlelZuMoPx3AAw36MC'},files={'image': photo}
                )

            open(restore_savedImage, 'wb').write(r.content)
            restored_photo = open(restore_savedImage, 'rb')
            if r.status_code == 200:
                self.bot.send_photo(message.chat.id, restored_photo, "Here is your photo!", message.id)
            else:
                tryTosendMsg(message,'Something went wrong, retry',self.bot)
            if os.path.exists(savedImage):
                os.remove(savedImage)
            if os.path.exists(restore_savedImage):
                os.remove(restore_savedImage)

        except Exception as e:
            print(e)
            tryTosendMsg(message, "Something went wrong, Retry later", self.bot)
    def help_mod(self):
        help_string =f"Help of {self.mod_name}\n"+\
              f"/upscaleimage - upscale image without losing details\n"+\
              f"/colorbwphoto - black and white photo to color\n"+ \
              f"/restore - restore old pic\n" + \
              f"/bremove - remove background"

        return help_string