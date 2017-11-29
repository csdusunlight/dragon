from wafuli.models import TransList, UserEvent
from rest_framework import serializers

# Create your views here.
class TransListSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='user.mobile', read_only=True)
    user_balance = serializers.CharField(source='balance', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = TransList
        fields = '__all__'
        
