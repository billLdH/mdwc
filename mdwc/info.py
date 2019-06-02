#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

class Info:
    def __init__(self,info_file):
        self.lines= open("mdwc/INFO.txt").readlines()
        info= dict()
        for line in lines:
            info[str(line.split("=")[0])] = str(line.split("=")[1])

        self.__name__=info["__name__"]
        self.__version__ =info["__version__"]
        self.__license__ = info["__license__"]
        self.__author__ = info["__author__"]
        self.__maintainer__ = info["__maintainer__"]
        self.__university__ = info["__university__"]
        self.__maintainer_email__ = info["__maintainer_email__"]
        self.__description__=info["__description__"]
        self.__date__ = info["__date__"]
        self.__url__= info["__url__"]
        self.__download_url__=info["__download_url__"]
