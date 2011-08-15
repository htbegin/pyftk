#!/usr/bin/env python
# -*- coding: utf8 -*-

class FtkApp(object):
    def __init__(self, name, get_icon, run):
        self.name = name
        self._get_icon = get_icon
        self._run = run

    def get_icon(self):
        return self._get_icon()

    def run(self):
        return self._run()
