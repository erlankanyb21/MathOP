from rest_framework import serializers
from .models import Chat

class MathRequestSerializer(serializers.Serializer):
    operation = serializers.CharField()
    expression = serializers.CharField()
    x_value = serializers.CharField(required=False)
    limit_value = serializers.CharField(required=False)
    upper_limit = serializers.CharField(required=False)
    lower_limit = serializers.CharField(required=False)

class ChatSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(max_length=1000)
    bitmap = serializers.ImageField(allow_null=True, required=False, use_url=True)
    is_from_user = serializers.BooleanField(required=True)

    class Meta:
        model = Chat
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.bitmap:
            ret['bitmap'] = self.context['request'].build_absolute_uri(instance.bitmap.url)
        return ret

