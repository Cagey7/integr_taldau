from rest_framework import serializers
from .models import *


class IndexIdSerializer(serializers.Serializer):
    index_id = serializers.IntegerField()

    def validate(self, data):
        try:
            Index.objects.get(id=data.get("index_id"))
        except:
            raise serializers.ValidationError("Не существует показатель с указанным айди")
        return data


class IndexInfoSerializer(serializers.Serializer):
    index_id = serializers.IntegerField()
    period_id = serializers.IntegerField()
    dic_ids = serializers.ListField(child=serializers.IntegerField())
    
    def validate(self, data):
        try:
            dics_id = Dic.objects.get(dic_ids=data.get("dic_ids")).id
            IndexDics.objects.get(index_id=data.get("index_id"), period_id=data.get("period_id"), dics_id=dics_id)
        except:
            raise serializers.ValidationError("Неправильные данные либо справочники показателя не загружены")
        return data
