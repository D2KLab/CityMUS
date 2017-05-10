import sys
print tuple(open(sys.argv[1]).readlines())
print len(list(tuple(open(sys.argv[1]).readlines())))