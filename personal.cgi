#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

# 登録/更新用 CGI

use strict;
use vars qw($MSG);
use POSIX;
use DB_File;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;

$| = 1;

my $q = CGI->new();

my $userid = $q->param("userid");
my $user = $q->remote_user();
if (!defined($userid)) {
    $userid = $user;
}

my $BASEDIR = ".";
$BASEDIR = ".." if defined $user;

unshift @INC, $BASEDIR;
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む
require 'message.pl';

main();
sub main {
    print $q->header("text/html; charset=utf-8");
    my $tmpl = HTML::Template->new('filename' => util::template_fname("$BASEDIR/template/personal.tmpl"));
    $tmpl->param('TITLE' => sprintf($$MSG{$conf::LANG}{'personal_page'}, $userid),
		 'HOME_TITLE' => $conf::HOME_TITLE,
		 'HOME_URL' => $conf::HOME_URL,
		 'FROM' => $conf::FROM,
		 'USER' => $user,
		 'BASEDIR' => $BASEDIR,
		 'MYGROUP' => my_grouplist(),
		 'MYDB' => my_dblist(),
		 'IS_MYPAGE' => $user eq $userid,
		);
    print $tmpl->output;
}

sub my_grouplist() {
    my $retstr = '';
    my %info = util::get_groupinfo("$BASEDIR/group.txt");
    my @mygroups = ();
    foreach my $id (keys %info) {
	if ($info{$id}->{'user'} eq $userid) {
	    push @mygroups, $id;
	}
    }
    foreach my $id (@mygroups) {
	$retstr .= "<div><span style=\"font-weight:bold;font-size:larger;\">";
	$retstr .= "<a href=\"./browse.cgi?scan=group;search=$id\">". $info{$id}->{'name'} ."</a></span>\n";
	if ($user eq $userid) {
	    $retstr .= "<span class=\"button\"><a href=\"./addgroup.cgi?cmd=editgroup;groupid=$id\">$$MSG{$conf::LANG}{'personal_modify'}</a></span></div>";
	}
	if (length($info{$id}->{'description'})) {
	    $retstr .= "<div style=\"font-size:smaller;margin-left:2em\">". $info{$id}->{'description'} ."</div>\n";
	}
	$retstr .= "<ul>\n";
	foreach my $subid (@{$info{$id}->{'list'}}) {
	    $retstr .= "<li><a href=\"./browse.cgi?id=$subid\">" . util::get_dbname($subid) . "</a>\n";
	    # $retstr .= "<span class=\"button\"><a href=\"./addgroup.cgi?cmd=delgroup;id=$subid\">[削除]</a></span>\n";
	}
	$retstr .= "</ul>\n";
    }
    return $retstr;
}

sub my_dblist() {
    my @files = util::pickup_files();
    my @mydb = ();
    foreach my $file (@files) {
	my $cont = util::readfile("$BASEDIR/$conf::DATADIR/$file");
	if ((util::get_tagvalues($cont, "userid"))[0] eq $userid) {
	    $file =~ s/\.xml$//g;
	    push @mydb, $file;
	}
    }
    my $retstr = '<ul>';
    foreach my $id (@mydb) {
	$retstr .= "<li><a href=\"./browse.cgi?id=$id\">" . util::get_dbname($id) . "</a>\n";
    }
    return $retstr."</ul>";
}
