all: test

# ��ñ�ʥƥ��Ȥ�Ԥ�
test: $(SCRIPTS)
	perl -e 'use Test::Harness qw(&runtests $$verbose); $$verbose=1; runtests @ARGV;' tests/*.t
