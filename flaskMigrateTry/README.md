## db.create_all()使用之前是否需要导入models模型？
### 或 flask-migrate在迁移数据库之前是否需要导入models模型？
***
- 我试了这套初始的代码，是需要在manage.py里导入models里的类，这样在creat_all()或migrate、upgrade之后才能生成数据表
- [这是我参考的掘金资料，不保证正确](https://juejin.im/post/5b1935355188257d492ae266)
- 我个人感觉跟flask的app堆栈，db实例化有关，但水平有限，搞不定
- 希望老师可以帮忙看看代码

***
-----------------分割线---------------------------
***
- 谢谢老师，目前结论应该是在创建数据库前需要引入models里的类
- 我查资料说其实很多人没有意识到这个问题是因为在views或blueprint中无意识的导入了models，最后导入了启动文件里，我感觉说的挺对的，我之前做过的小项目，没有明确导入，却生成了数据表，应该就是这样无意识的导入了
***
- 目前还有几个小问题，希望老师可以帮忙看看
- 进入app文件夹下的__init__内
1. 使用import app.models.wordRepertory，并直接未导入继承db.models类，其db.models全部在wordRepertory变量的命名空间下，所以为什么没有继承db.models的类还可以创建数据库？
2. from app.models.wordRepertory import CET4，仅仅导入了CET4的情况下，创建数据库，我发现会全部数据表，创建包括CET6和Kaoyan数据表都会创建，这是为什么？
3. 如果把import app.models.wordRepertory放到create_app里面会报错，放在外面就不会报错，求解原因？

***
-----------------分割线---------------------------
***
- 问题目前从使用层面大概可以解释，具体如何实现有待阅读源码解决
- 在create_all()之前，确实需要导入models，这一点同上，可以确认
- 回答问题1，2
    - 强烈建议阅读[解释连接](https://stackoverflow.com/questions/31082692/how-does-flask-sqlalchemy-create-all-discover-the-models-to-create/31091883#31091883)
    - 个人粗浅解释，继承db.model的类的数据表信息会被记录下来，但需要引入该模块来生效，不管是以模块的形式导入还是将模块中的类导入都可以使其生效，create_all()会查找被记录下来的信息，生成数据表，同理如果没有导入生效，则无法生成数据表
    - 个人理解，数据表信息记录在db.Model.metadata，所以导入一个数据表的类即可让其生效即可，达到导入一个数据表的类就可以创建全部数据表的效果
- 回答问题3
    - 如果把import app.models.wordRepertory放到create_app里面，模块名app和flask的核心对象app重名，会将app从核心对象重新赋值给模块app，所以后面的注册蓝图，app没有注册方法
    - 导致这样的原因是 import 会把模块的名称默认导入，解决办法是将import app.models.wordRepertory as xxx，使用别名
    - 体外话
        - 同理from app.api_1_0 import api as api_blueprint，不能将as去掉不起别名，否则app会被改为模块app，导致下面的app注册蓝图将同样找不到注册的方法
***
- [源码解读](https://www.zhihu.com/question/284904297/answer/444926077)