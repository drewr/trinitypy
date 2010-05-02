from django.conf import settings
from campaign_monitor_api import CampaignMonitorApi

class SignupException(StandardError):
    pass

def sign_up_to_list(email, name=""):
    cm = CampaignMonitorApi(settings.CAMPAIGN_MONITOR_KEY, None)
    try:
        return cm.subscriber_add(settings.CAMPAIGN_MONITOR_LIST, email, name)
    except CampaignMonitorApi.CampaignMonitorApiException, e:
        raise SignupException(e.message)


def list_lists():
    cm = CampaignMonitorApi(settings.CAMPAIGN_MONITOR_KEY, settings.CAMPAIGN_MONITOR_CLIENT)
    try:
        return cm.client_get_lists()
    except CampaignMonitorApi.CampaignMonitorApiException, e:
        print e.message
        return []



def list_subscribers(list_id):
    cm = CampaignMonitorApi(settings.CAMPAIGN_MONITOR_KEY, settings.CAMPAIGN_MONITOR_CLIENT)
    try:
        return cm.subscribers_get_active(list_id)
    except CampaignMonitorApi.CampaignMonitorApiException, e:
        assert False, e
