import urllib.request;
import re;
import os;

class Spider:

  # 初始化
  def __init__(self):
    self.url = "http://mm.taobao.com/json/request_top_list.htm";
    self.tool = Tool();

  # 获取页面
  def getPage(self, index):
    url = self.url + "?page=" + str(index);
    response = urllib.request.urlopen(url);
    return response.read();

  # 获取内容
  def getContent(self, index):
    page = self.getPage(index);
    pattern = re.compile('<div class="list-item".*?<a class="lady-name.*?>(.*?)</a>.*?<div class="pic w610".*?<a href="(.*?)"',re.S);
    items = re.findall(pattern, page.decode('gbk'));
    content = [];
    for item in items:
      content.append({"name":item[0],"url":item[1]});
    return content;  

  # 获取详情

  # 获取简介
  def getBrief(self, page):
    pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S);
    result = re.search(pattern, page.decode("gbk"));
    return self.tool.replace(result.group(1));

  # 获取图片
  def getImages(self, html):
    pattern = re.compile('<div class="mm-p-img-area".*?>(.*?)<!--',re.S);
    content = re.search(pattern, html.decode('gbk'));
    #print(html);
    print(content);
    pattern = re.compile('<img.*?src="(.*?)"', re.S);
    images = re.findall(pattern, content.group(1));
    return images;

  # 保存图片
  def saveImages(self, images, name):
    number = 1;
    #print("发现{0}共有{1}张图片".format(name,len(images)));
    for image in images:
      splitPath = image.split(".")
      tail = splitPath.pop();
      if len(tail) > 3:
        tail = "jpg";
      file = name + "/" + str(number) + "." + tail;   
      self.saveImage(url, file);
      number += 1;

  # 保存头像
  def saveIcon(self, icon, name):
    splitPath = icon.split(".")
    tail = splitPath.pop();
    file = name + "/icon." + tail;   
    self.saveImage(url, name);


  # 保存简介
  def saveBrief(self, content, name):
    file = name + "/" + name + ".txt";
    f = open(file, "w+");
    f.write(content.encode("UTF8"));
    f.close();

  # 保存图片
  def saveImage(self, url, name):
    u = urllib.request.urlopen(url);
    data = u.read();
    f = open(name, "wb");
    f.write(data);
    f.close();

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
    content = self.getContent(index);
    for item in content:
      print(item["url"]);
      page = self.getPage(item["url"]);
      #brief = self.getBrief(page);
      #print(page);
      images = self.getImages(page);
      self.mkdir(item["name"]);
      #self.saveBrief(brief, item[2]);
      #self.saveIcon(item[1], item[2]);
      self.saveImages(images, item["name"]);

  # 保存多张页面
  def savePages(self, start, end):
    for i in range(start, end + 1):
      self.savePage(i);

class Tool:
  removeImg = re.compile("<img.*?>| {1,7}| ");
  removeAddr = re.compile("<a.*?>|</a>");
  replaceLine = re.compile("<tr>|<div>|</div>|</p>");
  replaceTD = re.compile("<td>");
  replaceBR = re.compile("<br><br>|<br>");
  removeExtraTag = re.compile("<.*?>");
  removeNoneLine = re.compile("\n+");
  def replace(self, x):
    x = re.sub(self.removeImg, "", x);
    x = re.sub(self.removeAddr, "", x);
    x = re.sub(self.removeLine, "", x);
    x = re.sub(self.removeTD, "", x);
    x = re.sub(self.removeBR, "", x);
    x = re.sub(self.removeExtraTag, "", x);
    x = re.sub(self.removeNoneLine, "", x);
    return x.strip();

spider = Spider();
spider.savePages(2, 10);
