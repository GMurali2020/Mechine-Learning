from django.shortcuts import render
from rest_framework.serializers import Serializer
from django.http import JsonResponse,HttpResponse
import pandas as pd
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import JSONParser

from datetime import datetime



import json
import io
#data='5d'
class DateResultClass(APIView):
    def get(self,request):
        stream=io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        k_data=data['bno']
        df = pd.read_csv('./nifty50.csv')
        #print(df.head())
        df1 = pd.to_datetime(df['date'], format='%Y%m%d')
        df2 = pd.DataFrame(list(df1), columns=['date1'])
        l1 = []
        for x in df['time']:
            d = datetime.strptime(x, "%H:%M")
            l1.append(d.strftime("%I:%M %p"))

        df3 = pd.DataFrame(l1, columns=['time1'])
        df4 = pd.concat([df2, df3], axis=1)

        df5 = pd.concat([df.drop(['date', 'time', 'index'], axis=1), df4], axis=1)

        main_result = []
        weight = 0
        for x in range(int(k_data[0])):
            date = '2013-04-0{a}'.format(a=x + 1)
            df6 = df5[(df5['date1'] >= date) & (df5['date1'] <= date)]
            result = {"date": date + ' ' + df6['time1'][weight], "open": df6['open'].max(),
                      "high": df6['high'].max(),
                      "low": df6['low'].min(), "close": df6['close'].min()}

            main_result.append(result)
            weight += len(df6)
        return HttpResponse(json.dumps(main_result))
