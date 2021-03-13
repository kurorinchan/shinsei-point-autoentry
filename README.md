新生銀行のポイントプログラムにエントリーするツール。
このツールは自動で規約などに同意することを選択するので、同意できない場合は使用しないでください。
同意する必要のある規約は[ポイントプログラムのページ](https://www.shinseibank.com/service/point/)
などの新生銀行のウェブページから確認してください。

このツールを使用することによって被る結果のいかなる責任も負いません。

# 必要なもの
- Python 3
- Pipenv
- Chrome
- [Chrome driver](https://chromedriver.chromium.org/downloads)

# 使用方法
```
pipenv run python ./autoentry.py --driver=/path/to/driver \
  --account_num <account number> \
  --date_of_birth 'YYYY-MM-DD' \
  --tpoint_num <T point number> \
  --email <email>            
```

コマンドラインフラグの説明
* account_num
  * 新生銀行の10桁の口座番号
* date_of_birth
  * 生年月日 YYYY-MM-DD
* tpoint_num
  * 16桁のTポイントカード番号
* email
  * ポイントエントリーなどのメールを受け取ったメールアドレス
