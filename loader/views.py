from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import *
from .utils import *


class InsertAllChapters(APIView):
    def post(self, request):
        catalogs = get_all_catalogs()
        if "status" in catalogs and catalogs["status"] == "error":
            return Response({"status": "error", "error_code": catalogs["error_code"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            return Response({"status": "error", "error_code": periods["error_code"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response({"status": "error", "error_code": indices["error_code"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        indices_amount = 0
        for index in indices["results"]:
            if not Index.objects.filter(id=int(index["id"])).exists():
                indices_amount += 1
                Index.objects.create(id=index["id"], name=index["Name"])
        
        return Response({"status": "success", "new_indices": indices_amount}, status=status.HTTP_201_CREATED)


class AddOneIndexInfo(APIView):
    @swagger_auto_schema(request_body=IndexIdFilterSerializer, responses={})
    def post(self, request):
        serializer = IndexIdFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        index_id = serializer.data["index_id"]
        try:
            check_filters = serializer.data["check_filters"]
            info = add_one_index_info(index_id, check_filters)
        except:
            info = add_one_index_info(index_id)

        return Response({"status": "success", "info": info}, status=status.HTTP_201_CREATED)


class AddAllIndexInfo(APIView):
    def post(self, request):
        indices = Index.objects.filter(chapter=None)
        info = []
        for index in indices:
            one_info = add_one_index_info(index.id)
            info.append(one_info)
        
        return Response({"status": "success", "info": info}, status=status.HTTP_201_CREATED)


class InsertIndexData(APIView):
    @swagger_auto_schema(request_body=IndexIdSerializer, responses={})
    def post(self, request):
        serializer = IndexIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        index_id = serializer.data["index_id"]
        index = Index.objects.get(id=index_id)
        index_insert_data = IndexDics.objects.filter(index=index)
        info = []
        for index_insert_data_one in index_insert_data:
            insert_info = insert_index_data_param(index_insert_data_one)
            info.append(insert_info)

        return Response({"status": "success", "info": info}, status=status.HTTP_201_CREATED)


class InsertIndexDataParam(APIView):
    @swagger_auto_schema(request_body=IndexInfoSerializer, responses={})
    def post(self, request):
        serializer = IndexInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        index_id = serializer.data["index_id"]
        period_id = serializer.data["period_id"]
        dic_ids = serializer.data["dic_ids"]
        index = Index.objects.get(id=index_id)
        period = IndexPeriod.objects.get(id=period_id)
        dics = Dic.objects.get(dic_ids=dic_ids)
        index_insert_data_one = IndexDics.objects.get(index=index, period=period, dics=dics)
        info = insert_index_data_param(index_insert_data_one)

        return Response({"status": "success", "info": info}, status=status.HTTP_201_CREATED)
