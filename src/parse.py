# -*- coding: utf-8 -*-


import re
#處理掉unicode 和 str 在ascii上的問題
import sys
import os
import json

reload(sys)
sys.setdefaultencoding('utf8')


class FIND_CORP:
  '''
  00000000,{
  "公司狀況":"核准設立",
  "公司名稱":"復華廣告有限公司",
  "資本總額(元)":"500,000",
  "代表人姓名":"李水發",
  "公司所在地":"臺中市中區錦上里平等街５６巷１號",
  "登記機關":"經濟部中部辦公室",
  "核准設立日期":{"year":1976,"month":5,"day":24},
  "最後核准變更日期":{"year":1996,"month":12,"day":12},
  "所營事業資料":[],
  "董監事名單":[],
  "經理人名單":[],
  "停業日期(起)":null,
  "停業日期(迄)":null}
  '''
  wanted_list = ["代表人在台灣地區業務活動範圍", "代表人姓名", "停業日期(起)", "停業日期(迄)", "公司名稱", "公司所在地", "公司狀況", "分公司名稱", "分公司所在地", "分公司狀況", "名稱", "商業名稱", "在中華民國境內營運資金", "地址", "實收資本額(元)", "廢止日期", "最後核准變更日期", "最近異動日期", "核准設立日期", "統一編號", "經理人名單", "股權狀況", "董監事名單", "負責人姓名"]
  data = None

  def __init__(self):
    self.data=[]
    for i in range(10):
      self.parse(i)


  def parse(self,number):
    f = open(os.path.dirname(__file__)+'/../data/%d0000000.json'%number)
    i = 0
    for line in f.readlines():
      #print line[9:]

      j = json.loads(line[9:])
      j[u'統一編號'] = line[0:8]
      if u'核准設立日期' in j and j[u'核准設立日期'] is not None:
        d = j[u'核准設立日期']
        j[u'核准設立日期'] = '-'.join(map(str,[d['year'],d['month'],d['day']]))

      if u'停業日期(起)' in j and j[u'停業日期(起)'] is not None:
        d = j[u'停業日期(起)']
        j[u'停業日期(起)'] = '-'.join(map(str,[d['year'],d['month'],d['day']]))

      if u'停業日期(迄)' in j and j[u'停業日期(迄)'] is not None:
        d = j[u'停業日期(迄)']
        j[u'停業日期(迄)'] = '-'.join(map(str,[d['year'],d['month'],d['day']]))



      if u'廢止日期' in j and j[u'廢止日期'] is not None:
        d = j[u'廢止日期']
        j[u'廢止日期'] = '-'.join(map(str,[d['year'],d['month'],d['day']]))

      if u'最後核准變更日期' in j and j[u'最後核准變更日期'] is not None:
        d = j[u'最後核准變更日期']
        j[u'最後核准變更日期'] = '-'.join(map(str,[d['year'],d['month'],d['day']]))

      if u'資本總額(元)' in j:
        j[u'資本總額(元)'] = j[u'資本總額(元)'].replace(",","")

      if u'實收資本額(元)' in j:
        j[u'實收資本額(元)'] = j[u'實收資本額(元)'].replace(",","")


      if u'公司所在地' in j:
        j[u'公司所在地'] = j[u'公司所在地'].replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")

        if j[u'公司所在地'].find('內湖區')>=0:
          self.data.append(j)

 #     if u'所營事業資料' in j and len(j[u'所營事業資料'])>0:
 #       print "\n\n\n\nn\n\nn\n"int
 #       print j[u'所營事業資料']
 #       for k in j[u'所營事業資料']:
 #         for kk in k:
 #           print kk
 #         print type(k)
#      i = i +1
#      if i>=4:
#        break



#      if u'董監事名單' in j and len(j[u'董監事名單'])>0:
#        print "\n\n\n\nn\n\nn\n"
#        print j[u'董監事名單']
#        for k in j[u'董監事名單'][0]:
#          print k
#          print j[u'董監事名單'][0][k]
#          print type(k)
#      for ii in j:
#        if j[ii] is list:
#          for jj in j[ii][0]:
#            print "\t%s | %s" %(jj,j[ii][jj])
#        else:
#          print "%s | %s" %(ii,j[ii])



    f.close()

  def write(self):
    f = open(os.path.dirname(__file__)+'/../data/result.csv',"w+")
    f.write(",".join(self.wanted_list)+"\n")
    for d in self.data:
      c = []
      for col in map(unicode,self.wanted_list):
        if col in d:
          c.append(str(d[col]).encode('utf-8'))
        else:
          c.append("")
      #print c
      f.write(",".join(c)+"\n")
    f.close()

  def appendTD(self,a):
    return "<td>"+a+"</td>"

  def write_html(self):
    f = open(os.path.dirname(__file__)+'/../data/test.html',"w+")
    f.write("<!doctype html><html><head><meta charset='UTF-8'><title>TEST</title><style>td{border:1px solid rgb(44,157,142) } table{width:150%}</style><body><table><tr>\n")
    f.write("".join(map(self.appendTD,self.wanted_list))+"\n")
    f.write('</tr>\n')

    for d in self.data:
      f.write("<tr>")
      for col in map(unicode,self.wanted_list):
        f.write('<td>')
        if col in d and d[col] is not None:


          if type(d[col]) is list:
            f.write('<ul>')
            for e in d[col]:
              for ff in e:
                #print type(e)
                #print type(ff)
                if type(e[ff]) is dict:
                  f.write('<li>%s-%s-%s-%s</li>'%(ff,e[ff][u'year'],e[ff][u'month'],e[ff][u'day']))
                else:
                  f.write('<li>%s-%s</li>'%(ff,e[ff]))
            f.write('</ul>')
          elif type(d[col]) is dict:
            f.write('<ul>')
            for e in d[col]:
              f.write('<li>2'+e+"-"+d[col][e]+'</li>')
            f.write('</ul>')

          else:
            f.write(d[col])
        f.write('</td>')


      f.write("</tr>")

    f.write("</table></body></html>")

    #for d in self.data:
    #  c = []
    #  for col in map(unicode,self.wanted_list):
    #    if col in d:
    #      c.append(str(d[col]).encode('utf-8'))
    #    else:
    #      c.append("")
    #  print c
    #  f.write(",".join(c)+"\n")
    f.close()





if __name__ =="__main__":
  d = FIND_CORP()
  d.write_html()


