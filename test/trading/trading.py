# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import _init_paths

from app.trading import trader, decision

codes=['000001']
st=20170126
et=20180126

trader = trader.Trader(decision.SimpleDecision(codes[0]), st=st, et=et, codes=codes)
trader.run()