import boto3
import os


class Ses():
    def __init__(self):
        SES_REGION = os.environ['SES_REGION']
        self.MAILFROM = os.environ['MAIL_ADRESS_FROM_SODA']
        self.client = boto3.client('ses', region_name=SES_REGION)

    def sendTextmail(self, to, subject, body):
        self.client.send_email(
            Source=self.MAILFROM,
            Destination={
                'ToAddresses': [
                    to
                ]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
