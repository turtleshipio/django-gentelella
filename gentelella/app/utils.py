from datetime import datetime, timedelta
import pytz


def getYesterdayDateAt11pm():

    today = datetime.utcnow()
    today = today.replace(tzinfo=pytz.timezone("Asia/Seoul"))
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=0, second=0)
    return yesterday
