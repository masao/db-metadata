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
my $dbid = $q->param('dbid');
my $groupid = $q->param('groupid');
my $name = $q->param('name');
my $description = $q->param('description');
$description =~ s/\s+/ /g;

main();
sub main {
    if (defined($cmd)) {
	if ($cmd eq "newgroup" && defined($name) && length($name)) {
	    my %group = util::get_groupinfo("../group.txt");
	    my $newid = (sort { $b <=> $a } keys %group)[0] + 1;
	    $group{$newid} = {'name' => $name,
			      'user' => $user,
			      'description' => $description,
			      'list' => [] };
	    util::write_groupinfo("../group.txt", %group);
	    print $q->redirect("./personal.cgi");
	} elsif ($cmd eq "addgroup") {
	    if (defined($dbid) && length($dbid) &&
		defined($groupid) && length($groupid)) {
		my %group = util::get_groupinfo("../group.txt");
		my @list = @{$group{$groupid}->{'list'}};
		push @list, $dbid;
		$group{$groupid}->{'list'} = [ @list ];
		util::write_groupinfo("../group.txt", %group);
	    }
	    print $q->redirect("./browse.cgi?id=$dbid");
	} elsif ($cmd eq "delgroup") {
	    die("グループIDが指定されていません。")
		unless defined($groupid) && length($groupid);
	    my %group = util::get_groupinfo("../group.txt");
	    die("別のユーザが登録したグループです。")
		unless $group{$groupid}->{'user'} eq $user;
	    die("まだデータベースが登録されています。")
		if scalar @{$group{$groupid}->{'list'}};
	    delete $group{$groupid};
	    util::write_groupinfo("../group.txt", %group);
	    print $q->redirect("./personal.cgi");
	} elsif ($cmd eq "editgroup") {
	    if ($q->param('submit')) {
		my %group = util::get_groupinfo("../group.txt");
		my %info = %{$group{$groupid}};
		$info{'name'} = $name;
		$info{'description'} = $description;
		$group{$groupid} = \%info;
		util::write_groupinfo("../group.txt", %group);
		print $q->redirect("./addgroup.cgi?cmd=editgroup;groupid=$groupid");
	    } else {
		print $q->header("text/html; charset=utf-8");
		my $tmpl = HTML::Template->new('filename' => '../template/editgroup.tmpl');
		$tmpl->param('TITLE' => "グループの編集",
			     'HOME_TITLE' => $conf::HOME_TITLE,
			     'HOME_URL' => $conf::HOME_URL,
			     'FROM' => $conf::FROM,
			     'SCRIPT_NAME' => script_name(),
			     'USER' => remote_user(),
			     'BASEDIR' => '..',
			     'GROUPID' => $groupid,
			     'EDITGROUP_FORM' => editgroup_form(),
			    );
		print $tmpl->output;
	    }
	} elsif ($cmd eq "deldb") {
	    my %group = util::get_groupinfo("../group.txt");
	    my %info = %{$group{$groupid}};
	    my @list = grep { $dbid ne $_ } @{$info{'list'}};
	    $info{'list'} = \@list;
	    $group{$groupid} = \%info;
	    util::write_groupinfo("../group.txt", %group);
	    print $q->redirect("./addgroup.cgi?cmd=editgroup;groupid=$groupid");
	} else {
	    die "不明な命令です。";
	}
    } else {
	die "不明な命令です。";
    }
}

sub editgroup_form() {
    my $retstr = "<form action=\"./addgroup.cgi\" method=\"GET\">\n";
    my %group = util::get_groupinfo("../group.txt");
    my $name = $group{$groupid}->{'name'};
    my $description = $group{$groupid}->{'description'};
    $retstr .= <<EOF;
グループ名：<input type="text" name="name" value="$name" size="30"><br>
説明：<input type="text" name="description" value="$description" size="60">
<input type="hidden" name="cmd" value="editgroup">
<input type="hidden" name="groupid" value="$groupid">
<input type="submit" name="submit" value="変更">
</form>
EOF
    $retstr .= "<ul>\n";
    foreach my $subid (@{$group{$groupid}->{'list'}}) {
	$retstr .= <<EOF;
<li><a href="./browse.cgi?id=$subid">$subid</a>
<span class="button" style="margin:1em;"><a href="./addgroup.cgi?cmd=deldb;groupid=$groupid;dbid=$subid">[削除]</a></span>
EOF
    }
    $retstr .= "</ul>\n";
    return $retstr;
}
