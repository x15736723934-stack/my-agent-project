import streamlit as st
from views.agent_page import show_agent
from views.memory_page import show_memory  # 导入新增的记忆库页面
from views.setting_page import show_setting

st.set_page_config(
    page_title="Agent 智能研报工作台", page_icon="🤖", layout="wide"
)

# 侧边栏导航
with st.sidebar:
  st.title("🧩 导航菜单")
  page = st.radio(
      "选择功能模块",
      [
          "🤖 Agent 智能研报工作台",
          "📚 研报历史记忆库",
          "⚙️ 系统 API 设置",
      ],
  )

if page == "🤖 Agent 智能研报工作台":
  show_agent()
elif page == "📚 研报历史记忆库":
  show_memory()
elif page == "⚙️ 系统 API 设置":
  show_setting()