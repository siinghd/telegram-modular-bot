from telebot import types

from Modules.Base import Mod_Base
from Modules.ClassHelpers.Movies import Movies
from Modules.UsefulMethods import getmessageInCommand,WORNGMSG
class Mod_Movies(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_Movies,self).__init__("Movies",["/_addmovie","/getmovie","/ask_report_movie","/_dmovie"],
                                        ["Select you search", "Delete movie"])

    def handleOnCommand(self,message,name):
        try:
            if name == "/_addmovie":
                textMessageParams = getmessageInCommand(message,"/_addmovie",",")
                if len(textMessageParams)>0:
                    movie = Movies(message.id,textMessageParams[0].lower(),textMessageParams[1],None)
                    resp = self.insert_movie(movie)
                    if resp == "ok":
                        self.bot.reply_to(message, "Done, movie added")
                    else:
                        self.bot.reply_to(message, resp)
                else:
                    self.bot.reply_to(message, "Pass arguments")

            elif name =="/_dmovie":
                movieName= getmessageInCommand(message, "/_dmovie", None)
                if len(movieName)>0:
                    array_Matching_films = self.get_Movies(movieName.lower(),"NAME")
                    if isinstance(array_Matching_films, str):
                        self.bot.reply_to(array_Matching_films)
                    else:
                        if len(array_Matching_films)==0:
                            self.bot.reply_to("No Movie found!")
                        else:
                            self.send_Search(message,array_Matching_films,"Delete movie")

                else:
                    self.bot.reply_to(message, "Pass arguments")
            elif name =="/getmovie":
                movieName= getmessageInCommand(message, "/getmovie", None)
                if len(movieName)>0:
                    array_Matching_films = self.get_Movies(movieName.lower() ,"NAME")
                    if isinstance(array_Matching_films, str):
                        self.bot.reply_to(message,array_Matching_films)
                    else:
                        if len(array_Matching_films)==0:
                            self.bot.reply_to(message,"No Movie found!")
                        else:
                            self.send_Search(message,array_Matching_films,"Select you search")

                else:
                    self.bot.reply_to(message, "Please provide movie name\nExample:\n/search Avengers End game")
            elif name == "/ask_report_movie":
                messageOfUser = getmessageInCommand(message, "/ask_report_movie", None)
                if len(messageOfUser) > 0:
                    try:
                        self.bot.send_message(-1001477281571, messageOfUser)
                        self.bot.reply_to(message, "Done ,message sent.\nCheck in some hour the same movie asked.")
                    except:
                        self.bot.reply_to(message, WORNGMSG)
                else:
                    self.bot.reply_to(message,
                                      "Please provide a message\nExample:\n/ask_report_movie Can you add Avenger "
                                      "end game? OR Avenger end link doesn't work can you change it?")
        except Exception as e:
            print(e)

    def insert_movie(self,movies):
        try:
            self.cursor.execute(
                f"INSERT INTO movies VALUES ({movies.id},'{movies.name}','{movies.link}','{movies.created_at}')")
            return "ok"
        except Exception as e:
            return WORNGMSG

    def get_Movies(self,name_id,action):
        try:
            if action=="NAME":
                self.cursor.execute(f"""Select * from movies WHERE name LIKE '%{name_id}%'""")
            elif action=="ID":
                self.cursor.execute(f"""Select * from movies WHERE id={name_id}""")
            items =  self.cursor.fetchall()
            arrayi = []
            for i in items:
                movie = Movies(i[0],i[1],i[2],i[3])
                arrayi.append(movie)

            return arrayi
        except Exception:
            return WORNGMSG

    def deleteMovie(self,movie):
        try:
             self.cursor.execute(f"""DELETE FROM movies
                                    WHERE id={movie.id}""")
             count = self.cursor.rowcount
             if count>0:
                 return "Movie deleted!"
        except Exception:
            return WORNGMSG
    def help_mod(self):
        help =f"Help of {self.mod_name}\n"+\
              f"/getmovie - search movie providing movie name)\n"+\
              f"/ask_report_movie - Ask movie or report any problem"
        return help

    def send_Search(self, message,array_Matching_films, param):
        self.user_step.append(message.from_user.id)
        try:

            markup = types.InlineKeyboardMarkup()
            buttons = []
            for movie in array_Matching_films:
                buttons.append(types.InlineKeyboardButton(text=movie.name, callback_data=movie.id))

            buttons.append(types.InlineKeyboardButton(text="Cancel", callback_data="Cancel"))
            for button in buttons:
                markup.row(button)

            self.bot.send_message(message.chat.id, param, reply_markup=markup)
        except Exception as e :
            self.bot.reply_to(message,WORNGMSG)

    def callBackHandler(self,call,name):
        if call.from_user.id in self.user_step:
            self.user_step.remove(call.from_user.id)
            if "Cancel" in call.data:
                self.bot.delete_message(call.message.chat.id, call.message.id)
            else:
                if "Select you search" == name:
                    movies = self.get_Movies(call.data,"ID")
                    if isinstance(movies, str):
                        self.bot.reply_to(call.message,movies)
                        self.bot.delete_message(call.message.chat.id, call.message.id)
                    else:
                        msg_to_send =f"<b>How to download </b>: \n"\
                                    f"If you see a video player :\n" \
                                    f"From Mobile tap on the video player until the popup appear and click download.\n"\
                                    f"From Desktop/Pc Click on the three dots and then download.\n"\
                                    f"If you see download button just click on it :)"\
                                    f"If you se any other things just try to figure out how to download it :)\n"\
                                    f"<a href='{movies[0].link}'>Download {movies[0].name}</a>"
                        self.bot.reply_to(call.message,msg_to_send)
                        self.bot.delete_message(call.message.chat.id, call.message.id)
                if "Delete movie" == name:
                    movies = self.get_Movies(call.data,"ID")
                    if isinstance(movies, str):
                        self.bot.reply_to(call.message,movies)
                        self.bot.delete_message(call.message.chat.id, call.message.id)
                    else:
                        resp = self.deleteMovie(movies[0])
                        self.bot.reply_to(call.message,resp)
                        self.bot.delete_message(call.message.chat.id, call.message.id)