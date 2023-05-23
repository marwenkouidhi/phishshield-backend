from django.db import models
from django.contrib.auth.models import User


class Email(models.Model):
    class Meta:
        ordering = ('-emailId',)

    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="emails")
    header = models.TextField()
    body = models.TextField()
    phishing_score_header = models.CharField(default="0", max_length=256,)
    phishing_score_body = models.CharField(default="0", max_length=256,)
    builing_score_body = models.CharField(default="0", max_length=256,)
    fakenews_score_body = models.FloatField(default="0", max_length=256,)
    emailId = models.CharField(max_length=256, default="0")
    from_email = models.CharField(max_length=256, default="0", null=True)
    subject = models.CharField(max_length=256, default='0', null=True)
    date = models.CharField(max_length=256, default='0', null=True)

    def __str__(self) -> str:
        return self.body

    @property
    def overall_score(self):
        url_scores = self.urls.values_list("phishing_score", flat=True)
        urls_count = len(url_scores)
        urls_mean_score = sum(url_scores) / urls_count if urls_count > 0 else 0

        overall_score = (
            float(self.phishing_score_header) * 0.3
            + float(self.phishing_score_body) * 0.3
            + float(urls_mean_score) * 0.2

            + float(self.builing_score_body) * 0.1
            + float(self.fakenews_score_body) * 0.1
        )

        return round(overall_score * 100)


class Url(models.Model):
    url_text = models.TextField()
    phishing_score = models.FloatField()
    email = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="urls")
