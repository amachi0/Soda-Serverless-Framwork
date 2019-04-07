import json
from app.data.source.profile_table import ProfileTable
from app.data.ses import Ses
from app.util.return_dict import Successed, Failured


def cancel_sns(event, context):
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        eventId = message['eventId']
        title = message['title']
        listFavorite = message['listFavorite']

        profileTable = ProfileTable(event)
        profiles = profileTable.batchGetFromListIdentityId(listFavorite)

        for identityId in listFavorite:
            # それぞれのいいねをしていたユーザーのfavoriteEventから中止されたイベントを削除
            profileTable.deleteListItemInProfileTable(
                identityId, "favoriteEvent", [eventId])

        for profile in profiles:
            if not profile.isAcceptMail:
                continue

            ses = Ses()
            ses.sendTextmail(profile.email, 'イベント中止のお知らせ',
                             '立命館大学生のみなさま、こんにちは！\n\n'
                             'いつもSodaをご利用いただきありがとうございます。\n\n'
                             '〜イベント中止のお知らせ〜\nイベント 「' + title + '」が中止されました\n\n'
                             'その他のイベント情報はこちらまで https://sodaevent.com'
                             )

        res = {"result": 1}
        return Successed(res)

    except Exception:
        import traceback
        return Failured(traceback.format_exc())
