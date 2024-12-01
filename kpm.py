#!/usr/bin/python3
import os
import kpm.cli

if __name__=='__main__':
    if len(os.sys.argv) < 2:
        print('Usage: kpm.py <command>')
        os.sys.exit(1)
    kpm.cli.handle_command(os.sys.argv[1:])