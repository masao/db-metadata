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

use lib "..";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

my $q = CGI->new();
my $cmd = $q->param('cmd');

my $user = $q->remote_user();

main();
sub main {
    print $q->header("text/html; charset=utf-8");
    my $tmpl = HTML::Template->new('filename' => '../template/personal.tmpl');
    $tmpl->param('TITLE' => "$user さんのページ",
		 'HOME_TITLE' => $conf::HOME_TITLE,
		 'HOME_URL' => $conf::HOME_URL,
		 'FROM' => $conf::FROM,
#		 'SCRIPT_NAME' => $q->script_name(),
		 'USER' => $user,
		 'BASEDIR' => '..',
		 'MYGROUP' => my_grouplist(),
		 'MYDB' => my_dblist(),
		);
    print $tmpl->output;
}

sub my_grouplist() {
    my $retstr = '';
    my %info = util::get_groupinfo("../group.txt");
    my @mygroups = ();
    foreach my $id (keys %info) {
	if ($info{$id}->{'user'} eq $user) {
	    push @mygroups, $id;
	}
    }
    foreach my $id (@mygroups) {
	$retstr .= "<h3>". $info{$id}->{'name'} ."</h3>\n";
	$retstr .= "<ul>\n";
	foreach my $subid (@{$info{$id}->{'list'}}) {
	    $retstr .= "<li><a href=\"./browse.cgi?id=$subid\">$subid</a>\n";
	}
	$retstr .= "</ul>\n";
    }
    return $retstr;
}

sub my_dblist() {
    my $retstr = '<ul>';
    my %hash = ();
    tie(%hash, 'DB_File', "../userid.db", O_RDONLY) ||
	die "tie fail: userid.db: $!";
    my @mydb = split(/,/, $hash{$user});
    foreach my $id (@mydb) {
	$retstr .= "<li><a href=\"./browse.cgi?id=$id\">$id</a>\n";
    }
    return $retstr."</ul>";
}
