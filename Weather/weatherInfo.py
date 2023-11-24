from weatherapi.weatherapi_client import WeatherapiClient
import json
class WeatherInfo:
    _APIKEY = ""

    def __init__(self):
        self.client = WeatherapiClient(self._APIKEY)
        self.ap_is_controller = self.client.ap_is

    def getWeatherInfo(self,location,language):
        q = location
        try :
            result = self.ap_is_controller.get_realtime_weather(q, language)
        except Exception:
            string = "No location found :"+location
            return string
        location= result.location.name +" , "+result.location.region+" , "+result.location.country
        if(result.current.is_day==1):
            isday="☀"
        else:
            isday="🌃"
        dic = dict(loc=location,temp=result.current.temp_c,timeLocal=result.location.localtime,lastupdate=result.current.last_updated,
                   tempflike = result.current.feelslike_c,wcondition=result.current.condition.text,
                   winkhp=result.current.wind_kph,windeg=result.current.wind_degree,
                   presin=result.current.pressure_in,prec_mm=result.current.precip_mm,humidity=result.current.humidity,
                   clcover=result.current.cloud,uvIndex=result.current.uv,dayOrNight=isday)
        stringTemp = "<b>Today in  :\n{loc} | {timeLocal} </b>\n\n"+\
                 "<code><b>Last update</b> : {lastupdate}\n"+ \
                 "<b>Day or Night</b> : {dayOrNight}\n" + \
                 "<b>Weather condition</b> : {wcondition}  \n"+\
                 "<b>Wind in kph</b> : {winkhp}\n"+ \
                 "<b>Wind degree</b> : {windeg}\n" + \
                 "<b>Temperature in celsius</b> : {temp}\n"+ \
                 "<b>Feels like temperature in celsius</b> : {tempflike}\n" + \
                 "<b>Pressure inches</b> : {presin}\n"+\
                 "<b>Precipitation amount in millimeters</b> : {prec_mm}\n"+ \
                 "<b>Cloud cover</b> : {clcover}%\n" + \
                 "<b>Humidity</b> : {humidity}%\n"+ \
                 "<b>UV Index</b> : {uvIndex}%</code>"

        stringTemp=stringTemp.format(**dic)
        return stringTemp

    def getTime(self,location,language):
        q = location
        try :
            result = self.ap_is_controller.get_realtime_weather(q, language)
        except Exception:
            string = "No location found :"+location
            return string
        location= result.location.name +" , "+result.location.region+" , "+result.location.country

        dic = dict(loc=location,timeLocal=result.location.localtime)
        stringTime = "<b>Time in  :\n{loc}</b>\nis <code>{timeLocal}</code>"
        stringTemp=stringTime.format(**dic)
        return stringTemp