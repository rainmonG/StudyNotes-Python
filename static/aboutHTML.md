> 摘自《Python高效开发实战：Django、Tornado、Flask、Twisted（第3版）》
# 第3章 客户端的编程技术
B/S架构的应用系统在本质上是将客户端和服务端的代码都部署在服务器的网站上。服务器一般为客户端的浏览器产生静态网页和脚本，由后者解释、显示出来并执行动态脚本，所以全栈Web开发者既要精通服务器端编程，又要掌握基于浏览器的客户端开发技术。
本章讲涉及的主要的客户端技术。主要内容：
- HTML语言：讲解HTML的作用及基本语法，包括常用标签、基于DIV的网页布局、HTML表单等。
- CSS样式表：讲解层叠样式表CSS表达HTML的语法和规则，通过CSS集中化并更好地控制HTML元素的属性和方法。
- JavaScript：讲解脚本语言的作用及JavaScript的基本语法，使用文件对象模型DOM生成动态网页效果并响应HTML事件。
- jQuery：是对JavaScript的有效封装，本章讲解了jQuery的作用、语法和最常用的动态效果。
## 3.1 HTML
HTML（HyperText Markup Language，超文本标记语言）是Internet上网页最主要的表现技术。在本身提供经典的UI标签呈现网页内容的同时，还支持不同数据格式的文件嵌入，这使得HTML在Internet上盛行。最新的HTML 5标准增加了更多的强大呈现功能。
### 3.1.1 HTML介绍
因为HTML是文本语言，所以可以用任何编辑器对其进行编辑，只需将文件以*.html或*.htm命名即可。HTML的第1个版本由Internet工程工作小组（Internet Engineering Task Force，IETF）发布于1993年6月，当前最常见的4.01版本由W3C（World Wide Web Consortium，万维网联盟）发布于1999年12月，目前不同的操作系统和浏览器都对4.01版本完全支持。最新的HTML 5于2008年1月形成第1份正式草案，该版本对4.01版本有较大改进。目前HTML 5已获得大多数浏览器的支持，但不同的浏览器对一些特性的支持程度并不一致。
HTML语言的特点如下：
- HTML本身由尖括号表达的标签组成，如`<html>`、`<br>`等。
- 一般标签成对出现，如`<html></html>`、`<body></body>`，在成对标签之间放入标签内容。
- 个别标签没有内容时，则可以用单个标签组成，如`<br/>`。注意尖括号等特殊标签一定要写成半角形式，不能是中文全角形式。
- 标签对`<!-- -->`用于表达注释，注释只在查看HTML代码时出现，在浏览器解析时将不显示其中的内容。
- 标签之间可以嵌套，但不可以交错。**注意：虽然一般标签可以嵌套使用，但不可以在注释标签中嵌套另外一个注释标签。**
- 有些标签有属性字段，在尖括号中通过键值对的方式设置，例如，超链接标签的href属性。
- 标签本身不区分大小写。**注意：虽然语法不区分，但建议开发者遵循所有标签都小写的惯用做法。**
- 超文本标记语言的文件有一个基本的整体结构：`<html>`是整个文件的顶层标签，包含文件中的所有内容；`<html>`的内容由头和实体两部分组成，及`<head></head>`和`<body></body>`。头和实体的内容则由网页设计者通过其他HTML标签进行开发。**注意：HTML头与HTTP头是两个完全不同的概念，应该注意区分。**
- 浏览器一般忽略文件中的回车符，对文件中的空格通常也不按源程序中的效果显示。对于确实需要显示空格和回车符的地方，HTML通过特殊的符号来表达。

| 特殊字符       | 含义   | 显示       |
|------------|------|----------|
| `&nbsp;`   | 空格   | &nbsp;   |
| `&lt;`     | 小于   | &lt;     |
| `&gt;`     | 大于   | &gt;     |
| `&amp;`    | 和号   | &amp;    |
| `&quot;`   | 引号   | &quot;   |
| `&pound;`  | 英镑   | &pound;  |
| `&yen;`    | 日元   | &yen;    |
| `&Lambda;` | 与号   | &Lambda; |
| `&copy;`   | 版权   | &copy;   |
| `&reg;`    | 注册商标 | &reg;    |
| `&trade;`  | 商标   | &trade;  |
| `&times;`  | 乘号   | &times;  |
| `&divide;` | 除号   | &divide; |
| `&sim;`    | 波浪号  | &sim;    |
| `&infin;`  | 无限符号 | &infin;  |
| `&ne;`     | 不等于号 | &ne;     |
### 3.1.2 HTML基本标签
本节只列出常用标签的普通使用方法，但不是HTML的参考手册。
1. 段落<br/>
HTML会忽略源文件中的回车符和换行符，所以需要使用特别的标签来表示段落，标签为`<p></p>`。<br/>
`<hr/>`标签表示单行横线显示，`<br/>`标签表示换行。<br/>
**注意：嵌在`<head>`中的`<meta charset="utf-8"/>`标签是为了让浏览器以UTF-8方式解析文件内容，以便在不同的操作系统和语言环境中能正常显示汉字。**
2. 标题<br/>
HTML有特殊的标签用于显示标题，浏览器会根据显示器的分辨率自动设置标题的字号。标题从大到小分别有6个标签：从`<h1>`到`<h6>`。
3. 字体格式<br/>
除了标题字体，HTML还允许对显示格式进行更多风格的控制。例如，

| 标签             | 描述       | 例子                             |
|----------------|----------|--------------------------------|
| `<b>`          | 粗体字      | <b>111</b>11                   |
| `<i>`          | 斜体字      | <i>111</i>11                   |
| `<del>`        | 删除字      | <del>111</del>11               |
| `<big>`        | 大号字      | <big>111</big>11               |
| `<em>`         | 重点文字     | <em>111</em>11                 |
| `<small>`      | 小号字      | <small>111</small>11           |
| `<strong>`     | 加重语气     | <strong>111</strong>11         |
| `<sub>`        | 下标字      | <sub>111</sub>11               |
| `<sup>`        | 上标字      | <sup>111</sup>11               |
| `<ins>`        | 插入字      | <ins>111</ins>11               |
| `<abbr>`       | 缩写       | <abbr>hyper</abbr>aa           |
| `<acronym>`    | 首字母缩写    | <acronym>abc</acronym>11       |
| `<address>`    | 地址       | <address>111</address>11       |
| `<bdo>`        | 可定义方向的文字 | <bdo>111</bdo>11               |
| `<blockquote>` | 长的引用     | <blockquote>111</blockquote>11 |
| `<q>`          | 短的引用语    | <q>111</q>11                   |
| `<cite>`       | 引用、印证    | <cite>111</cite>11             |
| `<dfn>`        | 一个定义项目   | <dfn>111</dfn>11               |
| `<tt>`         | 打字机代码    | <tt>111</tt>11                 |
| `<var>`        | 变量       | <var>abc</var>11               |
其中大部分用不上吧
4. 链接和图像<br/>
网页之间的链接是HTML的重要功能，链接用`<a>`标签，href属性设置被跳转的URL，target设置在什么窗口中打开链接。<br/>
链接除了可以是文字，也可以图片。图片标签用`<img>`，src设置图片文件名，可以是绝对路径或相对路径，alt设置图片显示失败时替换的显示文字。
5. 表格<br/>
HTML中的表格有两种作用：一种是显示真实的表结构及数据，另一种是控制网页布局。两种方式都通过`<table>`、`<tr>`、`<td>`、`<th>`4个标签分别声明表格、表行、表单元、表头。显示表结构及数据时通常需要为表格设置边框；而控制网页布局时通常需要用到表格嵌套，即在一个表格的标签`<td>`中设置另外一个表格。<br/>
表格常用的属性有border、colspan、rowspan等，分别设置边框宽度、跨列单元、跨行单元等。
6. 列表<br/>
列表是常用的显示方式，HTML中的列表有3种。
- 无序列表：用标签`<ul>`表示列表，用`<li>`表示表项。
- 有序列表：用标签`<ol>`表示列表，用`<li>`表示表项。
- 定义列表：用标签`<dl>`表示列表，用`<dt>`表示被定义词，用`<dd>`表示定义描述。
7. 颜色及背景<br/>
HTML的颜色有3种表达方式：十六进制数字、RGB值或者颜色名称。颜色可以用于设置字体、网页背景等。
8. Flash及音视频播放<br/>
HTML还支持声音、视频、Flash集成，这才令当今网页丰富多彩。可以用`<object>`标签播放嵌入式Flash。<br/>
classid、codebase等属性用于指明客户端播放插件，开发者在使用中无需修改这部分内容，只需修改`<embed>`标签的相关属性就可以设置不同的Flash文件、播放窗口的大小等。<br/>
音频及视频可以通过`<audio>`及`<video>`标签嵌入HTML中，浏览器遇到它们时会将本地可用的音频及视频播放器嵌入页面中。<br/>
HTML可以识别的音频格式包括`mid/midi/rm/wav/wma/mp3`等，视频格式包括`avi/wmv/mpg/mpeg/mov/rm/ram/swf/flv/mp4`等。
### 3.1.3 HTML表单
HTML表单用于从客户端收集用户在浏览器中的输入，是HTML实现客户端与服务器交互的核心方法。作为连接客户端与服务器的纽带，HTML表单也是Python中各Web框架编程都要用到的技术。HTML表单用`<form>`标签表达，其内容由输入控件和提交控件组成，表单的基本工作方式如下：
- 用户在浏览器中输入数据并提交，输入数据的方式可以是文本、单选、多选等。
- 浏览器将输入的数据封装到HTTP Body中并以POST方式提交给服务器。
- 服务器收到请求后将结果Response给浏览器。
1. 文本输入<br/>
HTML表单中的文本输入有单行文本、多行文本、密码框等，分别用标签`<input type="text">`、`<textarea>`、`<input type="password">`表示<br/>
需要给每个输入控件设置一个不同的“name”属性，该属性用于在表单被提交到服务器后，使服务器识别各个输入控件。还可以通过设置rows和cols属性控制输入框的大小。
2. 单项选择<br/>
单项选择有两种表达方式：单选按钮或者下拉列表，它们分别用标签`<input type="radio">`、`<select>/<option>`表达。<br/>
通过在`<input type="radio"`>中设置check属性可以标识哪一项默认被选择，`<option>`标签的selected属性有同样的作用。此外，需要给每一个选项设置value属性，该属性用于在服务器端检查哪一个选项被选择，服务器端在检查Post消息体时将可以收到`name: value`的输入。
3. 多项选择<br/>
多项选择用复选框表达，相应的HTML标签是`<input type="checkbox">`
4. 文件上传<br/>
HTML定义了标准的文件上传控件，相应的HTML标签是`<input type="file">`。标签提供了一个文件名输入框，并且有一个浏览器按钮通过操作系统的文件夹选择框进行文件选择，通过accept属性可以设置文件选择框中的文件筛选器。
5. 边框及提交<br/>
HTML提供了边框控件，可以将所有其他控件包含在一起，以形成较好的视觉效果，标签为`<fieldset>`。完成前面的所有操作后，只需添加提交按钮控件即可，标签为`<submit>`
<form name="input" action="url_form_action">
<fieldset>
    <legend>用户注册</legend>
    <!-- 此处放置所有的输入控件 -->
    <input type="submit" value="注册">
</fieldset>
</form>

## 3.2 CSS
CSS（Cascading Style Sheet，层叠样式表）是一种用来表现HTML等文件的显示样式的语言。通过CSS可以将页面子元素与显示效果分离，提高页面的可复用性和可维护性。样式使用属性键值对的方式工作。CSS预定义了一系列的属性键，开发者可以设置这些属性的值以实现对页面显示的控制。
本节仅学习CSS的核心语法和作用，非CSS完整参考。
### 3.2.1 样式声明方式
当浏览器解析显示HTML页面时，将使用4种样式渲染页面元素，按照优先级从高到低分别为：元素内联样式、页面`<head>`中的内联样式、外联样式、浏览器默认样式。每个浏览器的默认样式都不相同，且开发者无需关心，只需了解前3种样式的设置方法。
1. 元素内联样式<br/>
通过向HTML元素提供style属性的值，可以直接设置元素的内联样式。在一个style中可以设置多个样式属性，多个样式之间以分分隔，每个样式通过冒号分隔键和值。
2. 页面`<head>`中的内联样式<br/>
`<head>`中的样式通过`<style type="text/css">`标签实现，其中的样式将在整个页面中有效，`<style>`标签中的内容由选择器及其样式组成。
3. 外联样式<br/>
外联样式是指把CSS数据放入一个单独的文件中，在HTML中通过`<link rel="stylesheet" type="text/css">`标签引用该文件。<br/>
外部样式文件一般以`*.css`命名，其内容与`<head>`中的内联样式一样，由选择器和样式组成。<br/>
### 3.2.2 CSS语法
样式文件的语法规则很简单，由选择器和样式属性组成
```
selector {key1: value; key2: value ...}
```
每个文件可以有若干条这样的配置。选择器用于指定要设置的HTML元素，CSS中基本的选择器有4种：

| 名称       | 选择器                |
|----------|--------------------|
| 通配选择器    | `*`                |
| 标签选择器    | `S`                |
| class选择器 | `.value`或`S.value` |
| id选择器    | `#value`或`S#value` |

除了基本的选择器，CSS还允许设置选择器的组合：

| 组合名称   | 选择器       |
|--------|-----------|
| 多选择器   | `S1, S2`  |
| 子元素选择器 | `S1 > S2` |
| 后代选择器  | `S1 S2`   |
| 相邻选择器  | `S1 + S2` |
CSS 2和CSS 3中还规定了更丰富的选择器，如属性选择器、链接已点击选择器等。

### 3.2.3 基于CSS+DIV的页面布局
标签`<div>`是HTML用于页面分组的块元素，是专门用来实现元素布局的标签。通过用CSS设置`<div>`的一系列显示属性，可以很好地设计网页的整体效果。

| CSS属性     | 属性含义         |
|-----------|--------------|
| position  | 元素位置类型       |
| direction | 元素内容靠哪侧显示    |
| float     | 元素本身靠屏幕的哪侧显示 |
| height    | 高度           |
| width     | 宽度           |
| margin    | 边框外部的留白      |
| border    | 边框           |
| padding   | 边框内部的填充      |

## 3.3 JavaScript
JavaScript是一种直译式脚本语言，是一种动态类型语言，内置支持类型。它的解释器被称为JavaScript引擎，该引擎内置于现代的所有浏览器中。在HTML网页上使用JavaScript可以为HTML网页增加动态功能。
### 3.3.1 在HTML中嵌入JavaScript
作为一种所有浏览器都支持的解释性脚本语言，在HTML中应用JavaScript一般有如下目的。
- 在客户端读写HTML元素，实现切换文字、滚动条等动态效果。
- 响应浏览器事件，如窗口变大、变小等。
- 验证表单输入，常见于密码的两次输入是否相同、出生年月是否小于当前时间等。

在HTML中嵌入JavaScript有两种方式：内部嵌入和外部链接。内部嵌入是指直接在HTML中用`<script>`标签写入脚本；外部链接是指在HTML中通过文件名引用独立的脚本文件。
> 技巧：外部JavaScript文件通常以`*.js`命名，这样有利于各种编辑器进行智能解析。

<html>
<head>
<!--内部嵌入方式-->
<script>
function hello(){
document.getElementById("message").innerHTML="hello world of javascript";
}
</script>
</head>
<body>
<div id="message"></div>
<!--button是一个按钮控件，其onclick属性定义当用户单击按钮时执行的JavaScript脚本-->
<button type="button" onclick="hello();">Try it</button>
</body>
</html>

### 3.3.2 JavaScript的基本语法
JavaScript的语法与Java很像，但其动态类型的特点与Python也有类似之处。
1. 语句<br/>
JavaScript区分大小写，每条语句以分号`;`结尾，用大括号`{}`表示作用域（而不是Python中的缩进），所以每条语句和变量之间可以有任意空格、Tab符或回车符。JavaScript用C、C++风格的`/*...*/`表示注释。
2. 变量及数据类型<br/>
JavaScript是动态数据类型，即一个变量的类型随着其值的变化而变化。<br/>
关键字`new`是JavaScript中用于新建组件实例的关键字，数组下标从0开始。<br/>
JavaScript中的对象类型与Python中的dictionary类型相似，都是用大括号以键值对的方式表示，但其语法略不同。在Python中dictionary的“键”是任意不可变数据类型。在JavaScript的对象中，“键”只能以成员变量的方式出现，定义时键上不加双引号。
3. 操作符<br/>
常用操作符与Python类似，有`+-*/%==>=<=`等。此外，JavaScript还允许自增操作`++`、自减操作`--`
4. 函数<br/>
JavaScript中用关键字function定义函数。<br/>
和Python一样，JavaScript函数中的返回值是可选的，如果函数有返回值，则可以在函数体中用return语句返回。
5. 判断语句<br/>
JavaScript中有两种判断语句：if和switch。if语句用于对不同的条件执行不同的代码块；switch语句用于对一个表达式的不同结果执行不同的代码块。<br/>
if语句的语义与Python中相似，switch中每个条件的block中可以放多条语句，但是每个块中都应该以break语句结尾。
6. 循环语句<br/>
JavaScript的循环语句有for和while两种，各有两种用法。for的第1种语法与Java、C、C++中的for语句类似：
```
for (sentence1; sentence2; sentence3)
{
Block_of_loop
}
```
其中sentence1在for语句开始时执行且只执行一次；sentence2在每个loop开始时执行，sentence2应该返回一个布尔值，如果sentence2的结果为true，则执行该loop，否则立即结束for循环；sentence3在每次循环结束时执行。
for的第2种用法和while语句及Python中的for语句用法相似。
```
for (x in array)
{
block_of_loop
}

while (expression)
{
block_of_loop
}

do
{
block_of_loop
}while(expression)
```

### 3.3.3 DOM及其读写
DOM（Document Object Model）是当网页被加载时浏览器创建的页面文档对象模型。DOM用结构化的方式描述了标记语言的文件内容。JavaScript中几乎所有有意义的行为都是围绕DOM展开的，如读写页面元素、响应页面事件、进行表单验证等。<br/>
HTML DOM被构建为树结构，在DOM内部每个HTML页面被描述为一个以document为根节点的树，HTML中的每一个标签<..>都被表示为该树中的一个节点。<br/>
通过操作DOM树，JavaScript可以读、增、删、改HTML标签的元素、内容、属性、样式等。DOM提供了一系列支持JavaScript遍历和修改DOM的方法。
1. 查找节点<br/>
一般情况下在DOM中查找节点时无须遍历树结构，而通过document对象的如下3个函数直接实现：
- getElementById(id)：返回对拥有指定id的第1个对象的引用。
- getElementByName(name)：返回带有指定名称的对象集合。
- getElementByTagName(tagName)：返回带有指定标签名的对象集合。

找到一个节点后，可以根据其相对位置的属性查找周围的节点：

| 属性                  | 描述             |
|---------------------|----------------|
| obj.childNodes      | 获得子节点的节点列表     |
| obj.firstChild      | 获得节点的第1个子节点    |
| obj.lastChild       | 获得节点的最后一个子节点   |
| obj.nextSibling     | 获得节点之后的第1个兄弟节点 |
| obj.parentNode      | 获得节点的父节点       |
| obj.previousSibling | 获得节点之前的第1个兄弟节点 |

2. 增加节点<br/>
查找到一个节点后可以在其中插入子节点，新增节点通过document.createElement()和obj.appendChild()/obj.insertBefore()/obj.replaceChild()
3. 删除节点<br/>
删除节点通过obj.removeChild()实现
4. 访问及修改属性节点<br/>
属性节点是指HTML标签中的属性，以键和值的方式呈现。通过设置属性节点，可以控制一个HTML标签的id、name、CSS等。属性节点的读取与设置通过obj.getAttribute()和obj.setAttribute()函数完成。同时，JavaScript允许以成员变量的方式访问属性节点。
5. 访问及修改节点的内容<br/>
大多数节点都有内容，DOM中通过obj.innerHTML访问和修改节点内容。

### 3.3.4 window对象
在JavaScript编程中，除了用DOM模型访问HTML页面中的内容，有时还需要访问和操作除HTML本身外的一些信息，如浏览器的窗口大小、网址等，这些信息通过window对象和其子对象document（文档）、history（浏览历史）、location（URL相关）、navigator（浏览器）的一些固有属性和方法进行访问。

常用的window对象的属性或方法

| 属性或方法         | 描述                       |
|---------------|--------------------------|
| closed        | 窗口是否已关闭                  |
| document      | 只读，指向document对象          |
| history       | 只读，指向history对象           |
| innerheight   | 只读，窗口的文档显示区高度            |
| innerwidth    | 只读，窗口的文档显示区宽度            |
| location      | 只读，指向location对象          |
| name          | 设置或返回窗口的名称               |
| navigator     | 只读，指向navigator           |
| opener        | 只读，对创建此创建窗口的窗口的引用        |
| outerheight   | 只读，窗口的外部高度               |
| outerwidth    | 只读，窗口的外部高度               |
| pageXOffset   | 设置或返回当前视图相对于页面横向的X位置     |
| pageYOffset   | 设置或返回当前视图相对于页面纵向的Y位置     |
| parent        | 只读，返回父窗口                 |
| screen        | 对screen对象的只读引用           |
| status        | 设置或返回窗口状态栏的文本            |
| top           | 只读，返回最顶层的祖先窗口            |
| alert()       | 显示带有一段消息和一个确认按钮的警告框      |
| close()       | 关闭浏览器窗口                  |
| confirm()     | 显示带有一段消息及确认按钮和取消按钮的对话框   |
| focus()       | 把键盘焦点给予一个窗口              |
| moveBy()      | 可相对于窗口的当前坐标把它移动指定的像素     |
| moveTo()      | 把窗口的左上角移动到一个指定的坐标        |
| open()        | 打开一个新的浏览器窗口或查找一个已命名的窗口   |
| print()       | 打印当前窗口的内容                |
| prompt()      | 显示可提示用户输入的对话框            |
| resizeTo()    | 把窗口的大小调整到指定的宽度和高度        |
| scrollBy()    | 按照指定的像素值来滚动内容            |
| scrollTo()    | 把内容滚动到指定的坐标              |
| setInterval() | 按照指定的周期（以毫秒计）来调用函数或计算表达式 |
| setTimeout()  | 在指定的毫秒数后调用函数或计算表达式       |

document的常用属性

| 属性           | 描述                   |
|--------------|----------------------|
| cookie       | 设置或返回当前文档有关的所有cookie |
| domain       | 只读，当前文档的域名           |
| lastModified | 只读，文档被最后修改的日期和时间     |
| referrer     | 只读，载入当前文档的URL        |
| title        | 只读，当前文档的标题           |

history的常用属性或方法

| 属性或方法     | 描述                  |
|-----------|---------------------|
| length    | 只读，浏览器历史列表中的URL数量   |
| back()    | 加载history列表中的前一个URL |
| forward() | 加载history列表的下一个URL  |

location对象的常用属性或方法

| 属性或方法     | 描述                 |
|-----------|--------------------|
| host      | 设置或返回主机名和当前URL的端口号 |
| hostname  | 设置或返回当前URL的主机名     |
| href      | 设置或返回完整的URL        |
| pathname  | 设置或返回当前URL的路径部分    |
| port      | 设置或返回当前URL的端口号     |
| protocol  | 设置或返回当前URL的协议      |
| search    | 设置或返回问号开始的URL后面的部分 |
| reload()  | 重新加载当前文档           |
| replace() | 用新的文档替换当前文档        |

navigator对象常用属性或方法

| 属性或方法              | 描述                           |
|--------------------|------------------------------|
| appCodeName        | 只读，浏览器的代码名                   |
| appMinorVersion    | 只读，浏览器的次级版本                  |
| appName            | 只读，浏览器的名称                    |
| appVersion         | 只读，浏览器的平台和版本信息               |
| browserLanguage    | 只读，当前浏览器的语言                  |
| cookieEnabled      | 只读，指明浏览器中是否启用Cookie的布尔值      |
| cpuClass           | 只读，浏览器系统的CPU等级               |
| onLine             | 只读，指明系统是否处于脱机模式的布尔值          |
| platform           | 只读，运行浏览器的操作系统平台              |
| ~~systemLanguage~~ | 只读，操作系统使用的默认语言               |
| userAgent          | 只读，由客户机发送给服务器的user-agent头部的值 |
| ~~userLanguage~~   | 只读，操作系统的自然语言                 |
| javaEnabled()      | 读取浏览器是否启用Java                |
devTool里面来看，没有systemLanguage和userLanguage属性，有language和languages

screen对象的常用属性

| 属性                   | 描述                     |
|----------------------|------------------------|
| availHeight          | 只读，显示屏幕的高度             |
| availWidth           | 只读，显示屏幕的宽度             |
| bufferDepth          | 设置或返回调色板的比特深度          |
| colorDepth           | 只读，目标设备或缓冲器上的调色板的比特深度  |
| deviceXDPI           | 只读，显示屏幕每英寸的水平点数        |
| deviceYDPI           | 只读，显示屏幕每英寸的垂直点数        |
| fontSmoothingEnabled | 只读，用户是否在显示控制面板中启用了字体平滑 |
| height               | 只读，显示器屏幕的高度            |
| logicalXDPI          | 只读，显示屏幕每英寸的水平方向的常规点数   |
| logicalYDPI          | 只读，显示屏幕每英寸的垂直方向的常规点数   |
| pixelDepth           | 只读，显示屏幕的颜色分辨率          |
| updateInterval       | 设置或返回屏幕的刷新率            |
| width                | 只读，显示器屏幕的宽度            |
各对象里的宽度高度含义有区别，在我的两个屏幕上读取，也有区别，AOC即使全屏，screen.availHeight也比window.outerHeight高6，宽也是；而ThinkPad的屏幕浏览器窗口最大化的时候对应是相等的。<br/>
另外，至少从浏览器的开发者工具中调用的时候，发现列出的属性有的没有。

### 3.3.5 HTML事件处理
用户在使用浏览器的过程中通常会产生一些事件，如移动鼠标、窗口大小发生变化、播放音频结束等。JavaScript可以响应这些事件所执行的代码，这称为HTML事件处理。事件响应是通过给HTML标签设置事件属性来完成的。<br/>
如果要运行的代码比较多，则可以将这些代码封装到一个函数中。<br/>
HTML中有很多事件可以定义，每个事件可以应用的标签不尽相同。

常用的HTML事件总结

| 事件类型       | 应用的标签                                                  | 事件             | 何时触发              |
|------------|--------------------------------------------------------|----------------|-------------------|
| 鼠标事件       | 所有可见的元素                                                | onclick        | 对象被单击             |
|            |                                                        | oncontextmenu  | 单击鼠标右键打开上下文菜单     |
|            |                                                        | ondbclick      | 双击某对象时            |
|            |                                                        | onmousedown    | 鼠标按钮被按下           |
|            |                                                        | onmouseenter   | 鼠标指针被移动到元素上       |
|            |                                                        | onmouseleave   | 鼠标指针被移出元素         |
|            |                                                        | onmousemove    | 鼠标被移动             |
|            |                                                        | onmouseover    | 鼠标被移动到对象上         |
|            |                                                        | onmouseout     | 鼠标指针被从对象上移开       |
|            |                                                        | onmouseup      | 鼠标按键被松开           |
|            |                                                        | onwheel        | 鼠标滚轮上下滚动          |
| 键盘事件       | 所有可见元素                                                 | onkeydown      | 某个键盘按键被按下         |   
|            |                                                        | onkeypress     | 某个键盘按键被按下并松开      |
|            |                                                        | onkeyup        | 某个键盘按键被松开         |
| 对象事件       | `<img>/<input type="image">/<object>/<script>/<style>` | onerror        | 在加载文档或图像时发生错误     |
|            | `<img>/<body>`等                                        | onabort        | 加载被中断             |
|            | `<body>/<input type="image">/<link>/<script>/<style>`等 | onload         | 一个页面或一副图像完整加载     |
|            | 所有可见元素                                                 | onresize       | 窗口或框架被重新调整大小      |
|            | `<body>/<frameset>`                                    | onunload       | 用户退出页面            |
| 表单事件       | `<form>`                                               | onchange       | 表单元素的内容改变时        |
|            |                                                        | onfocus        | 获取焦点时触发           |
|            |                                                        | oninput        | 元素获取用户的输入         |
|            |                                                        | onreset        | 表单重置时             |
|            |                                                        | onselect       | 用户选取文本时           |
|            |                                                        | onsubmit       | 表单提交时             |
| 剪切板事件      | 所有HTML元素                                               | oncopy         | 用户复制元素内容时         |
|            |                                                        | oncut          | 用户剪切元素时           |
|            |                                                        | onpaste        | 用户粘贴元素内容时         |
| 多媒体音频/视频事件 | `<audio>/<video>`                                      | oncanplay      | 可以开始播放视频、音频时      |
|            |                                                        | onpause        | 视频、音频暂停播放时        |
|            |                                                        | onplay         | 视频、音频开始播放时        |
|            |                                                        | onprogress     | 浏览器下载指定的视频、音频时    |
|            |                                                        | onseeked       | 用户重新定位视频、音频的播放位置后 |
|            |                                                        | onsuspend      | 浏览器读取媒体数据中止时      |
|            |                                                        | onvolumechange | 当前的播放音量发生改变时      |
|            |                                                        | onended        | 播放完成时             |

## 3.4 jQuery
在HTML、CSS、JavaScript成为实际的互联网标准时，专门对它们进行封装和开发的客户端框架库出现了，最优秀的客户端框架库之一就是jQuery。jQuery发布于2006年1月，使用jQuery能更方便地处理HTML、响应事件、实现动画效果，并且方便地为网站提供Ajax交互。在世界前10000个访问最多的网站中，有超过55%的网站在使用jQuery。用一句话总结jQuery：可以让开发者更轻松地写JavaScript代码。
### 3.4.1 使用jQuery
jQuery是一个纯JavaScript客户端库，全部代码被封装在一个文件中。jQuery有以下两种形式的发布版。
- 压缩发布版：compressed，用于正式发布，以`*.min.js`命名，如jquery-1.11.2.min.js。
- 正常发布版：uncompressed，用于阅读和调试，以`*.js`命名，如jquery-1.11.2.js。

每个版本的两种形式在功能上完全相同，只是压缩发布的文件更小。开发者通常在项目开发中使用正常发布版，在项目实际运行中为了使网页更快地被加载而使用压缩发布版。<br/>
开发者可以直接在HTML源文件中引用Internet上的jQuery库链接。<br/>
**技巧：使用Internet上的jQuery库，而不是将其下载到本地再引用有好处，即Internet上的这些jQuery库都做了CDN加速，通常在客户端下载这些文件的速度比下载开发者站点的速度要快。**<br/>
在JavaScript中调用jQuery的基础语法：
```html
$(selector).action()
```
其中$指明引用jQuery库；selector即选择器，用来筛选页面标签元素；action即行为，是对筛选出的元素进行的操作。<br/>
比如toggle()操作，是一个对元素进行隐藏、显示转换的行为。
### 3.4.2 选择器
jQuery中的选择器的概念与CSS中的选择器类似，但是除了按标签名、id等进行选择，jQuery的选择器的功能更丰富。例如，根据标签的特定属性进行选择、根据标签相对于父标签的位置进行选择、根据元素内容进行选择等。

常用的jQuery选择器

| 例子                            | 描述                                |
|-------------------------------|-----------------------------------|
| `$("*")`                      | 选取所有元素                            |
| `$(this)`                     | 选取触发事件的当前HTML元素                   |
| `$("div.container")`          | 选取所有class为container的`<div>`元素     |
| `$("div#one")`                | 选取所有id为one的`<div>`元素              |
| `$("div:last")`               | 选取最后一个`<div>`元素                   |
| `$("table tr:first")`         | 选取第1个`<table>`元素的第1个`<tr>`元素      |
| `$("ul li:fist-child")`       | 选取每个`<ul>`元素的第1个`<li>`元素          |
| `$("[src]")`                  | 选取带有src属性的元素                      |
| `$("div[title='mainFrame']")` | 选取所有title属性值等于mainFrame的`<div>`元素 |
| `$(":text")`                  | 选取所有的单行文本框                        |
| `$("p:visible")`              | 选取所有可见的`<p>`元素                    |
| `$("td:odd")`                 | 选取奇数位置的`<td>`元素                   |
| `$(":enabled")`               | 选取所有可用元素                          |
| `$(document)`                 | 文档对象                              |
| `$("p:contains('星期一')")`      | 选取所有内容中包含“星期一”字样的`<p>`标签          |
| `$(":empty")`                 | 选取所有内容为空的标签                       |

### 3.4.3 行为
jQuery基础语法中的行为（action）包含很多内容，如读取标签内容、设置CSS样式、绑定事件响应代码、jQuery动画等。
1. 标签内容操作<br/>
脚本编程中最常用的操作就是读取、修改某元素的内容和属性，在jQuery中标签内容通过以下机种方式实现。
- .text()：设置或返回标签中的文本内容。
- .html()：设置或返回标签中的HTML内容。
- .val()：设置或返回表单控件的用户输入数据。
- .attr("attr_name")：设置或返回标签的某属性。
- .css("property_name")：设置或返回标签的某CSS属性。

jQuery的每个行为一般有两种使用方式：读取和设置。所以行为普遍有如下特点：用作读取时，开发者可以从行为的返回值获得读到的数据；用作设置时，开发者应该把设置的值作为最后一个参数传递给行为。

2. 标签的新增与删除<br/>
相关行为：
- .append()：在父标签的最后部分插入标签。
- .prepend()：在父元素的最前面部分插入标签。
- .after()：在紧随某元素的后面插入标签。
- .before()：在某元素之前插入标签。
- .remove()：删除标签，同时删除它的所有子标签。
- .empty()：清空标签内容，但不删除标签本身。

对于新增标签，仍然需要通过JavaScript的document.createElement()函数建立，然后，通过上述函数之一插入到现有标签中。
3. 事件响应<br/>
jQuery还封装了对HTML事件的响应处理，每个事件都被定义成一个jQuery行为。用jQuery响应HTML事件的基本语法：
```html
$(selector).EVENT(function() {
// 事件处理代码
});
```
其中EVENT是HTML事件除去开头“on”字样的名字，例如，对于HTML的“onclick”事件，jQuery对应的事件行为是“click”。另外，jQuery中有一个特殊的事件`$(document).ready()`，用于响应文档已全部加载的事件。<br/>
常用的HTML事件都有相应的jQuery行为，名称可参考HTML事件名称。
4. 标签遍历<br/>
与用JavaScript遍历DOM树的一系列相对位置的函数类似，jQuery也提供了一系列对选择器所定位的元素进行前后遍历的行为。

jQuery常用的标签遍历行为

| 行为             | 返回值               |
|----------------|-------------------|
| parent()       | 父元素               |
| parents        | 祖先的集合             |
| parentsUntil() | 介于两个给定元素之间的所有祖先元素 |
| children()     | 直接子元素集合           |
| find()         | 后代集合              |
| first()        | 集合中的第一个元素         |
| last()         | 集合中的最后一个元素        |
| siblings       | 兄弟集合              |
| next()         | 紧接着的下一个兄弟         |
| nextall()      | 后面的兄弟集合           |
| nextUntil()    | 介于两个元素中间的所有兄弟元素   |
| prev()         | 前面紧挨着的一个兄弟        |
| prevall()      | 前面的兄弟集合           |
| prevUntil()    | 介于两个元素中间的所有兄弟元素   |

5. jQuery特效<br/>
除了对HTML、CSS、JavaScript相关行为的简单封装，jQuery还提供了一些用JavaScript实现难度较高的动画特效行为。
- .hide()/.show()：隐藏、显示元素。
- .toggle()：在元素的hide()与show()状态之前切换。
- .fadeIn()/.fadeOut()：淡入/淡出效果。
- .fadeToggle()：在fadeIn()和fadeOut()状态之间切换。
- .fadeTo(speed, opacity, callback)：渐变为给定的不透明度。其中，speed可以取值为slow、fast或毫秒数；opacity值介于0与1之间；callback为动作完成后需要回调的函数。
- .slideDown()/.slideUp()：向下滑动出现、向上滑动隐藏。
- .slideToggle()：在s里的Down()和slideUp()状态之间切换。
- .animate({params}, speed, callback)：自定义动画效果。其中，params可以是任意CSS属性。
- .stop()：停止动画。

通过这些方法，开发者已经能实现非常丰富的动态页面功能了。

## 3.5 本章总结
- 能看懂大多数的Web客户端代码，掌握丰富的Web客户端编程技巧。
- HTML常用标签及表单应用。
- 在HTML中嵌入CSS、JavaScript及jQuery客户端库。
- CSS的基本语法、CSS+DIV页面布局技巧。
- JavaScript的基本语法。
- DOM树的概念及其相关操作。
- JavaScript编程中常用的对象，如window、location、navigator、history、screen等的应用。
- HTML事件响应及处理。
- jQuery的概念及基本语法。
- jQuery丰富的选择器功能。
- 使用jQuery配置页面元素、响应HTML事件、开发丰富的页面特效。
