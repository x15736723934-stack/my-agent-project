import os
import streamlit as st


def show_setting():
  st.title("⚙️ 系统 API 与大模型配置")
  st.caption("配置 LLM 引擎与网络检索凭据，支持接入任意兼容 OpenAI 协议的大模型服务。")
  st.markdown("<br>", unsafe_allow_html=True)

  # 从 Session State 或环境变量中读取已有配置
  current_provider = st.session_state.get(
      "llm_provider", "阿里云百炼 (Qwen)"
  )
  current_api_key = st.session_state.get("llm_api_key") or os.getenv(
      "LLM_API_KEY", ""
  )
  current_base_url = st.session_state.get("llm_base_url") or os.getenv(
      "LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
  )
  current_model = st.session_state.get("llm_model_name") or os.getenv(
      "LLM_MODEL_NAME", "qwen-max"
  )
  current_tavily_key = st.session_state.get("tavily_api_key") or os.getenv(
      "TAVILY_API_KEY", ""
  )

  # 1. 预设供应商列表与默认参数
  PRESETS = {
      "阿里云百炼 (Qwen)": {
          "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
          "model": "qwen-max",
      },
      "DeepSeek 官方": {
          "base_url": "https://api.deepseek.com/v1",
          "model": "deepseek-chat",
      },
      "硅基流动 (SiliconFlow)": {
          "base_url": "https://api.siliconflow.cn/v1",
          "model": "deepseek-ai/DeepSeek-V3",
      },
      "Moonshot (Kimi)": {
          "base_url": "https://api.moonshot.cn/v1",
          "model": "moonshot-v1-8k",
      },
      "OpenAI 官方": {
          "base_url": "https://api.openai.com/v1",
          "model": "gpt-4o",
      },
      "自定义 (Custom OpenAI-Compatible)": {
          "base_url": current_base_url,
          "model": current_model,
      },
  }

  with st.form("api_settings_form"):
    st.subheader("🤖 大模型 (LLM) 引擎配置")

    # 选择框索引计算
    provider_names = list(PRESETS.keys())
    default_idx = (
        provider_names.index(current_provider)
        if current_provider in provider_names
        else 0
    )

    selected_provider = st.selectbox(
        "选择模型服务商预设 / 自定义窗口",
        options=provider_names,
        index=default_idx,
        help="选择预设供应商将自动填充基准地址与默认模型名称",
    )

    # 动态关联默认值
    preset_url = PRESETS[selected_provider]["base_url"]
    preset_model = PRESETS[selected_provider]["model"]

    api_key = st.text_input(
        "LLM API Key",
        value=current_api_key,
        type="password",
        placeholder="请输入对应的 API 密钥 (如 sk-xxxx)",
    )

    base_url = st.text_input(
        "API Base URL (服务基准地址)",
        value=preset_url,
        placeholder="https://your-api-domain.com/v1",
        help="符合 OpenAI 协议规范的 Endpoint URL",
    )

    model_name = st.text_input(
        "模型标识符 (Model Name)",
        value=preset_model,
        placeholder="例如: qwen-max, deepseek-chat, gpt-4o",
        help="调用 API 时传入的 model 参数名称",
    )

    st.markdown("---")
    st.subheader("🔍 搜索引擎凭据")

    tavily_key = st.text_input(
        "Tavily Search API Key",
        value=current_tavily_key,
        type="password",
        placeholder="tvly-xxxxxxxxxxxxxxxx",
        help="用于 Agent 执行全网硬核情报与数据检索",
    )

    submit_btn = st.form_submit_button("💾 保存凭据与引擎配置", type="primary")

  if submit_btn:
    # 写入 Session State
    st.session_state["llm_provider"] = selected_provider
    st.session_state["llm_api_key"] = api_key.strip()
    st.session_state["llm_base_url"] = base_url.strip()
    st.session_state["llm_model_name"] = model_name.strip()
    st.session_state["tavily_api_key"] = tavily_key.strip()

    # 同步写入环境变量
    os.environ["LLM_API_KEY"] = api_key.strip()
    os.environ["LLM_BASE_URL"] = base_url.strip()
    os.environ["LLM_MODEL_NAME"] = model_name.strip()
    os.environ["TAVILY_API_KEY"] = tavily_key.strip()

    st.success("✅ 配置保存成功！Agent 系统已就绪，可无缝对接指定的大模型引擎。")


if __name__ == "__main__":
  show_setting()