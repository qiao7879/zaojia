需求：创建一个审核页面，页面有功能有，顶部查询框，查询按钮，查询结果列表，列表有项目名称，项目类型，审核状态、审核人、审核时间、审核结果操作栏等字段，底部有分页器；操作栏有通过、拒绝按钮，点击项目名称可以进入项目详情页，在详情页面也可以审核。

下面是后端代码接口文件：
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\controllers\project.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\service\project_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\service\project_prefect_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\service\project_prefect_opinion_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\dao\project_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\dao\project_prefect_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\dao\project_prefect_opinion_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\vo\project_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\vo\project_prefect_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\vo\project_prefect_opinion_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\do\project_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\do\project_prefect_service.py
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-backend\module_admin\do\project_prefect_opinion_service.py

现在请你根据这个文件，为我生成一个前端页面，页面有查询框、查询按钮、查询结果列表、分页器、操作栏（通过、拒绝按钮）。
参考下面的前端页面文件：
D:\projects\RuoYi-Vue3-FastAPI\ruoyi-fastapi-frontend\src\views\system\user\index.vue

已完成上面需求的大致功能，接下去修改bug和优化页面效果。已知bug
1.maximum recursion depth exceeded in comparison
2.调整页面显示，在页面分为待审核和已审核两个tab栏，每个tab栏显示对于的数据。
3.在详情页面也可以审核，审核通过后，在列表中显示已审核状态，详情使用项目的详情。
4.添加批量审核功能。
