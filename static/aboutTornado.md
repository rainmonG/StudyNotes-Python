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
