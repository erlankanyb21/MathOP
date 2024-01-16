from rest_framework import serializers

class MathRequestSerializer(serializers.Serializer):
    operation = serializers.CharField()
    expression = serializers.CharField()
    x_value = serializers.CharField(required=False)
    limit_value = serializers.CharField(required=False)
    upper_limit = serializers.CharField(required=False)
    lower_limit = serializers.CharField(required=False)