#!/usr/bin/perl -w
# $Id$
# 共通するテストを行う。

use strict;
use Test;

BEGIN { plan test => 1 }

my $cgi = "./browse.cgi";
my @test_args = ("id=0001");

chdir "./member";
$ENV{'REMOTE_USER'} = "masao";

foreach my $arg (@test_args) {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
