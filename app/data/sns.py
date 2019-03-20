import boto3
import json


class Sns():
    def __init__(self, topicName):
        sns = boto3.resource('sns')
        self.topic = sns.Topic(topicName)

    def publishFromDictiorary(self, messageDict):
        messageJson = json.dumps(messageDict)
        self.topic.publish(
            Message=messageJson
        )
