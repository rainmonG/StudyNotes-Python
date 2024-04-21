# 统一教程
## 概述
集成SQLAlchemy内核和ORM组件，是整体介绍。
注意特定主题的ORM-ish程度。
SQLAlchemy Core作为“数据库工具包”，提供工具来管理与数据库的连接、数据库查询和结果交互，以及SQL语句编程构建。

从sqlalchemy命名空间导入与ORM无关的仅限Core部分。使用ORM时，这些概念仍在发挥作用，但不会显式体现在用户代码中。ORM用户应该了解Core，但不会在API中直接使用。

ORM基于Core，提供可选的对象关系映射功能。
ORM提供了一个额外的配置层，允许将用户定义的Python类映射到数据库表和其他结构，并提供称为会话的对象持久机制。它还扩展了核心层SQL表达式语言，允许根据用户定义的对象来组成和调用SQL查询。
与ORM相关的部分从sqlalchemy.orm命名空间里导入。

SQLAlchemy 2.0在ORM中有更高的核心API使用集成水平。
大多数Core概念也会在ORM中显式使用。它们将从sqlalchemy命名空间导入，同时可能使用sqlalchemy.orm构造。
这些主题Core用户和ORM用户都需要了解。

按一般应用的顺序：
首先，所有SQLAlchemy应用都会以一个创建Engine对象开始，
使用事务和DBAPI，涉及Engine的API以及相关对象Connection、Result，
使用数据库元数据，依赖将数据库模式定义为Python对象的系统实现SQL抽象和ORM，
使用Core或ORM进行CRUD操作，ORM的持久性框架，以ORM为中心插入、更新、删除，处理事务。

ORM 关系构造概念

## 建立连接-Engine
Engine对象作为连接到特定数据库的中央源，为这些数据库链接提供工厂和称为连接池的保留空间。

通常是创建一次的全局对象，使用URL字符串进行配置。

Engine在create_engine()首次返回时，实际上还没有尝试连接到数据库。只有在第一次要求它对数据库执行任务时才会连接。这种设计模式称为惰性初始化。

指定参数create_engine.echo，指示Engine将发出的所有SQL记录到Python记录器中。日志显示完整的SQL交互。

使用Engine连接的执行模式vs会话模式

现在大多数SQLAlchemy任务中不会用到文本SQL。

上下文管理器提供数据库连接，并在事务中构建操作。Python DBAPI默认不自动提交，一般调用Connection.commit()

适合项目中实际使用的，事务性：
使用Engine.begin()而非Engine.connect()方法来获取连接，这样机会管理连接的范围，又会预先宣布我们的连接块为交易块，将交易中的所有内容都包含在末尾的COMMIT中，自动提交，即认为整个块成功，或者在异常情况下回滚。
这种风格称为begin once

一般让SQLAlchemy为我们运行DDL序列，作为更高级别操作的一部分，通常不用担心COMMIT。

## executemany
Connection.execute()方法中可以传入一个字典列表作为多参数集合，这代表单个SQL语句会被多次调用，每个参数集一次。
对于多行插入之类的操作，会优化性能。
另有DBAPI级别cursor.executemany()方法

Insert.returning()有用于返回executemany执行结果集的专用逻辑

使用ORM时的基本事务/数据库交互对象称为会话。在现代SQLAlchemy中，该对象的使用方式与连接非常相似，当使用会话时，指的是它用于执行SQL时的内部连接。

在非ORM的架构中使用Session，与Connection的作用差不多，创建模式上有一点区别，也可以在上下文管理器中使用。会话在结束事务后实际上不会保留连接对象，下次需要对数据库执行SQL时，它会从引擎获得新的连接。
Session比Connection有更多使用技巧。execute方法是一样的。

流畅、可组合的SQL查询构造，其基础是代表表格和列等数据库概念的Python对象，统称为数据库元数据。可以以面向Core和面向ORM的风格使用。

```python
from sqlalchemy import  MetaData
```
程序中，一般会在全局应用中设置一个单独的MetaData对象，用模块层级变量（models或dbschema类型的包），或者通过声明基类访问，从而在Table对象中共享。

虽然也可以用多个集合来存放Table对象，表对象也可以不受限制地引用其他集合中的表对象，但对于多张有关联的表来说，实践中放在一个MetaData中建立是更直接的方法，声明和DDL使用都会更有序。

Table - 表示一张数据库中的表，并将其分配给元数据MetaData集合

Column - 表示数据表中的列，并分配给一个Table对象。一般包含一个字符串名称和一个类型对象。父表中的列对象集合通常通过位于Table.c的关联数组访问。

主键可通过Table.primary_key属性查看，一般隐式声明PrimaryKeyConstraint对象。
典型的显式声明的约束是外键，ForeignKeyConstraint对象。
仅涉及目标表上单列的外键约束通常通过ForeignKey对象使用列级速记符号声明。在Column定义中使用ForeignKey时，可以省略该列数据类型指定，会自动参考它关联的列类型。
NOT NULL 约束，使用Column的nullable参数。

MetaData的create_all()方法，传入指向相关数据库的Engine对象，调用则会执行建表。
该DDL创建过程中包含了一些特定SQLite的PRAGMA语句，这些语句在发出CREATE之前会测试每个表的存在。且一系列步骤包含在BEGIN/COMMIT对中，以适应事务DDL。
且创建过程会以正确的顺序发出语句，比如含外键的表会在依赖的表之后再创建。复杂依赖场景中，可以用ALTER将外键应用于表。
drop_all()方法会以与CREATE相反的顺序发出DROP语句，以删除schema中的元素。

注意，MetaData的CREATE/DROP功能适用于测试、中小型程序以及适用短寿命数据库的应用程序。然而，对于长期管理应用程序数据库模式来说，SQLAlchemy的Alembic等模式管理工具可能是更优选，因为随着应用程序设计的变化，它可以管理和编排逐步更改固定数据库模式的过程。

## 声明表
也会建表对象，同事还会提供ORM映射类——使用ORM时SQL的最基本单元，与Core使用也适配良好。
优势：
- 设置列时更简洁且更具Python风格，其中Python类型可以用于表示数据库中使用的SQL类型。
- 得到的映射类可用于生成SQL表达式，通常，Mypy和IDE类型检查器等静态分析工具能从中获取到PEP 484类型信息。
- 允许同时声明表元数据和持久性/对象加载操作中使用的ORM映射类。

使用ORM时，我们声明表元数据的过程通常与声明映射类的过程相结合。映射的类是我们想要创建的任何Python类，然后它将具有属性，这些属性将链接到数据库表中的列。虽然有多种方式实现，但最常见的方式是声明式，允许我们立即声明用户定义的类和表元数据。

### 建立声明基类
获得一个声明类的最便捷的方法是创建一个DeclarativeBase类的子类。再创建该基类的新子类时，结合适当的类级指令，会在类创建时作为一个新的ORM映射类建立，每个类通常（但不限于）指代一个特定的表对象。
假设我们没有从外部提供元数据集，声明类会指代一个自动创建的元数据集合，可通过DeclarativeBase.metadata类属性访问。当我们创建新的映射类时，它们每个都会引用此元数据集合中的一张表。

声明类还指向一个名为注册表的集合，这是SQLAlchemy ORM中的中央“映射配置”单元。虽然很少直接访问，但该对象是映射配置过程的核心，一组ORM映射类会通过此注册表协调。声明类会创建registry，且有相关的选项定制，之后可以通过DeclarativeBase.registry类变量访问该注册表。

DeclarativeBase不是映射类的唯一方法，只是最常用的。注册表还提供其他映射配置模式，包括面向装饰器和命令式的映射类方法。也完全支持在映射时创建Python数据类。

### 声明映射类
建立基类后，可以根据新类来定义表的ORM映射类。现代声明形式由PEP 484类型注释驱动，使用Mapped特殊类型，表示要映射为特定类型的属性。

声明映射过程中Table对象的名字赋给__tablename__属性。一旦类创建，生成的表可以从__table__属性获得。