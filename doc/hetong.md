需求：添加一个合同管理的页面，页面有查询区域：查询字段有合同名称、合同类型、查询按钮、查询结果列表、分页器、操作栏（新增、详情、修改、删除按钮）。
编写前后端代码，实现合同管理的功能。
数据库字段：
合同ID：自增，用于唯一标识合同
合同名称：合同的名称，用于标识合同的名称。
合同类型：合同的类型，例如项目合同、服务合同等。
合同金额：合同的金额，用于标识合同的金额。
合同状态：合同的状态，例如已签署、已过期、已终止等。
合同签署日期：合同签署的日期。
合同生效日期：合同生效的日期，从该日期开始合同生效。
合同过期日期：合同过期的日期，到该日期后合同过期。
合同终止日期：合同终止的日期，到该日期后合同终止。
合同操作人：合同的操作人，例如合同签署人、合同修改人等。
创建时间：合同创建的时间。
创建人：合同创建的人。
更新时间：合同最后更新的时间。
更新人：合同最后更新的人。

以上是合同表的字段，根据以上字段，编写合同管理的前端页面和后端代码，实现合同管理的功能。以及合同管理的前端页面的布局和样式。
建表语句：
```sql
CREATE TABLE `contract` (
  `contract_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '合同ID',
  `contract_name` varchar(255) DEFAULT NULL COMMENT '合同名称',
  `contract_type` varchar(255) DEFAULT NULL COMMENT '合同类型',
  `contract_amount` decimal(10,2) DEFAULT NULL COMMENT '合同金额',
  `contract_status` varchar(255) DEFAULT NULL COMMENT '合同状态',
  `contract_sign_date` date DEFAULT NULL COMMENT '合同签署日期',
  `contract_effective_date` date DEFAULT NULL COMMENT '合同生效日期',
  `contract_expire_date` date DEFAULT NULL COMMENT '合同过期日期',
  `contract_terminate_date` date DEFAULT NULL COMMENT '合同终止日期',
  `contract_operator` varchar(255) DEFAULT NULL COMMENT '合同操作人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `create_by` varchar(255) DEFAULT NULL COMMENT '创建人',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_by` varchar(255) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`contract_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='合同表';
```
后端代码参考以下文件：
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\controllers\enterprose_controller.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\service\enterprose_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\dao\enterprose_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\vo\enterprose_vo.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\do\enterprose_do.py

根据上面的文件，编写合同管理的前端页面和后端代码，实现合同管理的功能。
前端需要在api文件中添加合同管理的接口，例如查询合同列表、新增合同、详情合同、修改合同、删除合同等。
在views文件中添加合同管理的页面，页面有查询区域：查询字段有合同名称、合同类型、查询按钮、查询结果列表、分页器、操作栏（新增、详情、修改、删除按钮）。

代码要求：
1. 前端页面的布局和样式需要符合项目的设计规范。
2. 后端代码需要符合项目的编码规范，例如命名规范、注释规范等。
3. 后端代码需要实现合同管理的功能，例如查询合同列表、新增合同、详情合同、修改合同、删除合同等。
4. 要有详细的注释，注释需要符合项目的注释规范，例如注释格式、注释内容等。
5. 不需要很高级的语法，简单直接完美实现功能即可。
6. 后端尽量使用框架本身自带的功能，例如使用Flask-SQLAlchemy来操作数据库。
