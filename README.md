# 🤖 基于 Multi-Agent 架构的企业智能研报生成与分析系统

> **An Enterprise Intelligence Research & Analysis System Powered by Multi-Agent Architecture**  
> 基于 **Python + CrewAI + Qwen + Tavily + Streamlit** 构建的智能研报自动化生产与分析平台。用户仅需输入企业名称，系统即可通过多 Agent 协同，完成企业情报搜集、商业分析、研报撰写、内容审核与数据可视化，并支持多格式导出。

---

## 💡 核心亮点 (Highlights)

- 🤖 **Multi-Agent 深度协作**：采用 CrewAI 编排架构，将复杂的研报撰写流程解耦为 **搜集 → 分析 → 撰写 → 审核 → 可视化** 5 个专业角色节点。
- 🌐 **Tool Calling & 联网检索**：集成 Tavily Search API，使 Agent 具备实时获取公开商业数据、财务信息与竞争格局的能力，有效消除模型时效性滞后问题。
- 📊 **结构化数据 & 自动可视化**：Chart Agent 从分析文本中通过 JSON Schema 提取量化数据，并结合 Matplotlib 自动渲染研报专属数据图表，实现“文 + 表 + 图”一体化输出。
- 🛡️ **质量审核机制 (Reviewer Agent)**：引入专门的内容审核节点，对研报中的数据一致性、逻辑合理性及潜在模型幻觉进行二次校验与控制。
- 👁️ **Agent 可观测性与状态持久化**：实时监控 Agent 执行状态、耗时与 Token 消耗；内置 Session 持久化与历史记忆库，支持页面切换无损恢复及历史研报导出。

---

## 🏗️ 架构设计 (System Architecture)

```text
                               【 用户输入: 企业名称 】
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │ Streamlit Web UI    │
                               └──────────┬──────────┘
                                          │
                                          ▼
                         ┌─────────────────────────────────┐
                         │ Multi-Agent Workflow (CrewAI)   │
                         └──────────────┬──────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────┐               ┌───────────────┐               ┌───────────────┐
│  Researcher   │               │    Analyst    │               │    Writer     │
│     Agent     │               │     Agent     │               │     Agent     │
└───────┬───────┘               └───────┬───────┘               └───────┬───────┘
        │ (Tavily 联网搜索)              │ (商业模式/SWOT分析)            │ (结构化 Markdown)
        └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │  Reviewer Agent   │  <-- (质量审核 & 幻觉校验)
                              └─────────┬─────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │    Chart Agent    │  <-- (结构化提取 & Matplotlib 绘图)
                              └─────────┬─────────┘
                                        │
                                        ▼
                            【 最终企业智能研究报告 】
                               ( Markdown / Word / PNG )
```

---

## 👥 Multi-Agent 角色分工

| 角色 Agent | 职责描述 | 工具 / 技术 |
| :--- | :--- | :--- |
| **🔍 Researcher Agent** | 搜集公开信息、主营业务、财务表现、行业竞争及风险情报 | Tavily Search API |
| **📈 Analyst Agent** | 对搜集到的情报进行商业模式、核心竞争力、SWOT 及财务分析 | Qwen LLM |
| **✍️ Writer Agent** | 组织报告架构，整合前序分析结论，生成结构化 Markdown 研报 | Qwen LLM |
| **🛡️ Reviewer Agent** | 深度校验数据一致性、事实逻辑，过滤模型幻觉，管控质量 | Qwen LLM |
| **📊 Chart Agent** | 抽取文本中的量化数据（JSON），判定图表类型并渲染图表 | Matplotlib / JSON Schema |

---

## ⚡ 快速开始 (Quick Start)

### 1. 环境准备
确保本地安装有 **Python 3.10+**，建议使用虚拟环境：

```bash
# 克隆仓库
git clone https://github.com/x15736723934-stack/my-agent-project.git
cd my-agent-project

# 创建并激活虚拟环境
python -m venv venv
# Windows (cmd/PowerShell)
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境变量配置
在项目根目录复制 `.env` 文件并配置相关 API Key：

```bash
cp .env.example .env   # 如果没有 .env.example 可直接创建 .env
```

在 `.env` 中填写你的密钥信息：

```env
# 大语言模型 API 配置 (以 Qwen 为例)
QWEN_API_KEY=your_qwen_api_key_here

# 联网搜索 API 配置
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. 启动应用
```bash
streamlit run app.py
```
启动后在浏览器访问 `http://localhost:8501` 即可进入 Web 工作台。

---

## 🖥️ 功能展示 (Demo)

* **演示示例**：以 **腾讯控股** 为例，输入名称即可全自动生成企业智能研究报告。
* **主要样例输出**：已在 `reports/腾讯企业研报.md` 目录中存放生成的样本研报。

```text
输入: "腾讯控股" 
 -> [Researcher] 检索最新财报与主营业务数据...
 -> [Analyst] 生成 SWOT 与增删业务线分析...
 -> [Writer] 组装 Markdown 研报草案...
 -> [Reviewer] 审核数据事实无误...
 -> [Chart Agent] 绘制营收与业务占比 Matplotlib 图表...
 -> 完成研报生成与导出 (Markdown/Word/PNG)
```

---

## 📁 项目目录结构 (Directory Structure)

```text
agent-project/
│
├── app.py                  # Streamlit 主程序入口 & 页面路由导航
├── requirements.txt        # 项目依赖清单
├── .env.example            # 环境变量模版
├── README.md               # 项目说明文档
├── .gitignore              # Git 忽略配置文件
│
├── views/                  # Streamlit 视图模块
│   ├── agent_page.py       # 智能研报工作台 (Multi-Agent 调度核心逻辑)
│   ├── memory_page.py      # 研报历史记忆库 & 状态恢复
│   └── setting_page.py     # 系统 API 与 Agent 参数配置页面
│
├── images/                 # 项目资源及示意图
│   └── tencent_report.png  
│
└── reports/                # 示例研报输出存储目录
    └── 腾讯企业研报.md      # Demo 生成产物
```

---

## 🛠️ 技术栈 (Tech Stack)

* **核心框架**：`Python 3.10+` / `CrewAI` (Multi-Agent 编排)
* **大语言模型**：`Qwen` (通义千问)
* **搜索引擎**：`Tavily API` (专业 LLM 检索工具)
* **Web UI 界面**：`Streamlit`
* **数据可视化与处理**：`Matplotlib` / `Pandas`
* **文档导出**：`python-docx` / `Markdown`

---

## 🔮 路线图与后续优化 (Roadmap)

- [ ] **RAG 本地知识库**：集成 ChromaDB，实现本地企业年报/PDF 深度检索与 Multi-Agent 融合。
- [ ] **多模态财报解析**：引入 Vision 多模态模型，直接解析财报 PDF 中的复杂图表与表格。
- [ ] **溯源追踪 (Evidence Tracking)**：在研报结论中标注引用来源，支持点击跳转至原文出处。
- [ ] **容错重试机制**：针对 Agent 节点失败增加自动重试与回滚保护机制。

---

## 📄 免责声明 (Disclaimer)

本项目为个人 AI 应用开发实践项目。所生成的企业研究报告内容由 AI 系统与 Agent 工具链自动搜集并生成，仅用于展示 Multi-Agent 技术落地能力，**不构成任何投资、商业或决策建议**。
`` Carlisle ``
