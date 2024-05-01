> 摘自《Python高效开发实战：Django、Tornado、Flask、Twisted（第3版）》
# 第7章 高并发处理框架——Tornado
Tornado是一个可扩展的非阻塞式Web服务器及其相关工具的开源版本。Tornado每秒可以处理数以千计的连接，所以对于实时Web服务来说，Tornado是一个理想的Web框架。
- Tornado概述：学习Tornado的特点及框架组织结构，以及如何在Windows及Linux中安装Tornado。
- 异步编程及协程：学习作为Tornado基础的异步编程及协程技术。
- 开发Tornado网站：从开发一个小型的Tornado站点出发，学习Tornado网站的代码结构、URL映射、RequestHandler、错误处理、重定向、异步访问、处理等。
- 用户身份框架：学习Tornado基于Cookie的用户身份验证、会话维护、防攻击等。
- WebSocket编程：学习WebSocket的概念，以及如何将其应用在基于Tornado框架的开发中。
- Tornado网站部署：学习Tornado框架网站在调试及运营环境中的部署方式。

## 7.1 Tornado概述
### 7.1.1 Tornado介绍
Tornado是使用Python编写的一个强大的可扩展的Web服务器。它在处理大网络流量时表现得足够强健，而在创建和编写时足够轻量级，并能够被用在大量的应用和工具中。Tornado作为FriendFeed网站的基础框架，于2009年9月10日发布，目前已经获得了很多社区的支持，并在一系列不同的场合中得到了应用。除FriendFeed和Facebook外，还有很多公司在生产上转向Tornado，包括Quora、Turntable.fm、Bit.ly、Hipmunk及MyYearbook等。

相对于其他Python网络框架，Tornado有如下特点。
- 完备的Web框架：与Django、Flask等一样，Tornado也提供了URL路由映射、Request上下文、基于模板的页面渲染技术等开发Web应用的必备工具。
- 它是一个高效的网络库，性能与Twisted、Gevent等底层框架相媲美：提供了异步I/O支持、超时事件处理。这使得Tornado除了可以作为Web应用服务器框架，还可以用来做爬虫应用、物联网关、游戏服务器等后台应用。
- 提供高效HTTPClient：除了服务器端框架，Tornado还提供了基于异步框架的HTTP客户端。
- 提供高效的内部HTTP服务器：虽然其他Python网络框架（Django、Flask）也提供了内部HTTP服务器，但它们的HTTP服务器由于性能原因只能用于测试环境。而Tornado的HTTP服务器与Tornado异步调用紧密结合，可以直接用于生产环境。
- 完备的WebSocket支持：WebSocket是HTML 5的一种新标准，实现了浏览器与服务器之间的双向实时通信。

因为Tornado的上述特点，Tornado常被作为大型站点的接口服务框架，而不像Django那样着眼于建立完整的大型网站。

## 7.2 异步及协程基础
协程是Tornado中推荐的编程方式，使用协程可以开发出简捷、高效的异步处理代码。
### 7.2.1 同步与异步I/O
从计算机硬件发展的角度来看，当今计算机系统的CPU和内存速度日新月异，摩尔定律效果非常明显；同时，硬盘、网络等与I/O相关的速度指标却进展缓慢。因此，在当今的计算机应用开发中，减少程序在I/O相关操作中的等待时间是减少资源消耗、提高并发程度的重要手段。

根据Unix Network Programming一书中的定义，同步I/O操作（synchronous I/O operation）导致请求进程阻塞，直到I/O操作完成；异步I/O操作（asynchronous I/O operation）不导致请求进程阻塞。在Python中，同步I/O可以被理解为一个被调用的I/O函数会阻塞调用函数的执行，而异步I/O则不会阻塞调用函数的执行。

### 7.2.2 可迭代（iterable）与迭代器（iterator）
迭代器是访问集合内元素的一种方式。迭代器对象从集合的第1个元素开始访问，直到所有元素都被访问一遍后结束。迭代器不能回退，只能往前进行迭代。

Python中所有Sequence类型簇这样的容器对象都是可迭代的，将迭代的对象传给Python内建函数（built-in function）iter()可以获得相应的迭代器。不断调用next()函数能逐个访问集合中的元素，直到返回StopIteration异常，表示迭代已经完成。虽然列表、元组等可迭代，但相比于迭代器，它们一次性返回所有元素，因此效率上不及迭代器。

### 7.2.3 用yield定义生成器（generator）
定义迭代器：
- 按部就班法：实现一个iterable，然后用iter()函数获取迭代器。
- 生成器法：用yield关键字直接将一个函数转变为一个迭代器，用这种方式定义的迭代器被成为生成器。

### 7.2.4 协程
使用Tornado协程可以开发出类似同步代码的异步行为。同时，因为协程本身不使用线程，所以减少了线程上下文切换的开销，是一种更高效的开发模式。

协程使用了Python关键字yield将调用者挂起和恢复执行。装饰器@gen.coroutine声明这是一个协程函数，由于yield关键字的使用，代码中不用再编写回调函数用于处理访问结果，而可以直接在yield语句的后面编写结果处理语句。
> 为了简化并更好地标识异步IO,从Python 3.5开始引入了新的语法async和await,可以让coroutine的代码更简洁易读。

**调用协程函数**

IOLoop是Tornado的主事件循环对象，Tornado程序通过它监听外部客户端的访问请求，并执行相应的操作。

- 在本身是协程的函数内通过yield关键字调用
- 在IOLoop尚未启动时，通过IOLoop的run_sync()函数调用。该函数阻塞当前函数的执行，直到被调用的协程执行完成。事实上，Tornado要求协程函数在IOLoop的running状态中才能被调用，只不过run_sync函数自动完成了启动、停止IOLoop的步骤：启动IOLoop→调用被lambda封装的协程函数→停止IOLoop
- 在IOLoop已经启动时，通过IOLoop的spawn_callback()函数调用：不会等待被调用协程执行完成，协程会由IOLoop在合适的时机进行调用；没有为开发者提供获取协程函数调用返回值的方法，所以只能用来调用没有返回值的协程函数。

**在协程中调用阻塞函数**

在协程中直接调用阻塞函数会影响协程本身的性能，所以Tornado提供了在协程中利用线程池调度阻塞函数从而不影响协程本身继续执行的方法。

引用concurrent.futures中的ThreadPoolExecutor类，实例化一个由n个线程的线程池。在需要调用阻塞函数的协程中，使用thread_pool.submit调用阻塞函数，并通过yield关键字返回。这样便不会阻塞协程所在线程的继续执行，也保证了阻塞函数前后代码的执行顺序。

**在协程中等待多个异步调用**

Tornado允许在协程中用一个yield关键字等待多个异步调用，只需把这些调用列表或字典的方式传递给yield关键字即可。
> async、await下，大概是引入asyncio.gather，还有相应的loop.run_until_complete

### 7.3.3 RequestHandler
RequestHandler类是配置和响应URL请求的核心类。

1. 接入点函数<br/>
需要子类继承并定义具体行为的函数在RequestHandler中被称为接入点函数（Entry Point），比如常用的get()函数。  
1）RequestHandler.initialize()  
该函数被子类重写，实现了RequestHandler子类实例的初始化过程。可以为该函数传递参数，参数来源于配置URL映射时的定义：Application定义URL映射时以dict方式给出。  
2）RequestHandler.prepare()、RequestHandler.on_finish()  
prepare()函数用于调用请求处理（get、post等）函数之前的初始化处理。而on_finish()用于请求处理结束后的一些清理工作。这两种函数一种用在处理前，一种用在处理后，可以根据实际需要进行重写。通常用prepare()函数做资源初始化操作，而用on_finish()函数做清理对象占用的内存或关闭数据库连接等工作。  
3）HTTP Action处理函数  
每个HTTP Action在RequestHandler中都以单独的函数进行处理
   - RequestHandler.get(*args, **kwargs)
   - RequestHandler.head(*args, **kwargs)
   - RequestHandler.post(*args, **kwargs)
   - RequestHandler.delete(*args, **kwargs)
   - RequestHandler.patch(*args, **kwargs)
   - RequestHandler.put(*args, **kwargs)
   - RequestHandler.options(*args, **kwargs)  

    每个处理函数都以它们对应的HTTP Action小写的方式命名。
2. 输入捕获  
输入捕获是指在RequestHandler中用于获取客户端输入的工具函数和属性，如获取URL查询字符串、POST提交参数等。  
**1）RequestHandler.get_argument(name)、RequestHandler.get_arguments(name)  
这两个函数都返回给定参数的值，前者获得单个值，后者是针对参数存在多个值的情况下使用的，返回多个值的列表。**  
get_argument()、get_arguments()获取的是URL查询字符串参数与POST提交参数的参数合集。  
2）RequestHandler.get_query_argument(name)、RequestHandler.get_query_arguments(name)  
仅从URL查询参数中获取参数值  
3）RequestHandler.get_body_argument(name)、RequestHandler.get_body_arguments(name)  
仅从POST提交参数中获取参数值  
4）RequestHandler.get_cookie(name, default=None)  
根据Cookie名称获取Cookie值  
5）RequestHandler.request  
返回tornado.httputil.HTTPServerRequest对象实例的属性，通过该对象可以获取关于HTTP请求的一切信息  
        
    | 属性名       | 说明                                 |
    |-----------|------------------------------------|
    | method    | HTTP请求方法，如GET、POST等                |
    | uri       | 客户端请求的URI的完整内容                     |
    | path      | URI路径名，即不包括查询字符串                   |
    | query     | URI中的查询字符串                         |
    | version   | 客户端发送请求时使用的HTTP版本，如HTTP/1.1        |
    | headers   | 以字典方式表达的HTTP Headers               |
    | body      | 以字符串方式表达的HTTP消息体                   |
    | remote_ip | 客户端的IP地址                           |
    | protocol  | 请求协议，如HTTP、HTTPS                   |
    | host      | 请求消息中的主机名                          |
    | arguments | 客户端提交的所有参数                         |
    | files     | 以字典方式表达的客户端上传的文件，每个文件名对应一个HTTPFile |
    | cookies   | 客户端提交的Cookie字典                     |

3. 输出响应函数  
输出响应函数是指一组为客户端生成处理结果的工具函数，开发者调用它们以控制URL的处理结果。常用的输出响应函数：  
1）RequestHandler.set_status(status_code, reason=None)  
本函数用于设置HTTP Response中的返回码。如果有描述性的语句，则可以赋值给reason参数。  
2）RequestHandler.set_header(name, value)  
本函数用于以键值对的方式设置HTTP Response中的HTTP头参数。使用set_header配置的Header值将覆盖之前配置的Header。  
3）RequestHandler.add_header(name, value)  
也是用键值对的方式设置HTTP Response中的HTTP头参数，但不同于set_header，add_header配置的参数同键不会覆盖之前的配置。  
4）RequestHandler.write(chunk)  
本函数用于将给定的块作为HTTP Body发送给客户端。在一般情况下，用本函数输出字符串给客户端。如果给定的块是一个字典，则会将这个块以JSON格式发送给客户端，同时将HTTP Header中的Content_Type设置成application/json。  
5）RequestHandler.finish(chunk=None)  
本函数通知Tornado：Response的生成工作已完成，chunk参数是需要传递给客户端的HTTP Body。调用finish()函数后，Tornado将向客户端发送HTTP Response。本方法适用于对RequestHandler的异步请求处理。  
注意：在同步或协程访问处理的函数中，无需调用finish()函数。  
6）RequestHandler.render(template_name, **kwargs)  
本函数用给定的参数渲染模板。函数中第一个参数是传入模板文件名称，之后以命名参数的形式传入多个模板参数。  
Tornado的基本模板语法与Django相同，但是功能弱化，高级过滤器不可用。  
7）RequestHandler.redirect(url, permanent=False, status=None)  
本函数用于进行页面重定向。在RequestHandler处理过程中，可以随时调用进行页面重定向。  
8）RequestHandler.clear()  
本函数清空所有在本次请求之前写入的Header和Body内容。  
9）RequestHandler.set_cookie(name, value)  
本函数按键值对设置Response中的Cookie值。  
10）RequestHandler.clear_all_cookies(path='/', domain=None)
本函数清空本次请求中的所有Cookie。

### 7.3.4 异步协程化
Tornado针对RequestHandler的处理函数使用@tornado.gen.coroutine修饰器，将默认的同步机制改为协程机制。  
> 不知道这一点在当前是否已经out，感觉应该随async await的引入而有了变化。

## 7.4 用户身份验证框架
用户身份认证几乎是所有网站的必备功能，对于Tornado的开发源头FriendFeed和Facebook这样的社交网站尤其如此，所以Tornado框架本身较其他Python框架集成了最为丰富的用户身份验证功能。使用该框架，开发者能够快速开发出既安全又强大的用户身份认证机制。

### 7.4.1 安全Cookie机制
Cookie是很多网站为了辨别用户的身份而存储在用户本地终端（Client Side）的数据，定义于RFC2019。在Tornado中使用RequestHandler.get_cookie()、RequestHandler.set_cookie()函数可以方便地对Cookie进行读写。  
在实际应用中，Cookie经常用于保存Session信息。  
因为Cookie总是被保存在客户端，所以如何保证其不被篡改是服务器端程序必须解决的问题。Tornado提供了为Cookie信息加密的机制，使得客户端无法随意解析和修改Cookie的键值。  
- 在tornado.web.Application对象初始化时赋予cookie_secret参数，该参数值是一个字符串，用于保存本网站Cookie加密时的密钥。
- 在需要读取Cookie的地方用RequestHandler.get_secure_cookie替换原来的RequestHandler.get_cookie调用。
- 在需要写入Cookie的地方用RequestHandler.set_secure_cookie替换原来的RequestHandler.set_cookie调用。  

注意：cookie_secret参数是Cookie的加密密钥，需要做好保护工作，不能泄露给外部人员。

### 7.4.2 用户身份认证
在Tornado的RequestHandler类中有一个current_user属性用于保存当前请求的用户名。RequestHandler.current_user的默认值是None，在get()、post()等处理函数中可以随时读取该属性以获得当前的用户名。RequestHandler.current_user是一个只读属性，所以开发者需要重载RequestHandler.get_current_user()以设置该属性值。 简例：
- 用全局字典dict_sessions保存已经登录的用户信息，比如存“会话ID: 用户名”的键值对。
- 定义公共基类BaseHandler，该类继承自tornado.web.RequestHandler，用于定义本网站所有处理器的公共属性和行为。重载它的get_current_user()函数，其在开发者访问RequestHandler.current_user属性时自动被Tornado调用。
- tornado.web.authenticated装饰器使得具有该装饰器的处理函数在执行之前根据current_user是否已经被赋值来判断用户的身份认证情况。如果已经被赋值，则可以进行正常逻辑，否则自动重定向到网站的登录页面。
- tornado.web.Application的初始化函数中通过login_url参数给出网站的登录页面地址。该地址被用于tornado.web.authenticated装饰器在发现用户尚未验证时重定向到一个URL。
- Tornado使用bytes类型保存cookie值，因此在用get_secure_cookie()函数读取cookie_secret后需要用decode()函数将其转换为string类型再使用。  

注意：加入身份认证的所有页面处理器需要继承自BaseHandler类，而不是直接继承原来的tornado.RequestHandler类。  
商用的用户身份认证还要完善更多的内容，例如加入密码验证机制、管理登录超时、将用户信息保护到数据库等。

### 7.4.3 防止跨站攻击
1. CSRF攻击原理
跨站请求伪造（Cross-Site Request Forgery，CSRF）是一种对网站的恶意利用。通过CSRF，攻击者可以冒用用户的身份，在用户不知情的情况下执行恶意操作。比如：
- 用户首先访问了存在CSRF漏洞的网站Site1，成功登录并获取到了Cookie。此后，所有该用户对Site1的访问均会携带Site1的Cookie，因此被Site1认为是有效操作。
- 此时用户又访问了带有攻击行为的站点Site2，而Site2的返回页面中带有一个访问Site1进行恶意操作的链接，但被伪装成了合法内容。
- 用户一旦点击恶意链接，就在不知情的情况下向Site1站点发送了请求。因为之前用户在Site1进行过登录且尚未退出，所以Site1在收到用户的请求和附带的Cookie时将认为该请求是用户发出的正常请求。此时，恶意站点的目的已经达到。
2. 用Tornado防范CSRF  
为了防止CSRF攻击，要求每个请求包括一个参数值作为令牌来匹配存储在Cookie中的对应值。  
Tornado应用可以通过一个Cookie头和一个隐藏的HTML表单元素向页面提供令牌。这样，当一个合法页面的表单被提交时，它将包括表单值和已存储的Cookie。如果两者匹配，则Tornado应用认定请求有效。  
开启Tornado的CSRF防范功能需要两个步骤：
- 在实例化tornado.web.Application时传入xsrf_cookies=True参数，或者，如果需要初始化的参数过多时，可以通过setting字典的形式传入命名参数。
- 在每个具有HTML表单的模板文件中，为所有表单添加xsrf_form_html()函数标签。`{% module xsrf_form_html() %}`,为表单添加隐藏元素以防止跨站请求。

Tornado的安全Cookie支持和XSRF防范框架减轻了应用开发者的很多负担。没有它们，开发者需要思考很多防范的细节措施，因此Tornado内建的安全功能也非常有用。

## 7.5 HTML 5 WebSocket的概念及应用
Tornado的异步特性使得其非常适合服务器的高并发处理，客户端与服务器的持久连接应用架构就是高并发的典型应用。而WebSocket正是在HTTP客户端与服务端之间建立持久连接的HTML 5标准技术。

### 7.5.1 WebSocket的概念
WebSocket protocol是HTML 5定义的一种新的标准协议（RFC6455），它实现了浏览器与服务器的全双工通信（full-duplex）。
1. WebSocket的应用场景  
传统的HTTP和HTML技术适用于客户端主动向服务器发送请求并获得回复的应用场景。但是随着即时通信需求的增多，这样的通信模型有时并不能满足应用的要求。  
WebSocket与普通Socket通信类似，它打破了原来HTTP的Request和Response一对一的通信模型，同时打破了服务器只能被动地接受客户端请求的应用场景。  
传统的HTTP+HTML方案只适用于客户端主动发出请求的场景，而无法满足服务器端发起的通信要求。虽然有Ajax、Long poll等基于传统HTTP的动态客户端技术，但这些技术无不采用轮询技术，耗费了大量的网络带宽和计算资源。  
而WebSocket正是为了应对这样的场景而制定的HTML 5标准，相对于普通的Socket通信，WebSocket又在应用层定义了基本的交互流程，使得Tornado这样的服务器框架和JavaScript客户端可以构建出标准的WebSocket模块。  
总结WebSocket的特点：
- WebSocket适合服务器端主动推送的场景。
- 相对于Ajax和Long poll等技术，WebSocket通信模型更高效。
- WebSocket仍然与HTTP完成Internet通信。
- 因为它是HTML 5的标准协议，所以不受企业防火墙的拦截。
2. WebSocket的通信原理  
WebSocket的通信原理是在客户端与服务器之间建立TCP持久连接，从而使当服务器有消息需要推送给客户端时能够进行即时通信。  
虽然WebSocket不是HTTP，但由于在Internet上HTML本身是由HTTP封装并进行传输的，因此WebSocket仍然需要与HTTP进行协作。IETF在RFC6455中定义了基于HTTP链路建立WebSocket信道的标准流程。  
客户端通过发送HTTP Request告诉服务器需要建立一个WebSocket长连接信道，在HTTP Header中有4个特殊的字段：
```
Connection: Upgrade
Sec-WebSocket-Key: ...
Upgrade: websocket
Sec-WebSocket-Version: ..
```
它告诉Web服务器，客户端希望建立一个WebSocket连接，客户端使用的WebSocket版本、密钥。  
服务器在收到该Request后，如果同意建立WebSocket连接则返回一个标准的HTTP Response，其中与WebSocket相关的Header信息：
```
Connection: Upgrade
Upgrade: WebSocket
Sec-WebSocket-Accept:...
```
前面的两条数据告诉客户端：服务器已经将本连接转换为WebSocket连接。而Sec-WebSocket-Accept是将客户端发送的Sec-WebSocket-Key加密后产生的数据，以让客户端确认服务器能够正常工作。  
至此，在客户端与服务器之间已经建立了一个TCP持久长连接，双方已经可以随时向对方发送消息。

### 7.5.2 服务端编程
Tornado定义了tornado.websocket.WebSocketHandler类用于处理WebSocket连接的请求，应用开发者应该继承该类并实现其中的open()、on_message()、on_close()函数。
- WebSocketHandler.open()函数：在一个新的WebSocket连接建立时，Tornado框架会调用此函数。在本函数中，开发者可以和在get()、post()等函数中一样用get_argument()函数获取客户端提交的参数，以及用get_secure_cookie/set_secure_cookie操作Cookie等。
- WebSocketHandler.on_message(message)函数：建立WebSocket连接后，当收到来自客户端的消息时，Tornado框架会调用本函数。通常，这是服务器端WebSocket编程的核心函数，通过解析收到的消息做出相应的处理。
- WebSocketHandler.on_close()函数：当WebSocket连接被关闭时，Tornado框架会调用本函数。在本函数中，可以通过访问self.close_code和self.close_reason查询关闭的原因。

除了这3个Tornado框架自动调用的入口函数，WebSocketHandler还提供了两个开发者主动操作WebSocket的函数。
- WebSocketHandler.write_message(message, binary=False)函数：用于向与本连接相对应的客户端写信息。
- WebSocketHandler.close(code=None, reason=None)函数：主动关闭WebSocket连接。其中的code和reason用于告诉客户端连接被关闭的原因。参数code必须是一个数值，而reason是一个字符串。

### 7.5.3 客户端编程
由于WebSocket是HTML 5的标准之一，因此主流浏览器的Web客户端编程语言JavaScript已经支持WebSocket的客户端编程。  
客户端编程围绕着WebSocket对象展开，在JavaScript中，代码里只需要给WebSocket构造函数传入服务器的URL地址，即可创建一个WebSocket对象。可以为该对象的如下事件指定处理函数以响应它们：
- WebSocket.onopen：此事件发生在WebSocket连接建立时
- WebSocket.onmessage：此事件发生在收到了来自服务器的消息时
- WebSocket.onerror：此事件发生在通信过程中有任何错误时
- WebSocket.onclose：此事件发生在与服务器的连接关闭时

除了这些事件处理函数，还可以通过WebSocket对象的两个方法进行主动操作：
- WebSocket.send(data)：向服务器发送消息
- WebSocket.close()：主动关闭现有连接  

### 7.6.3 运营期配置
虽然Tornado的内置IOLoop服务器可以直接作为运营服务器运行，但部署一个应用到生产环境面临着最大化利用系统资源的新挑战。由于Tornado架构的异步特性，无法用大多数Python网络框架标准WSGI进行站点部署，为了强化Tornado应用的请求吞吐量，在运营环境中通常采用反向代理+多Tornado后台实例的部署策略。  
反向代理是代理服务器的一种。它根据客户端的请求，从后端 的服务器上获取资源，然后将这些资源返回给客户端。当前最常用的开源反向代理器是Nginx。  
网站通过Internet DNS服务器将用户浏览器的访问定位到多台Nginx服务器上，每台Nginx服务器又将访问重定向到多台Tornado服务端上。多个Tornado服务既可以部署在一台物理机上，也可以部署在多台物理机上。以资源最大化利用为目的，应该以每个物理机的CPU数量来决定分配在该台物理机上运行的Tornado实例数。  
在Nginx的配置文件中nginx.conf中，除了一些标准配置，最重要的是upstream、listen和proxy_pass指令。upstream中定义了多个后台Tornado服务的IP地址及各自的端口号；server中的listen定义了Nginx监听端口号；proxy_pass定义将所有对根目录的访问由之前定义的upstream中的服务器组提供服务，在默认情况下Nginx以循环方式分配到达的访问请求。  