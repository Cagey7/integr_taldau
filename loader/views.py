import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chapter, IndexPeriod, Index, Dic, IndixDics, DatePeriod
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
        index = Index.objects.get(id=index_id)
        if index.chapter:
            return Response({"status": "success", "status_info": "Раздел показателя уже загружен"}, status=status.HTTP_200_OK)
        time.sleep(2)
        index_info = get_index_attributes(index_id)
        if "status" in index_info and index_info["status"] == "error":
            return Response({"status": "error", "error_code": index_info["error_code"]}, status=status.HTTP_200_OK)
        
        chapter_id = int(index_info["path"].split("/")[-1])
        chapter = Chapter.objects.get(id=chapter_id)
        index.chapter = chapter
        
        time.sleep(2)
        periods = get_index_periods(index_id)
        if "status" in periods and periods["status"] == "error":
            return Response({"status": "error", "error_code": periods["error_code"]}, status=status.HTTP_200_OK)
        
        for period in periods:
            time.sleep(2)
            period_obj = IndexPeriod.objects.get(id=period["id"])
            segments = get_index_segment(index_id, period["id"])
            if "status" in segments and segments["status"] == "error":
                return Response({"status": "error", "error_code": segments["error_code"]}, status=status.HTTP_200_OK)
            for segment in segments:
                dic_ids = convert_to_list(segment["dicId"])
                dic_names = convert_to_list(segment["names"])
                term_ids = convert_to_list(segment["termIds"])
                dics = Dic(dic_ids=dic_ids, dic_names=dic_names, term_ids=term_ids)
                index_dics = IndixDics(index=index,dics=dics, period=period_obj, dates=[])
        

        dics.save()
        index_dics.save()
        index.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)

