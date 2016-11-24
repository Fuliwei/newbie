#!/usr/bin/python
#coding:utf-8

import urllib
import re,sys,os
def GetImgs():
    if not os.path.exists('douban_imgs'):
        os.mkdir('douban_imgs')
        os.chdir('douban_imgs')
    for num in 1000,1100,1200,1300:
        url = "http://www.douban.com/group/topic/73873048/?start=%d" % num
        content = urllib.urlopen(url).read()
        #print content
        #sys.exit()
        imgs = re.findall(r'<img class="pil" src="(.*)" alt="(.*)"',content)      # ͼƬ�������£�ÿ��ƥ���.*�����ߣ�.*\.jpg���������������ʽ����
 #<img class="pil" src="http://img3.douban.com/icon/u56865303-6.jpg " alt="����������">
        #print imgs ����Ľ��Ϊ[('http://img3.douban.com/icon/u56865303-6.jpg ', '�������'),����]
        #sys.exit()
        for img in imgs:
            img_url = img[0]  # ����ĵ�һ��Ԫ�ؼ�Ϊ��һ�� ��.*�������ݣ�
            img_name = img[1] # ����ĵڶ���Ԫ�ؼ�Ϊ�ڶ��� ��.*����
            urllib.urlretrieve(img_url,"%s.jpg" % img_name)
if __name__ == "__main__":
    GetImgs()
