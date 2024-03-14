from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chapter, IndexPeriod, Index
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
        
        return Response({"status": "ok", "new_chapters": chapters_amount}, status=status.HTTP_200_OK)


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

        return Response({"status": "ok", "new_periods": periods_amount}, status=status.HTTP_200_OK)
    

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
        
        return Response({"status": "ok", "new_indices": indices_amount}, status=status.HTTP_200_OK)

