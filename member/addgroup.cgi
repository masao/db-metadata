#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

# 登録/更新用 CGI

use strict;
use POSIX;
use CGI qw/:standard/;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;

$| = 1;

use lib "..";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

my $q = CGI->new();
my $user = $q->remote_user();

my $cmd = $q->param('cmd');
my $name = $q->param('name');
my $dbid = $q->param('dbid');
my $groupid = $q->param('groupid');

main();
sub main {
    if (defined($cmd)) {
	if ($cmd eq "newgroup" && defined($name) && length($name)) {
	    my %group = util::get_groupinfo("../group.txt");
	    my $newid = (sort { $b <=> $a } keys %group)[0] + 1;
	    $group{$newid} = {'name' => $q->param('name'),
			      'user' => $user,
			      'list' => [] };
	    util::write_groupinfo("../group.txt", %group);
	    print $q->redirect("./browse.cgi");
	} elsif ($cmd eq "addgroup") {
	    if (defined($dbid) && length($dbid) &&
		defined($groupid) && length($groupid)) {
		my %group = util::get_groupinfo("../group.txt");
		my @list = @{$group{$groupid}->{'list'}};
		push @list, $dbid;
		$group{$groupid}->{'list'} = [ @list ];
		util::write_groupinfo("../group.txt", %group);
	    }
	    print STDERR "DBID: $dbid";
	    print $q->redirect("./browse.cgi?id=$dbid");
	} else {
	    print $q->header("text/html; charset=utf-8");
	    my $tmpl = HTML::Template->new('filename' => '../template/addgroup.tmpl');
	    $tmpl->param('TITLE' => "新規グループの追加",
			 'HOME_TITLE' => $conf::HOME_TITLE,
			 'HOME_URL' => $conf::HOME_URL,
			 'FROM' => $conf::FROM,
			 'SCRIPT_NAME' => script_name(),
			 'USER' => remote_user(),
			 'BASEDIR' => '..',
			);
	    print $tmpl->output;
	    exit;
	}
    } else {
	print $q->redirect("./browse.cgi");
    }
}
