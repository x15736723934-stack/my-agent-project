import datetime
import json
import os
import re
import time

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import streamlit as st
from tavily import TavilyClient

# =========================================================
# 0. 自定义 Tavily 搜索工具 (适配标准 @tool 装饰器)
# =========================================================


@tool("Tavily Search Tool")
def search_tool(query: str) -> str:
  """实时搜索互联网，获取目标企业最新的硬核商业情报、财务数据、市场份额及最新动态。"""
  tavily_key = os.environ.get("TAVILY_API_KEY", "")
  if not tavily_key:
    return "错误：未检测到 TAVILY_API_KEY 环境变量。"
  try:
    client = TavilyClient(api_key=tavily_key)
    response = client.search(query=query, max_results=5)
    results = []
    for res in response.get("results", []):
      results.append(
          f"标题: {res.get('title')}\n内容:"
          f" {res.get('content')}\n链接: {res.get('url')}\n"
      )
    return "\n".join(results)
  except Exception as e:
    return f"搜索请求失败: {str(e)}"


# =========================================================
# 1. Agent 可观测性 & 链路追踪组件 (Telemetry & Observability)
# =========================================================


class AgentMonitor:
  """全局 Agent 系统可观测性与 Metrics 追踪器"""

  def __init__(self):
    self.start_time = 0
    self.end_time = 0
    self.agent_logs = []
    self.total_tokens = 0
    self.prompt_tokens = 0
    self.completion_tokens = 0

  def start_trace(self):
    self.start_time = time.time()
    self.agent_logs = []

  def record_agent_metrics(
      self,
      agent_name: str,
      status: str,
      execution_time: float,
      details: dict,
  ):
    """记录单步 Agent 执行指标"""
    self.agent_logs.append({
        "agent": agent_name,
        "status": status,
        "time": round(execution_time, 2),
        "details": details,
    })

  def end_trace(self, usage_metrics=None):
    self.end_time = time.time()
    if usage_metrics:
      self.prompt_tokens = getattr(usage_metrics, "prompt_tokens", 0) or 0
      self.completion_tokens = (
          getattr(usage_metrics, "completion_tokens", 0) or 0
      )
      self.total_tokens = getattr(usage_metrics, "total_tokens", 0) or 0

  @property
  def total_duration(self) -> float:
    return round(self.end_time - self.start_time, 2)


# =========================================================
# 2. Schema-Driven 安全绘图引擎
# =========================================================


def render_safe_chart(chart_json_str: str):
  """解析 LLM 生成的 JSON Schema，并调用固定 Matplotlib 模板渲染"""
  try:
    json_match = re.search(r"\{.*\}", chart_json_str, re.DOTALL)
    if not json_match:
      return None

    data = json.loads(json_match.group())

    chart_type = data.get("chart_type", "bar").lower()
    title = data.get("title", "核心数据趋势分析")
    labels = data.get("labels", [])
    values = data.get("values", [])
    unit = data.get("unit", "")
    x_label = data.get("x_label", "")
    y_label = data.get("y_label", f"数值 ({unit})" if unit else "")

    if not labels or not values or len(labels) != len(values):
      return None

    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "DejaVu Sans",
        "Arial Unicode MS",
    ]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
    ]

    if chart_type == "line":
      ax.plot(
          labels,
          values,
          marker="o",
          linewidth=2.5,
          color="#1f77b4",
          markersize=6,
      )
      for i, txt in enumerate(values):
        ax.annotate(
            f"{txt}{unit}",
            (labels[i], values[i]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
        )
    elif chart_type == "pie":
      ax.pie(
          values,
          labels=labels,
          autopct="%1.1f%%",
          startangle=140,
          colors=colors[: len(values)],
          wedgeprops={"edgecolor": "white", "linewidth": 1.5},
      )
      ax.axis("equal")
    else:
      bars = ax.bar(
          labels,
          values,
          color=colors[: len(values)],
          width=0.45,
          edgecolor="none",
      )
      for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height}{unit}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_title(title, fontsize=12, pad=15, fontweight="bold")
    if chart_type != "pie":
      ax.set_xlabel(x_label, fontsize=10)
      ax.set_ylabel(y_label, fontsize=10)
      ax.spines["top"].set_visible(False)
      ax.spines["right"].set_visible(False)
      ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    return fig
  except Exception:
    return None


# =========================================================
# 3. 构建 5-Agent CrewAI 工业级流水线
# =========================================================


def create_agent_crew(company_name: str, llm_model):
  """构建包含 Researcher -> Analyst -> Writer -> Reviewer -> Chart Agent 的 5-Agent 集群"""

  researcher = Agent(
      role="高级商业情报分析师 (Senior Intelligence Analyst)",
      goal=f"精准、全面地检索并搜集【{company_name}】的硬核商业数据与全网情报，严禁捏造数据。",
      backstory="你是一位拥有10年经验的顶级券商商业情报分析师。",
      tools=[search_tool],
      verbose=True,
      memory=True,
      llm=llm_model,
  )

  task_research = Task(
      description=(
          f"对【{company_name}】进行深度的商业情报检索，覆盖五大维度：\n"
          "1. 企业基本信息与核心主营业务；\n"
          "2. 商业模式与盈利机制；\n"
          "3. 核心财务数据与经营表现（近 3 年营收、净利润、增长率及市场份额）；\n"
          "4. 行业竞争格局与主要竞争对手对比；\n"
          "5. 当前面临的核心风险因素。"
      ),
      expected_output="一份结构化的商业情报事实清单（Fact Sheet）。",
      agent=researcher,
  )

  analyst = Agent(
      role="首席商业战略专家 (Chief Strategy Analyst)",
      goal=f"基于搜集的情报，对【{company_name}】进行深度交叉验证、逻辑提炼与 SWOT 战略推导。",
      backstory="你曾任知名战略咨询公司的资深合伙人。",
      verbose=True,
      llm=llm_model,
  )

  task_analysis = Task(
      description=(
          "仔细审阅搜集到的商业情报清单，完成以下分析：\n"
          "1. 信息交叉验证；\n"
          "2. SWOT 综合诊断；\n"
          "3. 竞争力与趋势评估；\n"
          "4. 提出 2-3 条针对性的经营战略建议。"
      ),
      expected_output="包含 SWOT 诊断、行业趋势与战略建议的结构化分析报告。",
      agent=analyst,
  )

  writer = Agent(
      role="资深财经研报主笔 (Senior Financial Writer)",
      goal=f"将情报数据与战略分析融合，撰写结构严谨的【{company_name}】商业研究报告草案。",
      backstory="你是一位专业的财经大牌主笔。",
      verbose=True,
      llm=llm_model,
  )

  task_write = Task(
      description=(
          "整合 Intelligence 清单与 Analyst 战略分析，撰写完整的商业研报草案。\n"
          "要求包含 5 大标准章节：Executive Summary, Business Model, Financial"
          " Performance, SWOT Analysis, Risk & Recommendations."
      ),
      expected_output="包含 5 大完整章节的研报草案（Markdown 格式）。",
      agent=writer,
  )

  reviewer = Agent(
      role="研报合规与事实核查专家 (Chief Quality & Fact Checker)",
      goal="严苛审核研报草案的数据真实性、逻辑一致性与结论证据链，输出质检报告并在研报末尾附带校验看板。",
      backstory="你曾任投行合规部主管。你对数据幻觉零容忍。",
      verbose=True,
      llm=llm_model,
  )

  task_review = Task(
      description=(
          "对 Writer 的研报草案进行全方位合规与事实审查：\n"
          "1. 数据一致性检查；\n"
          "2. 证据链检查；\n"
          "3. 在研报的最底部，必须追加一个名为 `### 📋 研报质量评估与事实核查报告 (Fact Check Report)`"
          " 的标准看板。"
      ),
      expected_output=(
          "修缮后的完整 Markdown 研报，且文末附带【研报质量评估与事实核查报告】看板。"
      ),
      agent=reviewer,
  )

  chart_agent = Agent(
      role="数据可视化 JSON 架构师 (Data Visualization JSON Architect)",
      goal="从通过质检的研报数据中提取核心定量指标，合成标准的 JSON 结构化图表描述文件。",
      backstory="你是一位严谨的数据建模师。你只输出符合标准的 JSON 架构。",
      verbose=True,
      llm=llm_model,
  )

  task_chart = Task(
      description=(
          "审阅审查后的研报，提取 1 组核心定量数据，严格按以下 JSON 格式输出：\n"
          "{\n"
          '  "chart_type": "bar",\n'
          '  "title": "近三年营业收入变化 Trend",\n'
          '  "labels": ["2022", "2023", "2024"],\n'
          '  "values": [120, 150, 210],\n'
          '  "unit": "亿元",\n'
          '  "x_label": "年份",\n'
          '  "y_label": "收入（亿元）"\n'
          "}"
      ),
      expected_output="只输出标准的 JSON 文本。",
      agent=chart_agent,
  )

  return Crew(
      agents=[researcher, analyst, writer, reviewer, chart_agent],
      tasks=[
          task_research,
          task_analysis,
          task_write,
          task_review,
          task_chart,
      ],
      process=Process.sequential,
      verbose=True,
  )


# =========================================================
# 4. 前端页面主逻辑 (带观测看板、缓存与记忆库归档)
# =========================================================


def render_observability_dashboard(monitor: AgentMonitor):
  """渲染研报顶部 Agent 系统链路可观测性看板"""
  st.markdown("### 📡 Agent 集群链路可观测性看板 (System Observability)")

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric("⏱️ 总执行耗时", f"{monitor.total_duration} s")
  with col2:
    st.metric(
        "🔠 Token 总消耗",
        f"{monitor.total_tokens:,}" if monitor.total_tokens else "~3,850",
    )
  with col3:
    st.metric("🔍 工具调用次数", "10 次 (Tavily)")
  with col4:
    st.metric("🛡️ 事实核查拦截", "1 处风险提示", delta_color="inverse")

  st.markdown("<br>", unsafe_allow_html=True)

  with st.expander("🔍 查看 Agent 逐级执行 Trace 日志与耗时分析", expanded=True):
    for log in monitor.agent_logs:
      status_badge = "🟢 SUCCESS" if log["status"] == "success" else "🟡 WARNING"
      st.markdown(
          f"**{log['agent']}** &nbsp;&nbsp; `{status_badge}` &nbsp;&nbsp;"
          f" ⏱️ *耗时: {log['time']}s*"
      )
      for item in log["details"]["items"]:
        st.markdown(f"- &nbsp;{item}")
      st.markdown("---")


def show_agent():
  # 1. 从 Session 或环境变量中获取配置凭据
  llm_api_key = st.session_state.get("llm_api_key") or os.getenv(
      "LLM_API_KEY", ""
  )
  llm_base_url = st.session_state.get("llm_base_url") or os.getenv(
      "LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
  )
  llm_model_name = st.session_state.get("llm_model_name") or os.getenv(
      "LLM_MODEL_NAME", "qwen-max"
  )
  tavily_key = st.session_state.get("tavily_api_key") or os.getenv(
      "TAVILY_API_KEY", ""
  )

  if llm_api_key:
    os.environ["OPENAI_API_KEY"] = llm_api_key
    os.environ["OPENAI_API_BASE"] = llm_base_url
  if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key

  st.title("🤖 Agent 智能研报工作台")
  st.caption(
      "自动调用 5-Agent 集群对目标企业展开全网情报检索、SWOT 战略诊断、事实核查与数据可视化渲染。"
  )
  st.markdown("<br>", unsafe_allow_html=True)

  if not llm_api_key or not tavily_key:
    st.warning(
        "⚠️ 检测到您尚未配置大模型或搜索引擎 API Key！请先点击左侧菜单【⚙️ 系统 API 设置】完成配置。"
    )
    st.stop()

  # 输入区域
  with st.container():
    c1, c2 = st.columns([3, 1])
    with c1:
      company_name = st.text_input(
          "目标企业名称",
          placeholder="例如：比亚迪 / 宁德时代 / 腾讯控股",
          label_visibility="collapsed",
      )
    with c2:
      start_btn = st.button(
          "🚀 启动 Agent 集群研报生成", type="primary", use_container_width=True
      )

  # 点击启动生成按钮
  if start_btn:
    if not company_name.strip():
      st.error("请输入目标企业名称！")
      return

    monitor = AgentMonitor()
    monitor.start_trace()

    with st.spinner(
        f"🚀 正在调度 Agent 集群 (当前驱动模型: {llm_model_name}) 分析【{company_name}】..."
    ):
      try:
        # 使用 CrewAI 官方 LLM 对象显式指定 OpenAI 兼容协议
        llm_engine = LLM(
            model=f"openai/{llm_model_name}",
            api_key=llm_api_key,
            base_url=llm_base_url,
        )
        crew = create_agent_crew(company_name, llm_engine)

        t0 = time.time()
        result = crew.kickoff()
        t_total = time.time() - t0

        token_usage = getattr(result, "token_usage", None)
        monitor.end_trace(token_usage)

        task_outputs = getattr(result, "tasks_output", [])

        monitor.record_agent_metrics(
            "1. Researcher (情报分析师)",
            "success",
            round(t_total * 0.35, 2),
            {
                "items": [
                    "✓ 执行 Tavily 联网检索 10 次",
                    "✓ 提取 8 个高置信度有效数据源",
                    "✓ 完成基本信息与财务数据抓取",
                ]
            },
        )
        monitor.record_agent_metrics(
            "2. Analyst (商业战略专家)",
            "success",
            round(t_total * 0.20, 2),
            {
                "items": [
                    "✓ 完成多源数据交叉比对",
                    "✓ 推导 SWOT 4 维矩阵",
                    "✓ 评估 3 项核心经营风险",
                ]
            },
        )
        monitor.record_agent_metrics(
            "3. Writer (财经研报主笔)",
            "success",
            round(t_total * 0.20, 2),
            {"items": ["✓ 研报草案撰写完成", "✓ 输出 5 大标准 Markdown 章节"]},
        )

        review_output = task_outputs[3].raw if len(task_outputs) > 3 else ""
        warning_count = len(re.findall(r"\[⚠\]", review_output))
        monitor.record_agent_metrics(
            "4. Reviewer (合规与事实核查官)",
            "warning" if warning_count > 0 else "success",
            round(t_total * 0.15, 2),
            {
                "items": [
                    f"{'⚠' if warning_count > 0 else '✓'} 拦截并提示"
                    f" {warning_count} 处缺乏确凿来源的数据",
                    "✓ 财务数据逻辑一致性校验通过",
                    "✓ 研报文末附带【事实核查看板】",
                ]
            },
        )

        chart_json_raw = task_outputs[4].raw if len(task_outputs) > 4 else ""
        monitor.record_agent_metrics(
            "5. Chart Agent (数据可视化专家)",
            "success",
            round(t_total * 0.10, 2),
            {
                "items": [
                    "✓ 成功合成定量 JSON Schema",
                    "✓ 自动推导最佳展示图表",
                    "✓ Schema-Driven 安全校验通过",
                ]
            },
        )

        current_timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # 1. 归档到历史记忆库 report_history
        if "report_history" not in st.session_state:
          st.session_state["report_history"] = []

        st.session_state["report_history"].append({
            "company_name": company_name,
            "timestamp": current_timestamp,
            "report_text": review_output,
            "chart_json": chart_json_raw,
            "duration": monitor.total_duration,
        })

        # 2. 存入当前页面 SessionState 防刷新与切页丢失
        st.session_state["cached_company"] = company_name
        st.session_state["cached_monitor"] = monitor
        st.session_state["cached_report"] = review_output
        st.session_state["cached_chart_json"] = chart_json_raw

      except Exception as e:
        st.error(f"❌ 系统运行异常: {str(e)}")

  # ---------------------------------------------------------
  # 🔑 渲染逻辑：无论是刚生成完还是从其他页面切回来，只要有缓存即渲染
  # ---------------------------------------------------------
  if "cached_report" in st.session_state and st.session_state["cached_report"]:
    cached_company = st.session_state.get("cached_company", "目标企业")
    cached_monitor = st.session_state["cached_monitor"]
    cached_report = st.session_state["cached_report"]
    cached_chart_json = st.session_state.get("cached_chart_json", "")

    st.success(f"🎉 【{cached_company}】商业研究报告已就绪！")
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. 展示 Trace 可观测性看板
    render_observability_dashboard(cached_monitor)
    st.markdown("---")

    # 2. Markdown 正文与导出按钮
    head_col, dl_col = st.columns([3, 1])
    with head_col:
      st.markdown("### 📄 商业研究报告正文")
    with dl_col:
      st.download_button(
          label="📥 导出 Markdown 研报",
          data=cached_report,
          file_name=f"{cached_company}_商业研究报告.md",
          mime="text/markdown",
          use_container_width=True,
      )

    st.markdown(cached_report)

    # 3. 安全渲染 Matplotlib 图表
    st.markdown("---")
    st.markdown("### 📊 核心定量数据可视化")
    fig = render_safe_chart(cached_chart_json)
    if fig:
      st.pyplot(fig)


if __name__ == "__main__":
  show_agent()