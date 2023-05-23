from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.preprocess import preprocess_email, extract_urls, detect_fakenews, extract_url_features, detect_cyberbuilling
from .utils.predict import classify_email_body, classifyUrl
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from .models import Email, Url
from .serializers import EmailSerializer

import requests
from requests.structures import CaseInsensitiveDict
import pprint


class EmailView(ListCreateAPIView):
    serializer_class = EmailSerializer
    queryset = Email.objects.all()

    def create(self, request, *args, **kwargs):
        print("Running create function")

        emails = request.data.get('emails', [])

        for email in emails:
            body = email.get('body')
            emailId = email.get('emailId')
            from_email = email.get('from_email')
            subject = email.get('subject')
            date = email.get('date')

            header = "\n".join([str(x) for x in email.get('header')])
            header = "\n".join([str(x) for x in email.get('header')])

            processed_email_body = preprocess_email(body)

            phishing_score_header = 0.01

            phishing_score_body = classify_email_body(processed_email_body)
            builing_score_body = detect_cyberbuilling(body)
            fakenews_score_body = detect_fakenews(body)

            print('header_pish ' + str(phishing_score_header))
            print('body_pish ' + str(phishing_score_body))
            print('bulling ' + str(builing_score_body))
            print('fake ' + str(fakenews_score_body))
            print('******************************************')

            email_instance = Email.objects.create(
                emailId=emailId,
                from_email=from_email,
                subject=subject,
                date=date,
                body=body,
                header=header,
                phishing_score_body=str(phishing_score_body),
                phishing_score_header=str(phishing_score_header),
                builing_score_body=str(builing_score_body),
                fakenews_score_body=str(fakenews_score_body),


            )
            email_instance.save()
            urls = extract_urls(body)
            for url in urls:
                url_features = extract_url_features(url)
                phishing_score = classifyUrl(url_features)
                url_instance = Url.objects.create(
                    url_text=url,
                    phishing_score=phishing_score,
                    email=email_instance
                )
                url_instance.save()

        return self.list(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def classfiyEmail(request):
    if request.method == 'POST':
        email_body = request.data['body']
        processed_email_body = preprocess_email(email_body)
        result = classify_email_body(processed_email_body)

    return Response({
        "bodyScore": result

    })


@api_view(['GET', 'POST'])
def fetchEmails(request):
    if request.method == 'POST':
        token = request.data['access_token']

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}"
        r = requests.get(
            'https://gmail.googleapis.com/gmail/v1/users/me/messages/?maxResults=5', headers=headers)

    return Response({
        "result": r.text
    })
