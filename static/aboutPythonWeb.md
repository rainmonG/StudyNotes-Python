> 摘自《Python高效开发实战：Django、Tornado、Flask、Twisted（第3版）》
# 第5章 Python网络框架纵览
目前Python的网络变成框架已经多达几十个，逐个学习它们显然不现实。但这些框架在系统架构和运行环境上有很多相通之处。
- Python网络框架综述：了解什么是网络框架，分析Python最主要的网络框架的特点及适用环境，学习Web开发中经典的MVC架构。
- 网络开发通用工具：Python网络开发标准接口WSGI、网络客户端调试工具等。
- Web服务器：Nginx的安装、配置，以及安全的HTTPS站点的搭建方法。
## 5.1 网络框架综述
### 5.1.1 网络框架及MVC架构
所谓网络框架是指这样一组Python包，它能够使开发者专注于网站应用业务逻辑的开发，而无须处理网络应用底层的协议、线程、进程等。这样能大大提高开发者的工作效率，同时提高网络应用程序的质量。

目前在Python语言的几十个开发框架中，几乎所有的全栈网络框架都强制或引导开发者使用MVC架构开发Web应用。所谓全栈网络框架，是指除了封装网络和线程操作，还提供HTTP栈、数据库读写管理、HTML模板引擎等一系列功能的网络框架。Django、Tornado和Flask是全栈网络框架的标杆；而Twisted更专注于网络底层的高性能封装，不提供HTML模板引擎等界面功能，因此不能称之为全栈框架。

MVC（Model View Controller）模式最早由Trygve Reenskaug在1978年提出，在20世纪80年代是程序语言Smalltalk的一种内部架构。后来MVC被其他语言所借鉴，成了软件工程中的一种软件架构模式。MVC把Web应用系统分为3个基本部分。
- 模型（Model）：用于封装与应用程序的业务逻辑相关的数据及对数据的处理方法，是Web应用程序中用于处理应用程序的数据逻辑的部分，Model只提供功能性的接口，通过这些接口可以获取Model的所有功能。Model不依赖于View和Controller，它们可以在任何时候调用Model访问数据。有些Model还提供了事件通知机制，为在其上注册过的View或Controller提供实时的数据更新。
- 视图（View）：负责数据的显示和呈现，View是对用户的直接输出。MVC中的一个Model通常为多个View提供服务。为了获取Model的实时更新数据，View应该尽早地注册到Model中。
- 控制器（Controller）：负责从用户端收集用户的输入，可以看成提供View的反向功能。当用户的输入导致View发生变化时，这种变化必须是通过Model反映给View的。在MVC架构下，Controller一般不能与View直接通信，这样提高了业务数据的一致性，即以Model作为数据中心。

这3个基本部分互相分离，使得在改进和升级界面及用户交互流程时，不需要重写业务逻辑及数据访问代码。

注意：MVC在除Python外的其他语言中也有广泛应用，如VC++的MFC、Java的Structs及Spring、C#的.NET开发框架。

### 5.1.2 4种Python网络框架：Django、Tornado、Flask、Twisted
Python作为最主要的互联网语言，在其发展的二十多年中出现了数十种网络框架，如Django、Flask、Twisted、Bottle、Web.py等，它们有的历史悠久，有的蓬勃发展，而有的已停止维护，如何对其进行取舍常常使初学者犹豫不决。
1. Django<br/>
Django发布于2003年，是当前Python世界里最负盛名且最成熟的网络框架。最初用来制作在线新闻的Web站点，目前已发展为应用最广泛的Python网络框架。<br/>
Django的各模块之间结合得比较紧密，它功能强大且是一个相对封闭的系统，其健全的在线文档及开发社区，使开发者在遇到问题时总能找到解决方法。
2. Tornado<br/>
Tornado是一个强大的、支持协程、高效并发且可扩展的Web服务器，发布于2009年9月，应用于FriendFeed、Facebook等社交网站。Tornado的强项在于可以利用它的异步协程机制开发高并发的服务器系统。
3. Flask<br/>
Flask是Python Web框架族里比较年轻的一个，发布于2010年。Flask的核心功能简单，通常以扩展组件形式增加其他功能，因此也被称为“微框架”。
4. Twisted<br/>
Twisted是一个有着近20年历史的开源事件驱动框架。Twisted不像前3种框架那样着眼于网络HTTP应用的开发，而是适用于从传输层到自定义应用协议的所有类型的网络程序的开发，并能在不同的操作系统上提供很高的运行效率。

### 5.3 Web服务器
Web服务器是连接用户浏览器与Python服务器端程序的中间节点，在网站建立的过程中起着重要的作用。目前最主流的Web服务器包括Nginx、Apache、lighthttpd、IIS等。Python服务器端程序在Linux平台下使用最广泛的是Nginx。
### 5.3.1 WSGI
WSGI是将Python服务器端程序连接到Web服务器的通用协议。由于WSGI的通用性，出现了独立的WSGI程序，如uWSGI和Apache的mod_wsgi。<br/>
WSGI的全称为Web Server Gateway Interface，也可称作Python Web Server Gateway Interface，为Python语言定义Web服务器和服务器端程序的通用接口规范。因为WGSI在Python中的成功，所以其他语言诸如Perl和Ruby也定义了类似WSGI作用的接口规范。<br/>
WSGI分为两个接口：一个是与Web服务器的接口，另一个是与服务器端程序的接口。WSGI Server与Web服务器的接口包括uWSGI、FastCGI等，服务器端的开发者无须详细了解，更需要关注的是WSGI与服务器端程序的接口。<br/>
定义服务器端程序中的函数，所有来自Web服务器的HTTP请求都会由WSGI服务转换为对这些函数的调用。

注意：虽然WSGI的设计目标是连接标准的Web服务器（Nginx、Apache等）与服务器端程序，但WSGI Server本身也可以作为Web服务器运行。由于性能方面的原因，该服务器一般只做测试使用，不能用于正式运行。

### 5.3.2 Linux+Nginx+uWSGI配置
Nginx是由俄罗斯工程师开发的一个高性能HTTP和反向代理服务器，其第一个公开版本0.1.0于2004年以开源形式发布。自发布后，它以运行稳定、配置简单、资源消耗低而闻名。许多知名网站（百度、新浪、腾讯等）均采用Nginx作为Web服务器。
```shell
sudo apt-get install nginx
```
安装程序把Nginx以服务的形式安装在系统中，相关的程序及默认的文件路径：
- 程序文件：放在/usr/sbin/nginx目录下
- 全局配置文件：/etc/nginx/nginx.conf
- 访问日志文件：/var/log/nginx/access.log
- 错误日志文件：/var/log/nginx/error.log
- 站点配置文件：/etc/nginx/sites-enabled/default

这些配置和Nginx的运行参数可以通过全局配置文件和站点配置文件进行设置。

在每个Nginx服务器中可以运行多个Web站点，每个站点的配置通过站点配置文件设置。每个站点应该以一个单独的配置文件存放在站点目录中。

**安装uWSGI及配置**

uWSGI是WGSI在Linux中的一种实现，这样开发者就无须自己编写WSGI Server了。
```shell
pip install uwsgi
```
安装完成后即可运行uwsgi命令来启动WSGI服务器。uwsgi命令通过启动参数的方式配置可选的运行方式。`--http`指定监听端口，`--wsgi-file`指定服务器端程序名。启动过程中会输出系统的一些环境信息：服务器名、进程数限制、服务器硬件配置、最大文件句柄数等。
- socket：以WSGI的Socket方式运行，并指定连接地址和端口。该Socket接口是uWSGI与其他Web服务器（Nginx、Apache等）进行对接的方式。
- chdir：指定uWSGI启动后的当前目录。
- processes：指定启动服务器端程序的进程数。
- threads：指定每个服务器端程序的线程数，即服务器端的总线程数为processes×threads。
- uid：指定运行uWSGI的Linux用户id。

除了在uWSGI启动命令行中提供配置参数，uWSGI还允许通过一个配置文件`*.ini`设置这些配置参数。启动uWSGI时直接指定配置文件即可。

**集成Nginx与uWSGI**

直接通过在站点配置文件中为location配置uwsgi_pass，即可将Nginx与uWSGI集成，建立一个基于Nginx+Python的正式站点。配置中的IP地址与Port配置必须与uWSGI接口中的参数相同。

技巧：可以为一个uWSGI配置多个Nginx Server和location，这样就轻松实现了以多域名访问同一个Python程序。

### 5.3.3 建立安全的HTTPS网站
普通HTTP站点的协议与数据以明文方式在网络上传输，而HTTPS（Hyper Text Transfer Protocol over Secure Socket Layer）是以安全为目标的HTTP通道，通过SSL达到数据加密及身份认证的目的。目前几乎所有的银行、证券、公共交通的网站均以HTTPS方式搭建。

OpenSSL是一个强大的免费Socket密码库，蕴含了主要的密码算法、常用的密钥和证书封装管理功能及SSL协议。目前大多数网站通过OpenSSL工具包搭建HTTPS站点，步骤：
1. 在服务器中安装OpenSSL工具包
```shell
sudo apt-get install openssl
sudo apt-get install libssl-dev
```
运行成功后，OpenSSL命令和配置文件将被安装到Linux系统目录中。默认在/usr/bin/openssl和/usr/lib/ssl/。
2. 生成SSL密钥和证书
生成CA证书ca.crt，服务器密钥文件server.key和服务器证书sever.crt。
```shell
# 生成CA密钥
openssl genrsa -out ca.key 2048
# 生成CA证书，days参数以天为单位设置证书的有效期，在本过程中会要求输入证书的所在地、公司名、站点名等。
openssl req -x509 -new -nodes -key ca.key -days 365 -out ca.crt
# 生成服务器证书RSA的密钥对
openssl genrsa -out server.key 2048
# 生成服务器证书CSR，本过程中会要求输入证书所在地、公司名、站点名等。
openssl req -new -key server.key -out server.csr
# 生成服务器端证书server.crt
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
```
上述命令生成服务器端证书时，必须在Common Name（CN）字段中如实输入站点的访问地址。即如果站点通过www.mysite.com访问，则必须定义CN=www.mysite.com；如果通过IP地址访问，则需设置CN为具体的IP地址。
3. 将证书配置到Web服务器
站点配置文件中添加server段，参数ssl_certificate和ssl_certificate_key需要分别指定生成的服务器证书和服务器密钥的全路径文件名。
4. 在客户端安装CA证书
