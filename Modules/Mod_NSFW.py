from Modules.Base import Mod_Base
from Modules.UsefulMethods import WORNGMSG
import requests
import json
class Mod_NSFW(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_NSFW,self).__init__("NSFW",["/enable_nsfw_detection","/disable_nsfw_detection",
                                              "/show_nsfw_detection_status"],
                                        [])

    def handleOnCommand(self,message,name):
        try:
            if name == "/enable_nsfw_detection":
                resp = self.insert_nsfw_status(message.chat.id)
                if resp =="ok":
                    self.bot.reply_to(message,"NSFW detection enabled")
                else:
                    self.bot.reply_to(message, resp)
            if name =="/disable_nsfw_detection":
                resp = self.delete_nsfw_status(message.chat.id)
                self.bot.reply_to(message,resp)
            if name=="/show_nsfw_detection_status":
                resp = self.get_NsfwStatus(message.chat.id)
                if isinstance(resp,str):
                    self.bot.reply_to(message,WORNGMSG)
                else:
                    if len(resp)>0:
                        self.bot.reply_to(message,"NSFW detection enabled")
                    else:
                        self.bot.reply_to(message, "NSFW detection disbaled")




        except Exception as e:
            self.bot.reply_to(message,WORNGMSG)



    def getEveryMessageMethod(self,message):
        try:
            if message.content_type == 'photo' :
                resp = self.get_NsfwStatus(message.chat.id)
                if not isinstance(resp,str):
                    if len(resp)>0:

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

                        self.send_nsfw_message(message,url)

        except:
            pass
    def send_nsfw_message(self,message,url):
        try:
            r = requests.post(
                "https://api.deepai.org/api/nsfw-detector",
                data={
                    'image': url,
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
    def help_mod(self):
        help =f"Help of {self.mod_name}\n"+\
              f"/enable_nsfw_detection - enable nsfw detection\n"+\
              f"/disable_nsfw_detection - disbale nsfw detection\n"\
              f"/show_nsfw_detection_status - get if your server nsfw status"
        return help