
from moviepy.editor import *
from pytube import YouTube
from Modules.Base import Mod_Base
import os
from Modules.UsefulMethods import getmessageInCommand,WORNGMSG,tryTosendMsg

class Mod_Youtube(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_Youtube,self).__init__("Youtube",["/tomp3","/towav","/tomp4"],
                                        [])

    def handleOnCommand(self,message,name):
        try:
            if name == "/tomp3":
                textMessageParams = getmessageInCommand(message,"/tomp3",None)
                if len(textMessageParams)>0 and "youtu" in textMessageParams:
                    tryTosendMsg(message, "Converting...", self.bot)
                    self.sendFileDownloaded(message,textMessageParams,"mp3")
                else:
                    tryTosendMsg(message, "Please provide youtube link.\n/tomp3 link", self.bot)

            elif name =="/towav":
                textMessageParams = getmessageInCommand(message, "/towav", None)
                if len(textMessageParams) > 0 and "youtu" in textMessageParams:

                    tryTosendMsg(message, "Converting...", self.bot)

                    self.sendFileDownloaded(message, textMessageParams, "wav")
                else:
                    tryTosendMsg(message, "Please provide youtube link.\n/towav link", self.bot)

            elif name =="/tomp4":
                textMessageParams = getmessageInCommand(message, "/tomp4", None)
                if len(textMessageParams) > 0 and "youtu" in textMessageParams:
                    tryTosendMsg(message,  "Converting...", self.bot)

                    self.sendFileDownloaded(message, textMessageParams, "mp4")
                else:
                    tryTosendMsg(message,  "Please provide youtube link.\n/tomp4 link", self.bot)

        except Exception as e:
            print(e)

    def sendFileDownloaded(self,message,textMessageParams, param):
        try:
            mp4= YouTube(textMessageParams).streams.get_highest_resolution().download()
            video_clip= VideoFileClip(mp4)
            if param!="mp4":
                mp3wav = mp4.split(".mp4",1)[0]+f".{param}"
                audio_clip= video_clip.audio
                audio_clip.write_audiofile(mp3wav)
                f = open(mp3wav, "rb")
                try:
                    self.bot.send_audio(message.chat.id,f)
                except Exception as e:
                    tryTosendMsg(message, WORNGMSG, self.bot)

                    print(e)
                    f.close()
                    audio_clip.close()
                    if os.path.exists(mp3wav):
                        os.remove(mp3wav)

                f.close()
                audio_clip.close()
                if os.path.exists(mp3wav):
                    os.remove(mp3wav)

            else:
                if os.path.getsize(mp4)<52428800:
                    f = open(mp4, "rb")

                    try:
                        self.bot.send_video(message.chat.id, f)
                    except Exception as e:
                        tryTosendMsg(message, WORNGMSG, self.bot)

                        print(e)
                        f.close()
                        video_clip.close()
                        if os.path.exists(mp4):
                            os.remove(mp4)
                    f.close()
                    video_clip.close()

                else:
                    tryTosendMsg(message,"File i bigger then 50MB :/", self.bot)

            if os.path.exists(mp4):
                os.remove(mp4)
        except Exception as e:
            print(e)
            tryTosendMsg(message, WORNGMSG, self.bot)

    def callBackHandler(self,call,name):
        if call.from_user.id in self.user_step:
            self.user_step.remove(call.from_user.id)
            if "Cancel" in call.data:
                self.bot.delete_message(call.message.chat.id, call.message.id)
            else:
                pass
    def help_mod(self):
        help_string =f"Help of {self.mod_name}\n"+\
              f"/tomp3 - convert youtube video to mp3\n"+\
              f"/towav - convert youtube video to wav\n"\
              f"/tomp4 - convert youtube video to mp4"
        return help_string