#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;
use POSIX;

my $q = new CGI;
my $user = $q->remote_user();

my $BASEDIR = ".";
$BASEDIR = ".." if defined $user;

unshift @INC, $BASEDIR;
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

my $comment = CGI::escapeHTML($q->param('comment')) || "";
$comment = nl2br(strip($comment));
my $id = $q->param('id');
$id = util::untaint($id, '\d+', undef);

main();
sub main {
    if (defined $id) {
	if (length($comment)) {
	    my $date = POSIX::strftime "%Y-%m-%d %H:%M", localtime();
	    # lock("bbs/$id");
	    my $fh = util::fopen(">> $BASEDIR/bbs/$id");
	    print $fh "$user\t$date\t$comment\n";
	    $fh->close;
	    # unlock("bbs/$id");
	}
#  	my $tmpl = HTML::Template->new('filename' => "$BASEDIR/template/bbs.tmpl");
#  	$tmpl->param('TITLE' => "データベースに関するコメント",
#  		     'HOME_TITLE' => $conf::HOME_TITLE,
#  		     'HOME_URL' => $conf::HOME_URL,
#  		     'FROM' => $conf::FROM,
#  		     'BASEDIR' => $BASEDIR,
#  		     'BBS-LIST' => util::bbs_list($id, $BASEDIR),
#  		     'USER' => $user,
#  		     'ID' => $id,
#  		     );
#  	print $q->header("text/html; charset=utf-8");
#  	print $tmpl->output;
	print $q->redirect("./browse.cgi?id=$id");
    }
}

sub strip($) {
    my ($str) = @_;
    $str =~ s/^\s+//g;
    $str =~ s/\s+$//g;
    return $str;
}

sub nl2br($) {
    my ($str) = @_;
    $str =~ s/\r\n/<br>/g;
    $str =~ s/\n/<br>/g;
    $str =~ s/\r/<br>/g;
    return $str;
}
