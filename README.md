# 基于 Multi-Agent 架构的企业智能研报生成与分析系统

> 基于 Python + CrewAI + Qwen + Tavily + Streamlit 构建的企业智能研报系统。
>
> 用户输入企业名称后，系统通过多个专业 Agent 协同完成企业信息检索、商业分析、研报撰写、质量审核和数据可视化，并最终生成结构化企业研究报告。

---

## 一、项目简介

本项目面向企业信息调研与商业分析场景，尝试使用 Multi-Agent 架构将传统企业研究流程进行自动化。

用户只需要输入目标企业名称，系统即可自动完成：

**企业信息检索 → 企业分析 → 研报生成 → 内容审核 → 数据可视化 → 报告导出**

项目重点实践了：

- LLM 应用开发
- Multi-Agent 架构
- Agent Workflow
- Tool Calling
- 联网信息检索
- 结构化数据处理
- 自动数据可视化
- AI 应用 Web 化
- Agent 执行监控

---

## 二、项目架构

```text
                         用户
                          │
                          ▼
                  Streamlit Web UI
                          │
                          ▼
                 Multi-Agent Workflow
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 Researcher           Analyst           Writer
     Agent              Agent             Agent
        │                 │                 │
        ▼                 ▼                 │
 Tavily Search       企业信息分析             │
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
                     Reviewer Agent
                          │
                          ▼
                      Chart Agent
                          │
                          ▼
                  企业智能研究报告
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
          Markdown       Word        PNG
```

---

## 三、Multi-Agent 设计

### 1. Researcher Agent —— 企业情报搜集
负责通过联网搜索获取目标企业的公开信息。

**主要任务：**
- 企业基本信息
- 企业主营业务
- 商业模式
- 财务信息
- 市场信息
- 行业竞争情况
- 企业风险信息

通过 Tavily Search 获取外部信息，为后续分析 Agent 提供研究素材。

### 2. Analyst Agent —— 商业分析
对 Researcher Agent 获取的信息进行进一步分析。

**主要任务：**
- 企业商业模式分析
- 核心业务分析
- 财务表现分析
- 行业趋势分析
- 竞争格局分析
- 企业核心竞争力分析
- SWOT 分析
- 潜在风险分析

### 3. Writer Agent —— 研报生成
根据前序 Agent 的研究和分析结果，生成结构化企业研究报告。

**主要负责：**
- 组织研报结构
- 整合企业信息
- 编写分析结论
- 输出企业经营分析
- 输出竞争分析
- 输出风险分析
- 生成完整 Markdown 研报

### 4. Reviewer Agent —— 内容质量审核
对生成的研报内容进行二次审核。

**主要检查：**
- 数据一致性
- 信息完整性
- 事实与结论是否匹配
- 数据来源
- 潜在事实错误
- 内容逻辑问题
- 可能存在的模型幻觉

通过 Reviewer Agent 对最终报告进行质量控制。

### 5. Chart Agent —— 数据可视化
负责从研报中提取结构化数据，并根据数据类型生成对应图表。

**主要实现：**
- 财务数据提取
- 数据结构化
- 图表类型判断
- Matplotlib 图表生成
- 图表与研报内容关联

最终实现：**文本分析 + 数据 + 可视化图表** 的组合输出。

---

## 四、核心工作流程

```text
用户输入企业名称
        │
        ▼
Researcher Agent
        │
        ├── Tavily 联网搜索
        │
        ▼
获取企业公开信息
        │
        ▼
Analyst Agent
        │
        ├── 商业模式分析
        ├── 财务分析
        ├── 行业分析
        └── 风险分析
        │
        ▼
Writer Agent
        │
        ▼
生成企业研究报告
        │
        ▼
Reviewer Agent
        │
        ├── 数据检查
        ├── 逻辑检查
        └── 内容审核
        │
        ▼
Chart Agent
        │
        ├── 提取数据
        └── 生成图表
        │
        ▼
最终企业研报
```

---

## 五、主要功能

### 1. 企业智能研究
用户输入企业名称（例如：`腾讯控股`）后，自动启动 Multi-Agent 研究流程，系统自动开始企业信息检索、分析和研报生成。

### 2. 联网信息检索
使用 Tavily Search 为 Researcher Agent 提供联网搜索能力。相比单纯依赖 LLM 内部知识，可以获取更加及时的企业公开信息。

### 3. Multi-Agent 协作
将复杂的企业研究任务拆分成多个专业角色（`Researcher` → `Analyst` → `Writer` → `Reviewer` → `Chart Agent`），通过 Agent Workflow 完成任务分工和协作。

### 4. 自动数据可视化
Chart Agent 自动从研究结果中提取量化数据，并生成对应图表：
```text
企业数据 → 结构化数据 → Chart Agent → Matplotlib → 数据图表
```

### 5. Agent 执行监控与历史记忆库
- **可观测性**：对 Agent 的运行过程进行监控，包括执行状态、耗时、Token 使用情况及 Workflow 执行过程，便于后续优化与成本控制。
- **状态持久化与历史库**：具备 Session State 持久化与研报历史记忆库，切换页面不丢失生成进度，且支持历史研报随时查阅与独立导出。

### 6. 多格式报告输出
系统支持生成 Markdown、Word 及 PNG，方便进行报告预览、导出与结果展示。

---

## 六、技术栈

| 技术 | 用途 |
| :--- | :--- |
| **Python** | 核心开发语言 |
| **CrewAI** | Multi-Agent 编排 |
| **Qwen** | 大语言模型 |
| **Tavily** | 联网搜索 |
| **Streamlit** | Web 应用界面 |
| **Matplotlib** | 数据可视化 |
| **python-docx** | Word 报告生成 |
| **python-dotenv** | 环境变量管理 |

---

## 七、项目界面

### Web 工作台
用户可以在 Streamlit Web 界面输入企业名称，并启动自动研报生成流程。

### Agent 执行过程与记忆库
系统实时展示不同 Agent 的执行状态以及任务流程，并自动归档至“研报历史记忆库”。

---

## 八、Demo：腾讯控股企业研究报告

本项目使用 **腾讯控股** 作为 Demo 企业。

用户输入：`腾讯控股`  
系统自动完成：**企业信息搜索 → 商业分析 → 研报生成 → 内容审核 → 数据可视化 → 最终研报**

最终生成：`腾讯企业研报.md`

**报告内容包括：**
- 企业基本信息
- 核心业务分析
- 商业模式分析
- 财务表现
- 行业分析
- 竞争格局
- SWOT 分析
- 风险分析
- 数据可视化
- 战略分析

> *注：Demo 报告由 AI 系统生成，仅用于展示系统能力，不构成投资建议。*

---

## 九、项目亮点

1. **Multi-Agent 任务拆解**：将复杂的企业研究任务拆分为多个专业 Agent，分别负责信息检索、商业分析、内容生成、质量审核和数据可视化。
2. **Tool Calling**：Researcher Agent 调用 Tavily Search 获取外部公开信息，使 Agent 具备实时外部信息获取能力。
3. **Agent Workflow**：通过顺序式 Workflow（`Research` → `Analysis` → `Writing` → `Review` → `Visualization`）控制执行顺序，形成完整自动化研究链路。
4. **结构化数据可视化**：将模型输出的数据进行结构化处理（JSON Schema），再由程序渲染图表，保证了可视化呈现的可靠性与安全性。
5. **Agent 可观测性**：对 Agent 执行状态、运行时间和 Token 使用情况进行记录，为后续性能优化和 API 成本控制提供依据。
6. **AI 应用 Web 化 & 状态持久化**：使用 Streamlit 将 Multi-Agent 系统封装为可交互 Web 应用，内置 Session 持久化与历史记忆机制，带来优秀的用户体验。

---

## 十、项目运行

### 环境要求
- Python 3.10+（建议使用虚拟环境运行项目）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置 API Key
项目使用环境变量管理 API Key。请在根目录创建 `.env` 文件：

```env
QWEN_API_KEY=your_qwen_api_key
TAVILY_API_KEY=your_tavily_api_key
```
> *请勿将真实 API Key 提交到 GitHub 或上传到公开仓库。*

### 启动项目
```bash
streamlit run app.py
```
启动后访问 Streamlit 提供的本地地址即可进入系统。

---

## 十一、项目目录

```text
agent-project/
│
├── app.py                  # 主程序入口 & 导航路由
├── requirements.txt        # 依赖配置文件
├── README.md               # 项目说明文档
├── .env                    # 环境变量配置文件
├── .gitignore              # Git 忽略文件配置
│
├── views/                  # 页面模块
│   ├── agent_page.py       # 智能研报工作台 (Multi-Agent 核心逻辑)
│   ├── memory_page.py      # 研报历史记忆库页面
│   └── setting_page.py     # 系统 API 配置页面
│
├── images/                 # 项目截图 / 图表配置
│   └── tencent_report.png  # (可选) 演示截图
│
└── reports/                # 示例研报输出目录
    └── 腾讯企业研报.md
```

---

## 十二、项目成果

通过本项目完成了从：
```text
LLM API 调用 → Tool Calling → Multi-Agent → Agent Workflow → 数据处理 → 数据可视化 → Web 应用 → 自动化研报生成
```
的完整 AI 应用开发实践。重点关注 AI 能力与实际业务场景结合，通过 Multi-Agent 架构实现了企业研究流程的自动化与工程化落地。

---

## 十三、后续优化方向

- **RAG 扩展**：接入 ChromaDB，实现基于本地向量库的 RAG + Multi-Agent 深度研报结合。
- **文档解析**：支持企业财报/年报 PDF 文件的上传与深度解析。
- **多模态理解**：引入 Vision 多模态模型，对文档、财报图表及复杂图像进行直接深度分析。
- **归因追踪 (Evidence Tracking)**：增加研报结论与引用信息源的精准关联与跳转。
- **容错强化**：优化 Reviewer Agent 的事实核验能力，增加任务失败重试与节点异常捕获机制。

---

## 十四、免责声明

本项目为个人 AI 应用开发实践项目。项目中的企业研究报告主要用于展示 Multi-Agent 系统的技术能力，报告内容由 AI 模型辅助生成，仅作为 Demo 使用，不构成任何投资、商业或决策建议。
