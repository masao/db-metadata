#!/usr/bin/perl -w
# $Id$
# ���̤���ƥ��Ȥ�Ԥ���

use strict;
use Test;

BEGIN { plan test => 6 }

my @scripts = ("./genform.cgi");

for my $cgi (@scripts) {
    # syntax ��
    ok(`perl -cwT $cgi 2>&1`, qr/syntax OK/, "$cgi: syntax");

    # Ŭ���ʰ����Ǽ¹Ԥ��ơ����顼��å�������ɽ�����ʤ�����
    for my $arg (0, 1, "foo", "bababa", "x"x500) {
	ok("", `perl -wT $cgi $arg 2>&1 > /dev/null`, "$cgi: $arg");
    }
}
