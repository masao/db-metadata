#!/usr/local/bin/perl -w
# $Id$

use strict;
use DB_File;

require 'util.pl';
require 'conf.pl';      # 設定内容を読み込む

main();
sub main {
    if (defined($ARGV[0])) {
	my @files = util::pickup_files();
	
	mkhash($ARGV[0], @files);
    } else {
	print "Usage: $0 target\n";
	exit 1;
    }
}

sub mkhash($$) {
    my ($name, @files) = @_;
    my %hash = ();
    tie(%hash, 'DB_File', "$name.db", O_CREAT|O_RDWR) ||
        die "tie fail: $name.db: $!";

    foreach my $file (@files) {
	my $content = util::readfile("$conf::DATADIR/$file");
        my ($id) = util::get_tagvalues($content, "id");
        my @values = util::get_tagvalues($content, $name);
	# print "$id => @values\n";
	foreach my $key (@values) {
	    next unless defined $key;
	    if (defined $hash{$key}) {
		if(check_id($hash{$key},$id) eq "false"){
		    $hash{$key} .= ",$id";
		}
	    } else {
		$hash{$key} = $id;
	    }
	}
    }
#    foreach my $key (sort keys %hash) {
#	print "$key => $hash{$key}\n";
#    }
}

sub check_id($$) {
    my ($list, $id) = @_;

    my $flag = "false";
    foreach my $kouho (split(',',$list)){
	if($kouho eq $id){
	    $flag = "true";
	}
    }
    return $flag;
}
