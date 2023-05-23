from rest_framework.serializers import ModelSerializer
from .models import Email, Url


class UrlSerializer(ModelSerializer):
    class Meta:
        model = Url
        fields = ('__all__')


class EmailSerializer(ModelSerializer):
    urls = UrlSerializer(many=True)

    class Meta:
        model = Email
        fields = ('id', 'overall_score', 'urls', 'header', 'body',
                  'phishing_score_header', 'phishing_score_body',
                  'builing_score_body', 'fakenews_score_body', 'emailId', 'from_email', 'subject', 'subject', 'date')
