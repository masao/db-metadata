#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use Text::ParseWords;

use lib ".";
require 'util.pl';
require 'conf.pl';	# �������Ƥ��ɤ߹���

$| = 1;

# 1�ڡ�����ɽ��������
my $MAX = 10;

# �ơ��֥����Τ��طʿ�
my $BGCOLOR = '#ddddd0';

# �ơ��֥�إå����طʿ�
my $BGCOLOR_HEAD = '#00A020';

# URI �餷��ʸ����˼�ưŪ�˥�󥯤�ĥ�롩
my $USE_AUTOLINK = 1;

# CGI�ѥ�᡼��
my $q = new CGI;
my $SCRIPT_NAME = $q->script_name();
my $page = CGI::escapeHTML($q->param('page')) || 0;
my $search = CGI::escapeHTML($q->param('search')) || "";
my $sort = CGI::escapeHTML($q->param('sort')) || 0;

# ��Ͽ����Ƥ���ǡ������ݻ���������
my @entries = ();

main();
sub main {
    print $q->header("text/html; charset=EUC-JP");
    print $conf::HTML_HEADER;
    print <<EOF;
<hr>
<form method="GET" action="$SCRIPT_NAME">
<p>����ɽ��:
<input type="text" name="search" value="$search">
<input type="hidden" name="sort" value="$sort">
<input type="submit" value="�ʤ���߸���">
</p>
</form>
EOF

    my $fh = util::fopen($conf::FILENAME);
    my @lines = <$fh>;
    chomp(@lines);

    if (length($search)) {	# ����
	@lines = grep(/$search/oi, @lines);
	print "<p>Perl �� /$search/oi ���Ƥ��ޤ���grep -i �Ȥۤ�Ʊ���Ǥ���</p>";
 	print "<p><font color=\"red\">�������: ", $#lines + 1, "��</font></p>\n";
    }

    for my $line (@lines) {
	my @tmp = quotewords(',', 0, $line);
	push(@entries, \@tmp) if @tmp > 0;
    }

    my $sortby = 0;
    $sortby = $1 if $sort =~ /(\d+)/;
    @entries = sort { fncmp($a->[$sortby], $b->[$sortby]) } @entries;
    @entries = reverse @entries if $sort =~ /r$/;

    print <<EOF;
<hr>
<table width="100%" border="1" bgcolor="$BGCOLOR">
<tr bgcolor="$BGCOLOR_HEAD">
EOF
    for (my $i = 0; $i < @conf::PARAMETERS; $i++) {
	print <<EOF;
<th>
<a href="$SCRIPT_NAME?sort=$i;search=$search">$conf::PARAM_LABELS{$conf::PARAMETERS[$i]}</a>
<a href="$SCRIPT_NAME?sort=${i}r;search=$search">(*)</a>
</th>
EOF
    }
    print "</tr>\n";

    for (my $i = $page * $MAX; $i < @entries && $i < ($page+1) * $MAX; $i++) {
	print "<tr valign=\"top\">\n";
	for my $cont (@{$entries[$i]}) {
	    $cont =~ s/^\s+//g;
	    $cont =~ s/\s+$//g;
	    if ($USE_AUTOLINK) {
		$cont =~ s#((https?|ftp)://[;\/?:@&=+\$,A-Za-z0-9\-_.!~*'()]+)#<a href="$1">$1</a>#gi;
	    }
	    print "<td>$cont</td>\n";
	}
	print "</tr>\n";
    }
    print "</table>\n";
    print_pages();
    print $conf::HTML_FOOTER;
}


# �������θ����������
sub fncmp() {
    my ($x, $y) = @_;
    $x =~ s/(\d+)/sprintf("%05d", $1)/ge;
    $y =~ s/(\d+)/sprintf("%05d", $1)/ge;
    return $x cmp $y;
}

sub print_pages() {
    my $base_url = "$SCRIPT_NAME?sort=$sort;search=$search";
    print "<p>�ڡ���:\n";
    for (my $i = 0; $i*$MAX < @entries; $i++) {
	if ($i == $page) {
	    print "[", $i+1, "]\n";
	} else {
	    print "<a href=\"$base_url;page=$i\">[", $i+1, "]</a>\n";
	}
    }
    print "</p>\n";
}


# For avoiding "used only once: possible typo at ..." warnings.
util::muda($conf::FILENAME,
	   $conf::HTML_HEADER,
	   $conf::HTML_FOOTER,
	   $conf::PARAM_LABELS,
	  );
