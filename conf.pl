#!/usr/local/bin/perl -w
# $Id$

package conf;

### ���̤�����

# ô���ԤΥ᡼�륢�ɥ쥹
$FROM = 'yuka@ulis.ac.jp';

# �ڡ����Υ����ȥ�
$TITLE = '�ǡ����١����������Ͽ/����';

# �ۡ���ڡ����� URL
$HOME_URL = 'http://nile.ulis.ac.jp/~masao/dbxml/';

# �ۡ���ڡ����Υ����ȥ�
$HOME_TITLE = '�ǡ����١�������ͭ�ץ�������';

# �ե��������Ƭ�˽���ջ����HTML��
$NOTE = <<EOF;
<p>
�ǡ����١����˴ؤ���������Ͽ���������ޤ���
</p>
EOF

# ɬ�ܹ��ܤ򼨤��ޡ�����HTML��
$REQ_MARK = '<small><font color="red">��</font></small>';

# ��Ͽ���Ƥ�Ͽ����ǥ��쥯�ȥ�̾: `chmod a+w $DATADIR`���Ƥ������ȡ�
$DATADIR = 'data';

# �᡼�����ε�ǽ��Ȥ���: �Ȥ����� 1 �ˤ��롣
$USE_MAIL = 0;

  # �᡼�����Τ������ Subject: ����ASCII�ϻȤ��ʤ���
  $SUBJECT = '[DB Metadata]';

### HTML �� <form> ���ʤ����

# �ե��������ʤΥ�٥��̾����
%PARAM_LABELS = ('name' => '̾��',
		 'post' => '��°',
		 'e-mail' => 'E-mail',# �᡼�����Τ������ɬ�סʰ����
		 'note' => '�̿�',
		 'date' => '��Ͽ����',
		 'contact' => 'Ϣ����',
		 'contact_name' => '̾��',
		 'address' => '����',
		 'phone' => '����',
		 'keyword' => '�������',
		);

# �ե��������ʤ�ɽ�������CVS�ե�����ؤ���Ͽ����ͤ�
@PARAMETERS = ('name', 'post', 'e-mail', 'note', 'date', 'contact', 'keyword');

# �ե��������ʤΤ�����ɬ�����Ϲ��ܤΤ��
# �ʡ�e-mail�פξ��ϥ᡼�륢�ɥ쥹�δʰץ����å���Ԥ���
%REQ_PARAMETERS = ('name' => 1, 'e-mail' => 1);

# �ե��������ʤμ���: textfield, textarea, radio, etc.
#
# ��external�פ���Ͽ����ưŪ�˾�����ɲä����������Ѥ��롣
#
%PARAM_TYPES = ('name' => 'textfield:40',
		'post' => 'textfield:40',
		'e-mail' => 'textfield:40',
		'note' => 'textarea:4:50',
		'date' => 'external:scalar localtime()',
		'contact' => 'nest:contact_name:address:phone',
		'contact_name' => 'textfield:40',
		'address' => 'textfield:40',
		'phone' => 'textfield:40',
		'keyword' => 'textfield:50',
	       );

# repeatable �����Ϲ���
%PARAM_REPEATABLES = ('keyword' => 1);

### HTML��ɽ��

# ������λ���Υ�å�������HTML�ˤ���Ƭ��ʬ
$REPORT_HEADER = <<EOF;
<p>
�ǡ����١����������Ͽ���꤬�Ȥ��������ޤ�����
</p>
<p>
��Ͽ���Ƥϰʲ����̤�Ǥ���<br>
����礻�� <a href="mailto:$FROM">$FROM</a> �ޤǤ��ꤤ�������ޤ���
</p>
<p>
[��Ͽ����]
</p>
<table border="2">
EOF

# ������λ���Υ�å������κǸ����ʬ
$REPORT_FOOTER = <<EOF;
</table>
EOF

# HTML����Ƭ��ʬ
$HTML_HEADER = <<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<title>$TITLE</title>
</head>
<body>
<h1>$TITLE</h1>
EOF

# HTML�κǸ����ʬ
$HTML_FOOTER = <<EOF;
<hr>
<address>
<a href="$HOME_URL">$HOME_TITLE</a> / <a href="mailto:$FROM">$FROM</a>
</address>
</body>
</html>
EOF

### ���ꤪ���
1;
