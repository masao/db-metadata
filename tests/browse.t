#!/usr/bin/perl -w
# $Id$
# browse.cgi に対するテストを行う。

use strict;
use Test;

BEGIN { plan test => 10 }

my $cgi = "./browse.cgi";
my @test_args =
    ("id=0001",
     "id=unknown",
     "search=新聞",
     "scan=subject",
     "id=0356", # データ項目が少なめ
     "id=8139", # 一番データが多い
     "id=9354", # 最後のid
     "scan=subject search=PC",
     "scan=subject search=エネルギー page=1",
     "scan=system",
     );

foreach my $arg (@test_args) {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
