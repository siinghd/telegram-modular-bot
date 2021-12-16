from Modules.Base import Mod_Base
from Modules.UsefulMethods import WORNGMSG ,getmessageInCommand,NOTADMIN,getBotIsAdmin,BOTNOTADMIN,tryTosendMsg,isOwner,getIsAdmin
import requests
import json
class Mod_NSFW(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_NSFW,self).__init__("NSFW",["/enable_nsfw_detection","/disable_nsfw_detection",
                                              "/show_nsfw_detection_status",
                                              "/nsfw_image"],
                                        [])

    def handleOnCommand(self,message,name):
        try:
            print(message)
            if getBotIsAdmin(self.bot, message):
                if isOwner(message) or getIsAdmin(self.bot,message):
                    if name == "/enable_nsfw_detection":
                        resp = self.insert_nsfw_status(message.chat.id)
                        if resp =="ok":
                            tryTosendMsg(message,"NSFW detection enabled",self.bot)

                        else:
                            tryTosendMsg(message,resp,self.bot)

                    if name =="/disable_nsfw_detection":
                        resp = self.delete_nsfw_status(message.chat.id)
                        tryTosendMsg(message,resp,self.bot)

                    if name=="/show_nsfw_detection_status":
                        resp = self.get_NsfwStatus(message.chat.id)
                        if isinstance(resp,str):
                            tryTosendMsg(message,WORNGMSG,self.bot)

                        else:
                            if len(resp)>0:
                                tryTosendMsg(message,"NSFW detection enabled",self.bot)

                            else:
                                tryTosendMsg(message, "NSFW detection disbaled",self.bot)
                else:
                    tryTosendMsg(message, NOTADMIN, self.bot)
            else:
                tryTosendMsg(message,BOTNOTADMIN,self.bot)
            
            if name == "/nsfw_image":
                textMessageParams = getmessageInCommand(message,"/nsfw_image"," ")
                if len(textMessageParams) > 0:
                    self.getNsfwImage(message,textMessageParams)
                else:
                    tryTosendMsg(message,"Please include type of nsfw image", self.bot)
            





        except Exception as e:
            print(e)
            tryTosendMsg(message,WORNGMSG,self.bot)




    def getEveryMessageMethod(self,message):
        try:
            if message.content_type == 'photo' or message.content_type == 'animation':
                resp = self.get_NsfwStatus(message.chat.id)
                if not isinstance(resp,str):
                    if len(resp)>0:
                        if message.content_type == 'photo':
                            if len(message.photo) == 1:
                                url = self.bot.get_file_url(message.photo[0].file_id)
                            elif len(message.photo) == 2:
                                url =  self.bot.get_file_url(message.photo[1].file_id)
                            elif len(message.photo) == 3:
                                url =  self.bot.get_file_url(message.photo[2].file_id)
                            elif len(message.photo) == 4:
                                url =  self.bot.get_file_url(message.photo[3].file_id)
                            elif len(message.photo) == 5:
                                url =  self.bot.get_file_url(message.photo[4].file_id)

                            self.send_nsfw_message(message,'image',url)
                        else:
                            url = self.bot.get_file_url(message.animation.file_id)
                            self.send_nsfw_message(message,'video' ,url)

        except:
            pass
    def send_nsfw_message(self,message,type,url):
        try:
            r = requests.post(
                "https://api.deepai.org/api/nsfw-detector",
                data={
                    type: url,
                },
                headers={'api-key': '282bb452-77d1-4561-a7d2-d750058fffd6'}
            )
            response = r.text
            dictionary = json.loads(response)
            if dictionary["output"]["nsfw_score"] > 0.65:
                self.bot.send_message(message.chat.id,
                                      f"Deleting last image from : {message.from_user.first_name}! NSFW Content detected!")
                self.bot.delete_message(message.chat.id, message.id)
        except:
            pass
    def insert_nsfw_status(self,id):
        try:
            self.cursor.execute(f"""Select * from nsfw WHERE id={id}""")
            items =  self.cursor.fetchall()
            if len(items)==0:
                self.cursor.execute(
                    f"INSERT INTO nsfw VALUES ({id})")
                return "ok"
            else:
                return "NSFW detection already enabled"
        except Exception as e:
            return WORNGMSG
    def get_NsfwStatus(self,id):
        try:
            self.cursor.execute(f"""Select * from nsfw WHERE id={id}""")
            items =  self.cursor.fetchall()
            arrayi = []
            for i in items:
                arrayi .append(i[0])
            return arrayi
        except Exception:
            return WORNGMSG
    def delete_nsfw_status(self,id):
        try:
             self.cursor.execute(f"""DELETE FROM nsfw
                                    WHERE id={id}""")
             count = self.cursor.rowcount
             if count>0:
                 return "NSFW detection disabled!"
        except Exception:
            return WORNGMSG
    
    def getNsfwImage(self,msg,params):
        try:
            r = requests.get(
                f"https://nekobot.xyz/api/image?type={params[0]}",
            )
            response = r.text
            dictionary = json.loads(response)
            print(dictionary)
            if dictionary['success']:
                tryTosendMsg(msg,dictionary['message'],self.bot)
            else:
                tryTosendMsg(msg, WORNGMSG, self.bot)
        except Exception as e:
            print(e)
            tryTosendMsg(msg,"Something went wrong retry!", self.bot)
    
    def help_mod(self):
        help_string =f"Help of {self.mod_name}\n"+\
              f"/enable_nsfw_detection - enable nsfw detection\n"+\
              f"/disable_nsfw_detection - disbale nsfw detection\n"+\
              f"/show_nsfw_detection_status - get if your server nsfw status"+\
              f"/nsfw_image image type - get nsfw image"
        return help_string
    