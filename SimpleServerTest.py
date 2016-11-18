#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from os.path import isfile, join

import xmlrpc.client

if __name__ == '__main__':
    s = xmlrpc.client.ServerProxy('http://localhost:8000')
    s.is_even(14)
