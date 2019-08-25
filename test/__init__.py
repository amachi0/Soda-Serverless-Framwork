import os

# profileテーブル
os.environ['PROFILE_TABLE'] = 'profile'
os.environ['PROFILE_CHECK_SODA_ID_INDEX'] = 'check-sodaId-index'
os.environ['PROFILE_CHECK_Email_INDEX'] = 'check-email-index'
os.environ['PROFILE_SODA_ID_INDEX'] = 'sodaId-index'

# eventテーブル
os.environ['EVENT_TABLE'] = 'event'
os.environ['EVENT_STATUS_START_INDEX'] = 'status-start-index'
os.environ['EVENT_STATUS_COUNTOFLIKE_INDEX'] = 'status-countOfLike-index'
os.environ['EVENT_STATUS_UPDATETIME_INDEX'] = 'indexKey-updateTime-index'

# sequenceテーブル
os.environ['SEQUENCE_TABLE'] = 'sequence'

# s3
os.environ['S3_JSON_BUCKET'] = 'soda-json'
os.environ['S3_IMAGE_BUCKET'] = 'soda-image'
os.environ['ARN_S3'] = "https://s3-ap-northeast-1.amazonaws.com"

os.environ['FAQS_JSON'] = 'faqs.json'
os.environ['TERMS_JSON'] = 'terms.json'
os.environ['UNIVERSITY_JSON'] = 'university.json'

print('__init__')
