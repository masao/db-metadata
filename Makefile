all: test

# ��ñ�ʥƥ��Ȥ�Ԥ�
test: $(SCRIPTS)
	perl -e 'use Test::Harness qw(&runtests $$verbose); $$verbose=0; runtests @ARGV;' tests/*.t
