from rest_framework import serializers

class MailRequestSerializer(serializers.Serializer):
    phone_number=serializers.IntegerField()
    product_number=serializers.IntegerField()
    product_name=serializers.CharField()
    text = serializers.CharField()
    file = serializers.FileField()