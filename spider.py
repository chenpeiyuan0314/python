import urllib.request;
import re;
import os;

class Spider:

  # 初始化
  def __init__(self):
    # 列表页地址
    self.url = "http://mm.taobao.com/json/request_top_list.htm";
    # 相册页地址
    self.url2 = "https://mm.taobao.com/album/json/get_album_photo_list.htm";
    # 获取失败列表
    self.failList = [];

  # 获取数据
  def getData(self, url):
    response = urllib.request.urlopen(url);
    return response.read().decode("GBK");

  # 获取美女列表
  def getBeautyList(self, index):
    html = self.getData(self.url + "?page=" + str(index));
    pattern = re.compile('<div class="list-item".*?<a class="lady-name.*?>(.*?)</a>.*?<div class="pic w610".*?<a href=".*?-(.*?)-(.*?)\.htm.*?"',re.S);
    items = re.findall(pattern, html);
    list = [];
    for item in items:
      url = self.url2 + "?user_id=" + item[1] +"&album_id=" + item[2];
      list.append({"name":item[0],"url":url});
    return list;  

  # 获取图片列表 
  """
  def getImageList(self, html):
    pattern = re.compile('"picUrl".*?"(.*?)"', re.S);
    items = re.findall(pattern, html);
    list = [];
    for item in items:
      # 获取清晰大图地址
      item = re.sub(re.compile('_290x10000\.jpg$'),"",item)
      list.append("https:" + item);
    return list;
  """
  def getImageList(self, url):
    # 获取总页数
    html = self.getData(url);
    pattern = re.compile('"totalPage".*?"(.*?)"', re.S);
    total = re.search(pattern, html);
    total = int(total.group(1));
    
    list = [];
    index = 1;
    pattern = re.compile('"picUrl".*?"(.*?)"', re.S);
    while index <= total:
      html = self.getData(url + "&page=" + str(index));
      items = re.findall(pattern, html);
      for item in items:
        # 获取清晰大图地址
        item = re.sub(re.compile('_290x10000\.jpg$'),"",item)
        list.append("https:" + item);
      index += 1;  
    return list;

  # 保存多张图片
  def saveImages(self, images, name):
    number = 1;
    for image in images:
      splitPath = image.split(".")
      tail = splitPath.pop();
      if len(tail) > 3:
        tail = "jpg";
      file = name + "/" + str(number) + "." + tail;   
      self.saveImage(image, file);
      number += 1;

  # 保存单张图片
  def saveImage(self, url, name):
    #print(url);
    try:
      u = urllib.request.urlopen(url);
      data = u.read();
      f = open(name, "wb");
      f.write(data);
      f.close();
    except:
      print("save image except: " + url);
      self.failList.append([url, name]);

  # 创建目录
  def mkdir(self, path):
    path = path.strip();
    exists = os.path.exists(path);
    if exists:
      return False;
    else:
      os.makedirs(path);
      return True;

  # 保存单张页面
  def savePage(self, index):
    list = self.getBeautyList(index);
    for item in list:
      #html = self.getData(item["url"]);
      images = self.getImageList(item["url"]);
      self.mkdir(item["name"]);
      self.saveImages(images, item["name"]);

    # 继续下载失败图片
    list = self.failList;
    while len(list) > 0:
      item = list.pop();
      self.saveImage(item[0], item[1]);

  # 保存多张页面
  def savePages(self, start, end):
    for i in range(start, end + 1):
      self.savePage(i);

spider = Spider();
spider.savePage(1);
