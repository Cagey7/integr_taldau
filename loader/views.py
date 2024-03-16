import time
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection, transaction
from .models import Chapter, IndexPeriod, Index, Dic, IndexDics, DatePeriod
from .utils import *


class InsertAllChapters(APIView):
    def post(self, request):
        catalogs = get_all_catalogs()
        if "status" in catalogs and catalogs["status"] == "error":
            return Response({"status": "error", "error_code": catalogs["error_code"]}, status=status.HTTP_200_OK)
        chapters_amount = 0
        for catalog in catalogs:
            if not Chapter.objects.filter(id=catalog[0]).exists():
                chapters_amount += 1
                Chapter.objects.create(id=catalog[0], name=catalog[1], parent_id=catalog[2])
        
        return Response({"status": "success", "new_chapters": chapters_amount}, status=status.HTTP_201_CREATED)


class InsertAllPeriods(APIView):
    def post(self, request):
        periods = get_all_periods()
        if "status" in periods and periods["status"] == "error":
            return Response({"status": "error", "error_code": periods["error_code"]}, status=status.HTTP_200_OK)

        periods_amount = 0
        for period in periods:
            if not IndexPeriod.objects.filter(id=int(period["id"])).exists():
                periods_amount += 1
                IndexPeriod.objects.create(id=period["id"], name=period["text"])

        return Response({"status": "success", "new_periods": periods_amount}, status=status.HTTP_201_CREATED)
    

class InsertAllIndices(APIView):
    def post(self, request):
        chapters_ids =  ",".join(map(str, Chapter.objects.values_list("id", flat=True)))
        period_ids = ",".join(map(str, IndexPeriod.objects.values_list("id", flat=True)))
        indices = get_all_indices(chapters_ids, period_ids)
        if "status" in indices and indices["status"] == "error":
            return Response({"status": "error", "error_code": indices["error_code"]}, status=status.HTTP_200_OK)
        
        indices_amount = 0
        for index in indices["results"]:
            if not Index.objects.filter(id=int(index["id"])).exists():
                indices_amount += 1
                Index.objects.create(id=index["id"], name=index["Name"])
        
        return Response({"status": "success", "new_indices": indices_amount}, status=status.HTTP_201_CREATED)


class AddOneIndexInfo(APIView):
    def post(self, request):
        index_id = request.data.get("index_id")

        if index_id is None:
            return Response({"status": "error", "error_info": "Не все данные были предоставлены"}, status=status.HTTP_400_BAD_REQUEST)


        with transaction.atomic():
            index = Index.objects.select_for_update().get(id=index_id)
            
            time.sleep(2)
            index_info = get_index_attributes(index_id)
            if "status" in index_info and index_info["status"] == "error":
                raise Exception("Ошибка в талдау")
            
            chapter_id = int(index_info["path"].split("/")[-1])
            chapter = Chapter.objects.get(id=chapter_id)
            index.chapter = chapter
            index.save()
            
            time.sleep(2)
            periods = get_index_periods(index_id)
            if "status" in periods and periods["status"] == "error":
                raise Exception("Ошибка в талдау")
            
            for period in periods:
                time.sleep(2)
                period_obj = IndexPeriod.objects.get(id=period["id"])
                segments = get_index_segment(index_id, period["id"])
                if "status" in segments and segments["status"] == "error":
                    raise Exception("Ошибка в талдау")
                for segment in segments:
                    dic_ids = convert_to_list(segment["dicId"])
                    dic_names = convert_to_list(segment["names"])
                    term_ids = convert_to_list(segment["termIds"])
                    
                    dics = Dic.objects.filter(dic_ids=dic_ids).first()
                    if not dics:
                        dics = Dic(dic_ids=dic_ids, dic_names=dic_names, term_ids=term_ids)
                        dics.save()
                    
                    index_dics = IndexDics.objects.filter(index=index, dics=dics, period=period_obj).first()
                    if not index_dics:
                        index_dics = IndexDics(index=index, dics=dics, period=period_obj, dates=[])
                        index_dics.save()


        return Response({"status": "success"}, status=status.HTTP_200_OK)


class InsertIndexData(APIView):
    def post(self, request):
        index_id = request.data.get("index_id")
        index = Index.objects.get(id=index_id)
        index_insert_data = IndexDics.objects.filter(index=index)

        with transaction.atomic():
            with connection.cursor() as cursor:
                for one_index in index_insert_data:
                    dic = one_index.dics
                    period = one_index.period
                    dates = one_index.dates
                    dic_ids = dic.dic_ids
                    term_ids = dic.term_ids
                    for dic_id in dic_ids:
                        create_dic_table(cursor, dic_id)
                    create_index_table(cursor, index_id, period.id, dic_ids)
                    term_ids_str = ",".join(map(str, term_ids))
                    dic_ids_str = ",".join(map(str, dic_ids))
                    time.sleep(2)
                    dates = get_index_dates(index_id, period.id, term_ids_str, dic_ids_str)
                    if "status" in dates and dates["status"] == "error":
                        raise Exception("Ошибка в талдау")
                    for date_id, date_name in zip(dates["datesIds"], dates["periodNameList"]):
                        date_id = int(date_id)
                        date_exists = DatePeriod.objects.filter(id=date_id).first()
                        if not date_exists:
                            date = DatePeriod(id=date_id, name=date_name, index_period=period)
                            date.save()
                    
                    index_dics = IndexDics.objects.get(index=index, dics=dic, period=period)
                    taldau_dates = [int(date) for date in dates["datesIds"]]
                    new_dates = set(index_dics.dates) ^ set(taldau_dates)
                    if new_dates:
                        index_dics.dates = index_dics.dates + list(new_dates)
                        index_dics.save()
                    else:
                        continue

                    time.sleep(2)
                    new_dates_str = ",".join(map(str, new_dates))
                    index_values = get_index_data(index_id, period.id, dic_ids_str, new_dates_str)
                    if "status" in index_values and index_values["status"] == "error":
                        raise Exception("Ошибка в талдау")
                    for values in index_values:
                        for term_id, term_name, dic_id in zip(values["terms"], values["termNames"], dic_ids):
                            insert_term(cursor, dic_id, int(term_id), term_name)
                        for val in values["periods"]:
                            date_now = datetime.now()
                            taldau_date = datetime.strptime(val["date"], "%d.%m.%Y")
                            date_period_id = DatePeriod.objects.get(name=val["name"]).id
                            period_values = get_period_values(period.id, taldau_date)
                            if val["value"] == "x":
                                val["value"] = -1
                            data_index_insert = [val["value"], taldau_date, date_now, date_period_id] + period_values + values["terms"]
                            insert_index_data(cursor, index_id, period.id, dic_ids, data_index_insert)
                    print("-1")

        return Response({"status": "success"}, status=status.HTTP_200_OK)
