from rest_framework import serializers
from rest_framework.reverse import reverse
from peacecorps.models import Project, Campaign
from django.db import models
from django.utils.translation import ugettext as _
from pprint import pprint


class CountryCampaignSerializer(serializers.ModelSerializer):

    country = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_country(self, obj):
        return obj.country.name

    def get_description(self, obj):
        return obj.description.html

    class Meta:
        model = Campaign
        fields = ('name','campaigntype','country','description','abstract','primary_url',)

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('name','primary_url',)

class ProjectSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Project
        fields = ('title','tagline','slug','description','country','campaigns', 'volunteername', 'volunteerhomestate','abstract', 'fully_funded', 'primary_url')