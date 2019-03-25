import decimal
import json
from app.data.event import Event
from app.data.profile import Profile


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Event):
            event = {
                'eventName': o.eventName,
                'eventId': o.eventId,
                'start': o.start,
                'location': o.location,
                'countOfLike': o.countOfLike
            }
            return event

        if isinstance(o, Profile):
            profile = {
                'email': o.email
            }
            return profile

        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
