from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chapters, Indices, IndexPeriods, IndicesDics, Dics
from .utils import select_index_data

class GetAllChapters(APIView):
    def get(self, request):
        chapter_objects = list(Chapters.objects.all())
        if not chapter_objects:
            return Response({'status': 'error'}, status=status.HTTP_204_NO_CONTENT)
        data = []
        for chapter in chapter_objects:
            data.append({'name': chapter.name, 'parent_id': None if chapter.parent is None else chapter.parent.id })
        return Response({'status': 'success', 'chapters': data}, status=status.HTTP_200_OK)
    
    
class GetAllIndices(APIView):
    def get(self, request):
        index_objects = list(Indices.objects.all())
        if not index_objects:
            return Response({'status': 'error'}, status=status.HTTP_204_NO_CONTENT)
        data = []
        for index in index_objects:
            data.append({'name': index.name, 'measure': index.measure, 'chapter_id': index.chapter})
        return Response({'status': 'success', 'indices': data})


class GetPeriodsDicsById(APIView):
    def get(self, request, index_id):
        #print('ID - {}'.format(index_id))
        period_dics_objects = list(IndicesDics.objects.filter(index=index_id).select_related('dics', 'period'))
        if not period_dics_objects:
            return Response({'status': 'error'}, status=status.HTTP_204_NO_CONTENT)
        data = []
        for period_dics in period_dics_objects:
            data.append({'periods': period_dics.period, 'dics': period_dics.dics})
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
    

class GetIndexData(APIView):
    def get(self, request, index_id, dates=None):
        # {'terms': [ids],
        # 'termNames': [names],              
        # 'periods': [{'name', 'date', 'value'}, ],
        # }
        # terms -> d_{dic}__id
        # termNames -> d_{dic}__names
        # periods__value -> i_index__value
        # periods__date -> i_index__date_taldau
        # periods__name -> i_index__date_period_id__name

        # Get arguments from URL
        period_id = request.GET.getlist('period')[0]
        dics_id = request.GET.getlist('dics')[0].split(',')
        dates = request.GET.getlist('dates')[0].split(',')
        data = []
        table_name = f"i_{index_id}_p_{period_id}_d_{'_'.join(map(str, dics_id))}"
        dics_table_name = []
        for dic in dics_id:
            dics_table_name.append(f"d_{dic}")

        # Testing purposes
        # print('period - {}\ndics - {}\ndates = {}'.format(period_id, dics_id, dates))
        # print(dics_table_name)
        # print(table_name)
        # print(len(dics_table_name))
        # a = select_chapters()

        index_data, dics_data = select_index_data(table_name, dics_table_name, dates)
        if not index_data or not dics_data:
            return Response({'status': 'error'}, status=status.HTTP_204_NO_CONTENT)
        
        for index in index_data:
            data.append({'terms': dics_data, 'periods': index_data})
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)