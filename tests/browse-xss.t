#!/usr/local/bin/perl -w
# -*-CPerl-*-
# $Id$
# XSS 対策用のテスト

use strict;
use Test;

BEGIN { plan test => 5 }

my $cgi = "./browse.cgi";
my $arg = '<>&"';

foreach my $cgi_arg ("id", "sort", "scan", "search", "page") {
    ok(`perl -wT $cgi '$cgi_arg=$arg'` =~ /\Q$arg/ ? 1 : 0, 0, "$cgi: XSS: $cgi_arg=$arg");
}
