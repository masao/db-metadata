# $Id$
package conf;

### 全般の設定

# 担当者のメールアドレス
$FROM = 'yuka@ulis.ac.jp';

# ページのタイトル
$TITLE = 'データベース情報の登録/更新';

# ホームページの URL
$HOME_URL = 'http://nile.ulis.ac.jp/~yuka/db-template/top.html';

# ホームページのタイトル
$HOME_TITLE = 'データベース情報共有プロジェクト';

# 必須項目を示すマーク（HTML）
$REQ_MARK = '<small><font color="red">※</font></small>';

# 登録内容を記録するディレクトリ名: `chmod a+w $DATADIR`しておくこと。
$DATADIR = 'data';

# メール通知機能を使う？: 使う場合は 1 にする。
$USE_MAIL = 0;

  # メール通知する場合の Subject: （非ASCIIは使えない）
  $SUBJECT = '[DB Metadata]';

# データを登録する XML のルート要素名
$ROOT_ELEMENT = 'データベース';

### HTML の <form> 部品の定義

# フォーム部品のラベル（名前）
%PARAM_LABELS = (
		 'dbid' =>  "データベースID",
		 'userid' =>  "ユーザID",
		 'system' =>  "システム名",
		 'system_yomi' =>  "システム名・ヨミ",
		 'distributor' =>  "ディストリビュータ",
		 'distributor_yomi' =>  "ディストリビュータ・ヨミ",
		 'distributor_country' =>  "ディストリビュータ国名",
		 'service_type' =>  "サービス種別",
		 'distribute_type' =>  "配布種別",
		 'terminal_type' =>  "端末種別",
		 'fee' =>  "利用料金",
		 'time' =>  "利用時間",
		 'condition' =>  "利用条件",
		 'comment' =>  "コメント",
		 'dbname' =>  "データベース名",
		 'dbname_yomi' =>  "データベース名・ヨミ",
		 'producer' =>  "プロデューサ",
		 'producer_yomi' =>  "プロデューサ・ヨミ",
		 'producer_country' =>  "プロデューサ国名",
		 'description' =>  "特徴",
		 'field' =>  "分野",
		 'subfield' =>  "分野",
		 'keyword' =>  "キーワード",
		 'type' =>  "対象とするデータ種別",
		 'publication' =>  "冊子体名",
		 'survey' =>  "調査名",
		 'lang' =>  "言語",
		 'period' =>  "収録期間",
		 'total' =>  "収録件数",
		 'interval' =>  "更新周期",
		 'interval_num' =>  "更新件数",
		 'region' =>  "対象地域"
		);

# フォーム部品の表示順序、CVSファイルへの登録順も兼ねる
@PARAMETERS = qw(
	       dbname
	       dbname_yomi

	       description
	       field
	       keyword

	       dbid
	       userid
	       system
	       system_yomi
	       distributor
	       distributor_yomi
	       distributor_country
	       service_type
	       distribute_type
	       terminal_type
	       fee
	       time
	       condition
	       comment
	       producer
	       producer_yomi
	       producer_country
	       type
	       publication
	       survey
	       lang
	       period
	       total
	       interval
	       interval_num
	       region

	       id
	      );

# フォーム部品のうち、必須入力項目のもの
# （「e-mail」の場合はメールアドレスの簡易チェックも行う）
%REQ_PARAMETERS = (
		   'dbname' => 1,
#		   'description' => 1,
		  );

# フォーム部品の種類: textfield, textarea, radio, etc.
#
# 「external」は登録時に動的に情報を追加したい場合に用いる。
#
%PARAM_TYPES = (
		'id' =>  "hidden:0",
		'dbid' =>  "hidden",
		'userid' =>  "hidden",
		'system' =>  'textfield:60',
		'system_yomi' =>  'textfield:60',
		'distributor' =>  'textfield:60',
		'distributor_yomi' =>  'textfield:60',
		'distributor_country' =>  'textfield:60',
		'service_type' =>  'textfield:60',
		'distribute_type' =>  'textfield:60',
		'terminal_type' =>  'textfield:60',
		'fee' =>  'textfield:60',
		'time' =>  'textfield:60',
		'condition' =>  'textfield:60',
		'comment' =>  'textfield:60',
		'dbname' =>  'textfield:60',
		'dbname_yomi' =>  'textfield:60',
		'producer' =>  'textfield:60',
		'producer_yomi' =>  'textfield:60',
		'producer_country' =>  'textfield:60',
		'description' =>  'textarea:5:60',
		'field' =>  'textfield:60',
		'keyword' =>  'textfield:60',
		'type' =>  'textfield:60',
		'publication' =>  'textfield:60',
		'survey' =>  'textfield:60',
		'lang' =>  'textfield:60',
		'period' =>  'textfield:60',
		'total' =>  'textfield:60',
		'interval' =>  'textfield:60',
		'interval_num' =>  'textfield:60',
		'region' =>  'textfield:60',
	       );

# repeatable な入力項目
%PARAM_REPEATABLES = (
		      "service_type" => 1,
		      "distribute_type" => 1,
		      "terminal_type" => 1,
		      "keyword" => 1,
		      "type" => 1,
		      "lang" => 1,
		     );

### 設定おわり
1;
