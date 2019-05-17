# lost-and-found-backend

## 简介

使用 `Flask` 框架开发的失物招领后台API

## 项目结构
- migrations 数据库迁移文件
- app/model  数据库模型
- app/route  路由接口
- app/forms.py  表单模型
- app/util.py   部分工具类

## 项目技术架构
整体项目框架采用 `Flask` 配合部分插件进行开发，

采用 `MVC` 架构，由于是 `RESTful API`，所以没有了 `V` 层

模型方面使用 `sqlalchemy` 框架作为 `ORM` 框架，

路由方面使用 `Flask-RESTful` 插件进行 `RESTful API` 风格实现

## 安装运行
```bash
git clone https://github.com/zerolingchan/lost-and-found-backend.git
cp config.py.example config.py
vim config.py # setup variable
pip install -r requirements

# 更新迁移数据库
flask db upgrade
python run.py
```
