#!/usr/local/bin/perl -w
# $Id$

package conf;

### ���̤�����

# ô���ԤΥ᡼�륢�ɥ쥹
$FROM = 'hasegawa@ulis.ac.jp';

# �ڡ����Υ����ȥ�
$TITLE = '���Ͳ��ϥ���ݥ�����᡼�������Ͽ';

# �ۡ���ڡ����� URL
$HOME_URL = 'http://phase.hpcc.jp/nas/';

# �ۡ���ڡ����Υ����ȥ�
$HOME_TITLE = '��31����Ͳ��ϥ���ݥ����� (NAS2002)';

# �ե��������Ƭ�˽���ջ����HTML��
$NOTE = <<EOF;
<p>
������᡼��ˤ�����򤴴�˾�����Ϥ���Ͽ����������
���ÿ������ߤǤϤ���ޤ���
</p>
EOF

# ��Ͽ���Ƥ�Ͽ����CSV�ե�����: `chmod a+w $FILENAME`���Ƥ������ȡ�
$FILENAME = "annai.csv";

# �᡼�����ε�ǽ��Ȥ���: �Ȥ����� 1 �ˤ��롣
$USE_MAIL = 0;

  # �᡼�����Τ������ Subject: ����ASCII�ϻȤ��ʤ���
  my $SUBJECT = 'NAS2002 registration';

### HTML �� <form> ���ʤ����

# �ե��������ʤΥ�٥��̾����
%PARAM_LABELS = ('name' => '̾��',
		 'post' => '��°',
		 'e-mail' => 'E-mail',# �᡼�����Τ������ɬ�סʰ����
		 'note' => '�̿�',
		 'date' => '��Ͽ����');

# �ե��������ʤ�ɽ�������CVS�ե�����ؤ���Ͽ����ͤ�
@PARAMETERS = ('name', 'post', 'e-mail', 'note', 'date');

# �ե��������ʤΤ�����ɬ�����Ϲ��ܤΤ��
# �ʡ�e-mail�פξ��ϥ᡼�륢�ɥ쥹�δʰץ����å���Ԥ���
%REQ_PARAMETERS = ('name' => 1, 'e-mail' => 1);

# �ե��������ʤμ���: textfield, textarea, radio, etc.
#
# ��external�פ���Ͽ����ưŪ�˾�����ɲä����������Ѥ��롣
#
%PARAM_TYPES = ('name' => 'textfield:40', 'post' => 'textfield:40',
		'e-mail' => 'textfield:40', 'note' => 'textarea:4:50',
		'date' => 'external:scalar localtime()');

### HTML��ɽ��

# ������λ���Υ�å�������HTML�ˤ���Ƭ��ʬ
$REPORT_HEADER = <<EOF;
<p>
���Ͳ��ϥ���ݥ�����ؤΰ��⿽�����ߤ��꤬�Ȥ��������ޤ���
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
<center>
<h1>$TITLE</h1>
EOF

# HTML�κǸ����ʬ
$HTML_FOOTER = <<EOF;
</center>
<hr>
<a href="$HOME_URL">$HOME_TITLE</a>
</body>
</html>
EOF

### ���ꤪ���
1;
