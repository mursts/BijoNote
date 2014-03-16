BijoNote
========

美女暦の画像をEvernoteにクリップします。

--------------------

 このスクリプトでは以下のモジュールを使用しています。
 
 + requests
 + PIL
 + evernote

 ```
 pip install PIL
 pip install requests
 pip install evernote
 や
 easy_install PIL
 easy_install requests
 easy_install evernote
 ```
 等でインストールします。

### config.py
user_store_uriに環境に合わせたuriを設定します。
[サンドボックスでのテスト](http://dev.evernote.com/intl/jp/documentation/cloud/chapters/Testing.php)

+ サンドボックス https://sandbox.evernote.com/
+ プロダクション https://www.evernote.com/


auth_tokenにはデベロップトークンを設定します。
[デベロッパトークンの使用](https://www.evernote.com/api/DeveloperToken.action)

