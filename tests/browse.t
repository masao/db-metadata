#!/usr/bin/perl -w
# $Id$
# ���̤���ƥ��Ȥ�Ԥ���

use strict;
use Test;

BEGIN { plan test => 7 }

my $cgi = "./browse.cgi";
my @test_args =
    ("id=0001", "id=unknown", "search=��ʹ", "scan=keyword",
     "id=8139", # ���֥ǡ�����¿��
     "id=9354", # �Ǹ��id
     "scan=keyword search=PC",
     );

foreach my $arg (@test_args) {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
