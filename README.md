
# RiceLncRNADatabase
## 项目简介
### RiceLncRNADatabase 是一个面向水稻（*Oryza sativa*）长链非编码RNA（lncRNA）的综合数据库。它整合了水稻lncRNA的基因组定位、表达水平、功能注释等信息，并提供了多种数据检索、浏览和分析工具。用户可以方便地通过关键词检索、基因组位置、表达水平筛选lncRNA，并支持序列相似性搜索（BLAST）、数据下载和提交。

![RiceLncRNADatabase](https://picgo.rice-lncrna.top/20250406081249377.png)

#### 目前，大多数植物数据库均为闭源，严重限制了科研数据的共享与应用。
#### 本数据库致力于构建一个开源的水稻 lncRNA 资源平台，旨在为水稻 lncRNA 功能研究提供高效、便捷的支持，促进水稻分子育种与功能基因组学领域的发展。


## 网站功能模块

| 功能 | 描述 |
|:-----|:-----|
| **首页 (Home)** | 介绍数据库背景与概况，提供快捷入口。 |
| **搜索 (Search)** | 提供基于表达量、基因组位置、lncRNA ID、关键词的多条件检索。 |
| **浏览器 (JBrowse)** | 提供基因组可视化浏览功能，查看lncRNA在水稻基因组中的分布。 |
| **BLAST搜索 (BLAST)** | 支持用户上传序列，进行相似性比对，快速定位匹配的lncRNA。 |
| **下载 (Download)** | 支持批量导出检索到的lncRNA信息，或单个序列FASTA格式下载。 |
| **统计 (Table)** | 提供基础数据统计信息，便于了解lncRNA数据信息。 |
| **下载 (Download)** | 提供数据库所有内容，自由下载。 |
| **人工智能助手 (ChatDB)** | 大模型交互提供数据库使用说明、数据信息，帮助用户理解和使用数据库。 |
| **联系我们 (Contact)** | 提供联系方式和地图，支持用户反馈与交流。 |

---

## 系统架构

- **后端**：Django 4.x（Python框架）
- **前端**：HTML5 + CSS3 + Bootstrap 5（响应式设计）
- **数据库**：Django ORM（支持SQLite / MySQL）
- **工具集成**：
  - **BLAST+**：用于序列相似性搜索。
  - **JBrowse**：用于基因组浏览。
  - **Excel导出**：支持查询结果一键导出。

---

## 主要文件结构

```bash
RiceLncRNADatabase/
│
├── views.py            # 处理各类前端请求与页面渲染
├── models.py           # 定义LncRNA数据库模型
├── urls.py             # 路由配置文件
├── templates/          # 前端页面模板（HTML）
│   ├── index.html      # 首页
│   ├── search.html     # 搜索页面
│   ├── search_result.html # 搜索结果页面
│   ├── blast.html      # BLAST功能页面
│   ├── jbrowse.html    # JBrowse基因组浏览器页面
│   ├── download.html   # 下载页面
│   ├── statistics1.html/statistics2.html # 统计信息页面
│   ├── documentation.html # 文档页面
│   ├── contact.html    # 联系我们页面
│   └── submit.html     # 数据提交页面
└── static/             # 静态文件（图片、CSS、JS、BLAST数据库等）
```

---

## 快速部署

1. 克隆项目：

```bash
git clone https://github.com/YourUsername/RiceLncRNADatabase.git
cd RiceLncRNADatabase
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 迁移数据库：

```bash
python manage.py migrate
```

4. 运行开发服务器：

```bash
python manage.py runserver
```

5. 打开浏览器访问：

```
http://127.0.0.1:8000/
```

---

## 数据使用与引用

本数据库中所有数据仅供非商业科研用途免费使用。若在发表成果时使用到本平台数据，请引用
Shan, X., Xia, S., Peng, L., Tang, C., Tao, S., Baig, A., & Zhao, H. (2025). Identification of Rice LncRNAs and Their Roles in the Rice Blast Resistance Network Using Transcriptome and Translatome. Plants (Under Review). Doi: 10.20944/preprints202502.1634.v1

---

## 联系方式

- **地址**：College of Plant Protection, Weigang Campus, Nanjing Agricultural University, Nanjing, China
- **邮箱**：`sdausxl@126.com`

欢迎反馈问题和提出建议！
