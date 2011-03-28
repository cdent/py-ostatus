#!/usr/bin/env python

import sys

from ostatus.profile import profile

def run():
    args = sys.argv
    for arg in args[1:]:
        data = profile(arg)
        print data


if __name__ == '__main__':
    run()
