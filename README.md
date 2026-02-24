crud 数据库的增删改查逻辑

models 数据库模型 SQLAlChemy ORM

routers 路由层 按模块划分

schemas 数据验证模型 Pydantic

utils 工具函数

config 相关配置

## 启动项目

推荐（不需要手动激活 venv）：

```bash
.venv/bin/python -m uvicorn main:app --reload
```

或使用 Makefile：

```bash
make run
```
开发的过程：
1. 模块化路由 -> API接口规范文档
2. 定义模型类 -> 数据库表
3. 在crud文件夹里面创建文件，封装数据库操作的方法
4. 在路由处理函数里面调用crud封装好的方法。响应结果