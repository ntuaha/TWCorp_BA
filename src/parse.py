# -*- coding: utf-8 -*-


import re
#處理掉unicode 和 str 在ascii上的問題
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf8')


class FIND_CORP:
  def __init__(self):
    f = open('../data/00000000.json')
    i = 0
    for line in f.readlines():
      #print line[9:]
      j = json.loads(line[9:])
      print j[u'公司所在地']
      #print j
      i = i +1
      if i>=10:
        break

    f.close()



if __name__ =="__main__":
  FIND_CORP()


