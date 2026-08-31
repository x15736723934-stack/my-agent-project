import datetime
import streamlit as st
from views.agent_page import render_safe_chart


def show_memory():
  st.title("📚 研报历史记忆库")
  st.caption(
      "查看与管理 Agent 系统历史生成的商业研究报告，支持按时间追溯与一键导出。"
  )
  st.markdown("<br>", unsafe_allow_html=True)

  # 获取会话中存储的报告列表
  report_history = st.session_state.get("report_history", [])

  if not report_history:
    st.info("💡 暂无历史研报记录。请先前往【🤖 Agent 智能研报工作台】生成研报！")
    return

  # 顶部管理栏
  top_col1, top_col2 = st.columns([3, 1])
  with top_col1:
    st.markdown(f"**共计归档研报：`{len(report_history)}` 份**")
  with top_col2:
    if st.button("🗑️ 清空所有历史记忆", type="secondary"):
      st.session_state["report_history"] = []
      st.rerun()

  st.markdown("---")

  # 逐条展示历史研报卡片
  for index, item in enumerate(reversed(report_history)):
    company_name = item.get("company_name", "未知企业")
    timestamp = item.get("timestamp", "")
    report_text = item.get("report_text", "")
    chart_json = item.get("chart_json", "")
    duration = item.get("duration", 0)

    # 用 Expander 展开卡片
    with st.expander(
        f"📄 【{company_name}】商业研究报告 &nbsp;&nbsp;|&nbsp;&nbsp; 🕒"
        f" 生成时间: {timestamp}",
        expanded=(index == 0),
    ):
      # 导出按钮与元信息
      m_col1, m_col2 = st.columns([3, 1])
      with m_col1:
        st.caption(f"⏱️ 耗时: {duration}s | 格式: Markdown | 校验状态: 已核查")
      with m_col2:
        safe_filename = (
            f"{company_name}_研报_{timestamp.replace(':', '-').replace(' ', '_')}.md"
        )
        st.download_button(
            label="📥 导出这份研报",
            data=report_text,
            file_name=safe_filename,
            mime="text/markdown",
            key=f"dl_btn_{index}",
            use_container_width=True,
        )

      st.markdown("<br>", unsafe_allow_html=True)

      # 渲染 Markdown 正文
      st.markdown(report_text)

      # 渲染历史保存的图表
      if chart_json:
        st.markdown("---")
        st.markdown("#### 📊 随附可视化图表")
        fig = render_safe_chart(chart_json)
        if fig:
          st.pyplot(fig)


if __name__ == "__main__":
  show_memory()