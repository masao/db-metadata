#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use DirHandle;

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

# ����ɽ���κݤ�ɽ�����٤�����:  @conf::PARAMETERS ������Ѥ��ͤ������
my @DISPLAY_ELEMENTS = ('name', 'date');

# CGI�ѥ�᡼��
my $q = new CGI;
my $SCRIPT_NAME = $q->script_name();
my $page = CGI::escapeHTML($q->param('page')) || 0;
my $search = CGI::escapeHTML($q->param('search')) || "";
my $sort = CGI::escapeHTML($q->param('sort')) || 0;

# ��Ͽ����Ƥ���ǡ������ݻ���������
my @files = ();

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
<hr>
EOF

    opendir(DIR, $conf::DATADIR) || die "opendir: $conf::DATADIR: $!";
    @files = grep { /^\d+\.xml$/o } readdir(DIR);
    closedir(DIR) || die "closedir: $!";

    if (length($search)) {	# ����
	my @result = ();
	for my $file (@files) {
	    my $cont = util::readfile($file);
	    push @result, $file if $cont =~ /$search/oi;
	}
	@files = @result;
	print "<p>Perl �� /$search/oi ���Ƥ��ޤ���grep -i �Ȥۤ�Ʊ���Ǥ���</p>";
 	print "<p><font color=\"red\">�������: ", $#files + 1, "��</font></p>\n";
    }

    print <<EOF;
<table width="100%" border="1" bgcolor="$BGCOLOR">
<tr bgcolor="$BGCOLOR_HEAD">
EOF
    for (my $i = 0; $i < @DISPLAY_ELEMENTS; $i++) {
	print <<EOF;
<th>
<a href="$SCRIPT_NAME?sort=$i;search=$search">$conf::PARAM_LABELS{$DISPLAY_ELEMENTS[$i]}</a>
<a href="$SCRIPT_NAME?sort=${i}r;search=$search">(*)</a>
</th>
EOF
    }
    print "</tr>\n";

    for (my $i = $page * $MAX; $i < @files && $i < ($page+1) * $MAX; $i++) {
	print "<tr valign=\"top\">\n";
	# print "<td><a href=\"$script_name/$i\">". $i+1 ."</a></td>\n";
	my $cont = util::readfile("$conf::DATADIR/$files[$i]");
	for my $elem (@DISPLAY_ELEMENTS) {
	    my @tmp = ();
	    my $tag = $conf::PARAM_LABELS{$elem};
	    $cont =~ s#<$tag[^>]*>([^<]*)</$tag>#push(@tmp, $1)#e;
	    $cont = join(",", @tmp);
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
    for (my $i = 0; $i*$MAX < @files; $i++) {
	if ($i == $page) {
	    print "[", $i+1, "]\n";
	} else {
	    print "<a href=\"$base_url;page=$i\">[", $i+1, "]</a>\n";
	}
    }
    print "</p>\n";
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda($conf::HTML_HEADER,
	   $conf::HTML_FOOTER,
	   $conf::PARAM_LABELS,
	  );
