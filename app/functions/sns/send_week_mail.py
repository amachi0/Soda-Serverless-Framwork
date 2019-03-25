import json
from botocore.exceptions import ClientError
from app.data.ses import Ses
from app.util.return_dict import Failured


def send_week_mail(event, context):
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        events = message['events']
        data = {
            'events': events
        }

        profiles = message['profiles']
        listEmail = []
        for profile in profiles:
            listEmail.append(profile['email'])

        ses = Ses()
        for email in listEmail:
            ses.sendMailTemplate(email, json.dumps(data))

    except ClientError:
        import traceback
        return Failured(traceback.format_exc())
