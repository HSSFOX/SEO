# SEO MANGERMENT TOOL（SEO管理程序）
## _The Last Markdown Editor, Ever_

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

SEO程序目前是基于Python以及Qt搭载的云服务站群管理系统，目前支持桌面端Widnwos, OS系统。



## 功能
- 通过导入安装程序批量建站并设置静态文件、备案等。
- 通过AI 输入或导入关键词并自动生成标题->文章。
- 批量式管理站群系统，一键增删改查。
- 每日定时自动发布，根据栏目自动发布文章到指定站点。


## 技术

本项目通过一系列开源项目、语言及框架完成: 
- [PHP] - 用于SEO网页的前端以及后端架构搭建。
- [Python] - 用于SEO程序的后端架构搭建。
- [Qt Framework] - 用于SEO程序的前端页面显示。
- [Jieba] - 用于SEO程序文章内容分词。
- [pip] - 用于Python安装Dependences。


## 安装&依赖
SEO程序包（源码）需在Python3.8+同时配置了Qt环境下运行。
相对于SEO程序本身，可在Windows/OS系统下运行。
> Note: 请确保设备上已安装过任意版本的`Google Chome浏览器`

通过Git Clone安装SEO程序包（源码）👇

```sh
mkdir FOLDER
cd FOLDER
git clone https://github.com/jong757/SeoTool.git
```

| Dependences | Application |
| ------ | ------ |
| PyQt5 | 应用于图形界面生成 |
| Selenium |通过设备本身的Chrome浏览器以及软件搭载的ChromeDrive浏览器，打开各类网页 |
| jieba | 内容分词 |
| keyborad | 与界面上的按钮绑定进行快捷互动 |
| ping3 | 信号测试 |
| redis | 用于软件内的缓存记忆处理 |
| schedule | 定时操作（主要用于自动发布） |
| tldextract | 智能分割域名 |

Python库安装指令 👇
```sh
pip install PyQt5
pip install selenium
pip install jieba
pip install keyboard
pip install ping3
pip install redis
pip install schedule
pip install tldextract
```

## 打包
```sh
pip install Pyinstaller                 # pip安装打包程序
## 无黑框
pyinstaller --noconfirm --onefile --windowed  "{file.py}"
## 黑框
pyinstaller --noconfirm --onefile --console  "{file.py}"

或
pip install auto-py-to-exe              # pip安装打包程序 with ui界面
```



## 插件

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Google Drive | [plugins/googledrive/README.md][PlGd] |

## 文档结构图
```angular2html
api_requests/
├── BtAPI.py                  # Bt API 文件
├── CertificateApi.py         # 证书 API 文件
├── RedisAPI.py               # Redis API 文件
├── TokenAPI.py               # Token API 文件
└── __pycache__/              # 缓存目录

backend/
└── AI_write/
    ├── AI_write.py           # AI 写作主文件
    ├── AI_write_sub.py       # AI 写作子模块
    ├── chatgpt_model.py      # ChatGPT 模型
    ├── perplexity_model.py    # 复杂度模型
    ├── qw_model.py           # QW 模型
    └── __pycache__/          # 缓存目录

auto_publish/
├── auto_publish.py           # 自动发布主文件
└── auto_publishment/
    ├── auto_publishment.py    # 自动发布逻辑
    ├── auto_publishment_window/
    │   ├── auto_publishment_window.py  # 窗口逻辑
    │   └── __pycache__/                  # 缓存目录
    ├── set_table.py          # 设置表格
    ├── table_insertion.py     # 表格插入
    └── __pycache__/          # 缓存目录

FTP_management/
├── FTP_addition/
│   ├── FTP_addition.py       # FTP 添加模块
│   ├── FTP_management.py      # FTP 管理模块
│   └── FTP_setting/
│       ├── FTP_setting.py     # FTP 设置模块
│       └── __pycache__/      # 缓存目录
├── set_table.py              # 设置表格
├── batch_edit/
│   ├── batch_edit.py         # 批量编辑模块
│   └── __pycache__/          # 缓存目录
├── platform_setting/
│   ├── platform_setting.py    # 平台设置模块
│   └── __pycache__/          # 缓存目录
└── __pycache__/              # 缓存目录

methods/
└── __pycache__/              # 缓存目录

model/
├── logs/
│   ├── 2024-08-15_bt_action_logger.log  # 日志文件
│   ├── ai_logs.log              # AI 日志文件
│   ├── app.log                  # 应用日志文件
│   ├── auto_publish_logger.log   # 自动发布日志
│   ├── content_publish_logger.log # 内容发布日志
│   ├── seo_logger.log            # SEO 日志文件
│   └── word_management_logger.log  # 单词管理日志
├── utils.py                    # 工具函数
└── __pycache__/                # 缓存目录

post_summary/
├── bt_class.txt                # BT 类文件
├── README.md                   # 说明文件
├── SEO.py                      # SEO 主文件
├── SEO.spec                    # SEO 配置文件
├── SEO_SSH_update_program.py   # SEO SSH 更新程序
├── SEO_update_program.py       # SEO 更新程序
├── SEO_update_program_ui.py     # SEO 更新程序 UI
└── test/
    ├── gpt_test.py             # GPT 测试文件
    ├── new_words.txt           # 新单词列表
    ├── QTimer test.py          # QTimer 测试文件
    ├── test.py                 # 测试文件
    ├── test02.py               # 测试文件 02
    ├── test03.py               # 测试文件 03
    ├── test04.py               # 测试文件 04
    ├── test05.py               # 测试文件 05
    ├── test_toolButton.py       # 工具按钮测试文件
    ├── test_toolButton.ui       # 工具按钮测试 UI
    ├── textEdit_layout_testing.py # 文本编辑布局测试文件
    ├── textEdit_layout_testing.ui # 文本编辑布局测试 UI
    ├── words.txt               # 单词列表
    ├── 非农数据标题.txt         # 非农数据标题文件

tools/
├── backend_tools/
│   ├── ChromeDriverDownload.py  # Chrome 驱动下载工具
├── frontend_tools/
│   ├── LineEditValidator.py     # 行编辑验证器
│   ├── ListWidgetWithMenu_Model.py # 带菜单的列表控件模型
│   ├── QTableWidgetWithCB.py    # 带复选框的表格控件
│   ├── QTableWidgetWithCBMenu.py # 带复选框和菜单的表格控件
│   ├── QTableWidgetWithMenu.py   # 带菜单的表格控件
│   ├── QWebEngineViewWithDebug.py # 带调试的 Web 引擎视图
│   ├── SearchComboBox.py         # 搜索组合框
│   └── __pycache__/              # 缓存目录

获取文件树状图.py               # 获取文件树状图的脚本

```

## License

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [PHP]: <https://github.com/php>
   
   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
