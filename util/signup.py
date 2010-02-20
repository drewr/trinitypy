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
