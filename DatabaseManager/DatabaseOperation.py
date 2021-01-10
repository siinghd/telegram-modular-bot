from DatabaseManager.NewsSubscription import NewsSubscription
from DatabaseManager.User import User
from DatabaseManager.AfkStatus import AfkStatus


class DatabaseOperation:
    def insertGroup(self,group,cursor):
        try:
            cursor.execute("""Select group_id from groups where group_id={id}""".format(id=group._id))
            item = cursor.fetchall();
            if len(item)==0:
                cursor.execute("INSERT INTO groups VALUES (:group_id,:name,:created_At)",
                          {"group_id":group._id,"name":group._name,"created_At":group._timestamp})

            return "ok"
        except Exception:
            return "Something went wrong retry!"
    def insertnewSubscription(self, news_subscription, cursor):
            try:
                cursor.execute("""Select * from news_subscriptions where groupId={id} AND state='{state_}'""".format(id=news_subscription._groupId,state_=news_subscription._state))
                item = cursor.fetchall();
                if len(item)==0:
                    cursor.execute("INSERT INTO news_subscriptions VALUES (:id,:state,:time,:groupId,:subscription)",
                                  {"id":news_subscription._id,"state": news_subscription._state,"time": news_subscription._time, "groupId":  news_subscription._groupId,"subscription": news_subscription._subscription})
                    return "Subscription successfull!"
                else:
                    return self.update_subscription(item[0][0],news_subscription,1,cursor)
            except Exception:
                return "Something went wrong retry!"
    def insertUser(self,user,cursor):
        try:

            cursor.execute("""Select id , username from users where id={id}""".format(id=user._id))
            item = cursor.fetchall();

            if len(item)==0:
                cursor.execute("INSERT INTO users VALUES (:id,:is_bot,:first_name,:username,:last_name,:created_At)",
                          {"id":user._id,"is_bot":user._is_bot,"created_At":user._created_At,"first_name":user._first_name,
                           "username":user._username,"last_name":user._last_name})
            elif item[0][1]!=user._username:
                cursor.execute("""UPDATE users  SET username='{name}'
                                                    WHERE id={id}""".format(name=user._username,
                                                                                          id=user._id))
            return "ok"
        except Exception:
            return "Something went wrong retry!"
    def insertStatus(self,statusInfo,cursor):
        try:

            cursor.execute("""Select userId from afkstatus where userId={id}""".format(id=statusInfo._id))
            item = cursor.fetchall()
            if len(item)==0:
                cursor.execute("INSERT INTO afkstatus VALUES (:id,:message,:created_At)",
                          {"id":statusInfo._id,"message":statusInfo._message,"created_At":statusInfo._created_At})
            else:
                cursor.execute("UPDATE afkstatus SET message= '{messh}' where userId={user_}".format(user_=statusInfo._id,messh=statusInfo._message))

            return "ok"
        except Exception:
            return "Something went wrong retry!"
    def deleteStatus(self,id,cursor):
        try:

            cursor.execute("""Select userId from afkstatus where userId={id}""".format(id=id))
            item = cursor.fetchall();
            if len(item)==0:
                return "You have no AFK status to delete!"

            else:
                cursor.execute("""DELETE FROM afkstatus
            WHERE userId={id}""".format(id=id))
                return "AFK status deleted successfully"
        except Exception:
            return "Something went wrong retry!"
    def getNews_Subscriptions(self, cursor):
        try:
            cursor.execute("""Select id,state,time,groupId,subscription from news_subscriptions
                 JOIN groups ON news_subscriptions.groupId=groups.group_id WHERE subscription=1""")
            items = cursor.fetchall()
            arrayI = []
            for i in items:
                x = NewsSubscription(i[0],i[1],i[2],i[3],i[4])
                arrayI.append(x)

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    def getUserInfo(self, cursor):
        try:
            cursor.execute("""Select * from users""")
            items = cursor.fetchall()
            arrayI = []
            for i in items:
                x = User(i[0],i[1],i[2],i[3],i[4])
                arrayI.append(x)

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    def getUserStatusByID(self, id , cursor):
        try:
            cursor.execute("""Select userId, message,afkstatus.created_At, first_name  from afkstatus 
            JOIN users ON userId = id
            WHERE userId={id}""".format(id=id))
            items = cursor.fetchall()
            arrayI = []
            for i in items:
                x = AfkStatus(i[0],i[1],i[3],i[2])
                arrayI.append(x)

            return arrayI
        except Exception:
            return "Something went wrong retry!"

    def getUserByUsername(self, userName, cursor):
        try:
            cursor.execute("""Select id from users WHERE username='{username}'""".format(username=userName))
            items = cursor.fetchall()
            arrayI = []
            for i in items:
                arrayI.append(i[0])

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    def getNews_byGroupSubscriptions(self, cursor,groupId):
        try:
            cursor.execute("""Select id,state,time,groupId,subscription from news_subscriptions
                 JOIN groups ON news_subscriptions.groupId=groups.group_id WHERE subscription=1 AND groupId={id}""".format(id=groupId))
            items = cursor.fetchall()
            arrayI = []
            for i in items:
                x = NewsSubscription(i[0],i[1],i[2],i[3],i[4])
                arrayI.append(x)

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    def update_subscription(self,id,newsClass,subscription,cursor):
        try:

            if newsClass is None:
                cursor.execute("""UPDATE news_subscriptions
                                                    SET subscription = {subscription}
                                                    WHERE id={idmessage}""".format(subscription=subscription,
                                                                                          idmessage=int(id)))
                return "Cancelled succefully!"
            else:
                cursor.execute("""UPDATE news_subscriptions
                                    SET subscription = {subscription},
                                        time = '{time}'
                                    WHERE
                                        id={idmessage}""".format(subscription=subscription,time=newsClass._time,idmessage=id))
                return "Updated succefully!"
        except Exception:
            return "Something went wrong retry!"