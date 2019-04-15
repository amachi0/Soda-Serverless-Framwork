<div align="center">
<img src="https://s3-ap-northeast-1.amazonaws.com/soda-image/soda.png">
</div>

[![CircleCI](https://circleci.com/gh/amachi0/Soda-Serverless-Framwork/tree/master.svg?style=svg&circle-token=ce8c77ea8b879a3bb0510605f97654ead78d50be)](https://circleci.com/gh/amachi0/Soda-Serverless-Framwork/tree/master)

# Sodaとは
Sodaは、立命館大学生のためのイベントを共有する無料サービスです。あなたの所属するサークルやクラブ活動だけでなく、あなた自身で開催するイベントも、簡単に全ての人に共有することができます。
このレポジトリはSodaのバックエンドのAPI部分を実現しています。

# アプリケーションの機能一覧
- イベントの新規作成・変更・削除・詳細
- タイムラインの表示 ( 開催順・人気順・投稿順 )
- ユーザー情報の登録・取得・変更
- いいね機能
- いいねをしたイベントのタイムラインの表示
- 作成したイベントのタイムラインの表示 
- 毎週月曜日に人気のイベントトップ20をメールで配信
- 毎日Twitterに今日開催されるイベントを投稿

# 使用している技術
![aws_picture](https://user-images.githubusercontent.com/40754926/55887220-16870b00-5be8-11e9-8e7d-a11c959d1bf2.png)

インフラにはAWSを使用し、低コストで運用できるサーバーレスアーキテクチャを実現した。  
__API Gateway__ でブラウザからのリクエストを受け取りメソッドに対応する __Lambda function__ を起動させる。  
そして、その中で適切な処理を行った後にレスポンスをブラウザに返す。データベースにはサーバーレスアーキテクチャと相性のいい __DynamoDB__ を使用している。  
イベントのサムネイル画像やユーザーのプロフィール画像などを保存するストレージには __S3__ を使用している。  
また、Lambdaから __SNS__ を起動し、それがトリガーになるLambda関数も実装した。その具体的な例として、メールを送信するなどの比較的実行時間がかかる処理を非同期的に行うことができるようになった。  
また、__CloudWatch Events__ を用いて、毎朝８時にLambdaを起動させてお知らせメールを送る、Twitterにtweetするなどの機能を実現している。