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
		 'id' =>  "データベースID",
		 'source_id' =>  "派生元ID",
		 'created_date' =>  "作成日",
		 'update_date' =>  "更新日",
		 'userid' =>  "ユーザID",
		 'dbname' =>  "データベース名",
		 'system' =>  "システム名",
		 'condition' =>  "利用条件(料金、時間含む)",
		 'format' =>  "データ提供形態",
		 'contributor' =>  "コントリビュータ",
		 'description' =>  "特徴",
		 'subject' =>  "主題（分野、キーワード）",
		 'type' =>  "対象とするデータ種別",
		 'lang' =>  "言語",
		 'period' =>  "収録期間",
		 'total' =>  "収録件数",
		 'interval' =>  "更新周期",
		 'interval_num' =>  "更新件数",
		 'region' =>  "対象地域",
		 'category' =>  "カテゴリ",
		 'access' =>  "アクセス先（URLなど）",
		 'group', =>  "グループ名",
		);

# フォーム部品の表示順序、CVSファイルへの登録順も兼ねる
@PARAMETERS = qw(
	       dbname

	       description
	       subject

	       userid
               access
	       system
	       contributor
	       format
	       condition
	       type
	       lang
	       period
	       total
	       interval
	       interval_num
	       region

	       id
               source_id
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
		'id' =>  "hidden",
		'source_id' =>  "hidden",
		'userid' =>  "hidden",
		'system' =>  'textfield:60',
		'system_yomi' =>  'textfield:60',
		'contributor' =>  'textfield:60',
		'service_type' =>  'textfield:60',
		'format' =>  'textfield:60',
		'terminal_type' =>  'textfield:60',
		'condition' =>  'textfield:60',
		'dbname' =>  'textfield:60',
		'dbname_yomi' =>  'textfield:60',
		'description' =>  'textarea:5:60',
		'subject' =>  'textfield:60',
		'type' =>  'textfield:60',
		'publication' =>  'textfield:60',
		'survey' =>  'textfield:60',
		'lang' =>  'textfield:60',
		'period' =>  'textfield:60',
		'total' =>  'textfield:60',
		'interval' =>  'textfield:60',
		'interval_num' =>  'textfield:60',
		'region' =>  'textfield:60',
		'access' =>  'textfield:60',
	       );

# repeatable な入力項目
%PARAM_REPEATABLES = (
		      "contributor" => 1,
		      "format" => 1,
		      "terminal_type" => 1,
		      "subject" => 1,
		      "type" => 1,
		      "lang" => 1,
		     );

### 設定おわり
1;
