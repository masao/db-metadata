#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

# 登録/更新用 CGI

use strict;
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

main();
sub main {
    print $q->header("text/html; charset=utf-8");
    my $tmpl = HTML::Template->new('filename' => "$BASEDIR/template/personal.tmpl");
    $tmpl->param('TITLE' => "$userid さんのページ",
		 'HOME_TITLE' => $conf::HOME_TITLE,
		 'HOME_URL' => $conf::HOME_URL,
		 'FROM' => $conf::FROM,
		 'SCRIPT_NAME' => "browse.cgi",
		 'USER' => $user,
		 'BASEDIR' => $BASEDIR,
		 'ADDGROUP_FORM' => addgroup_form(),
		 'MYGROUP' => my_grouplist(),
		 'MYDB' => my_dblist(),
		);
    print $tmpl->output;
}
sub addgroup_form () {
    my $retstr = "";
    if ($user eq $userid) {
	$retstr = <<EOF;
<div class="addgroup-form">
<form method="POST" action="./addgroup.cgi">
<input type="hidden" name="cmd" value="newgroup">
新規グループ名: <input type="text"   name="name" value="" size="30"><br>
説明: <input type="text" name="description" value="" size="60">
<input type="submit" name="submit" value=" 登 録 ">
</form>
</div>
EOF
    }
    return $retstr;
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
	$retstr .= "<div><span style=\"font-weight:bold;font-size:larger;\">". $info{$id}->{'name'} ."</span>\n";
	if ($user eq $userid) {
	    $retstr .= "<span class=\"button\"><a href=\"./addgroup.cgi?cmd=editgroup;groupid=$id\">[修正]</a></span></div>";
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
    my $retstr = '<ul>';
    my %hash = ();
    tie(%hash, 'DB_File', "$BASEDIR/userid.db", O_RDONLY) ||
	die "tie fail: userid.db: $!";
    my @mydb = split(/,/, $hash{$userid});
    foreach my $id (@mydb) {
	$retstr .= "<li><a href=\"./browse.cgi?id=$id\">" . util::get_dbname($id) . "</a>\n";
    }
    return $retstr."</ul>";
}
