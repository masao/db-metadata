#!/usr/bin/perl -w
# $Id$
# 共通するテストを行う。

use strict;
use Test;

BEGIN { plan test => 6 }

my @scripts = ("./genform.cgi");

for my $cgi (@scripts) {
    # syntax ？
    ok(`perl -cwT $cgi 2>&1`, qr/syntax OK/, "$cgi: syntax");

    # 適当な引数で実行して、エラーメッセージを表示しないか？
    for my $arg (0, 1, "foo", "bababa", "x"x500) {
	ok("", `perl -wT $cgi $arg 2>&1 > /dev/null`, "$cgi: $arg");
    }
}
