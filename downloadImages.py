import re
import urllib.request
import ssl

# 把获取该url所对应的html
def HTML(url):
    # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    # 将要伪装成的浏览器添加到对应的http头部
    request = urllib.request.Request(url,headers=headers)
    '''
        该错误时添加context
        urllib.error.URLError:
        <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
        certificate verify failed (_ssl.c:749)>
    '''
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)    #报ssl错误时添加

    response = urllib.request.urlopen(request,context=context)
    data = response.read()
    # 将获得的html解码为utf-8
    data = data.decode('utf-8')
    return data

#保存图片的方法
#data是HTML(url)方法的返回值
#reg是匹配图片的正则表达式
#path是保存路径，保存的图片名字为0.png,1.png....
def saveImage(data,reg,path):
    abc = re.findall(reg, data)
    i = 0
    for url in abc:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # 报ssl错误时添加
            request = urllib.request.urlopen(url, context=context)
            data = request.read()
            # wb 二进制写，文件存储同样被清空
            f = open(path + '/%d.png' % (i), mode='wb')
            f.write(data)
            print('已保存%d张图片' % (i + 1))
            f.close()
        except Exception as e:
            print('第%d张图片保存失败，错误代码：%s' % (i + 1, e))
        finally:
            pass
        i += 1
        print(url+'\n')

#调用saveImage方法
url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E5%AE%A0%E7%89%A9'

saveImage(HTML(url),r'"objURL":"(http://.+?)",','/Users/mac-mini/Desktop/images')