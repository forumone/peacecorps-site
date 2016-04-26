from rest_framework import serializers
from rest_framework.reverse import reverse
from peacecorps.models import Project, Campaign
from django.db import models
from django.utils.translation import ugettext as _
from pprint import pprint


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('name','primary_url',)

class ProjectSerializer(serializers.ModelSerializer):
    project_page_url = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    campaigns = CampaignSerializer(many=True)
    description = serializers.SerializerMethodField()
    fully_funded = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description.html

    def get_country(self, obj):
        return obj.country.name

    def get_fully_funded(self, obj):
        return obj.account.funded()

    def get_project_page_url(self, obj):
        return obj.primary_url()

    class Meta:
        model = Project
        fields = ('title','tagline','slug','description','country','campaigns', 'volunteername', 'volunteerhomestate','abstract', 'fully_funded', 'project_page_url')