#!/usr/bin/env python3
# -*- coding: utf8 -*-


class Pixivlove(object):
    def __init__(self, originalUrl1,originalUrl2):
        
        self.originalUrl1 = originalUrl1
        self.originalUrl2 = originalUrl2

    def print_attrs(self):
        print(
            
            'originalUrl1:', self.originalUrl1, ',',
            'originalUrl2:', self.originalUrl2
        )

    def get_info(self):
        return {
            
        }
