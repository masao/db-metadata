all: test

# 簡単なテストを行う
test: $(SCRIPTS)
	perl -e 'use Test::Harness qw(&runtests $$verbose); $$verbose=1; runtests @ARGV;' tests/*.t
