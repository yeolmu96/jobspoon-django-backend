from rest_framework import serializers

class NaverOauthAccessTokenSerializer(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()
