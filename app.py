import streamlit as st
from chain import work

st.title(":red[_Law_]:blue[ by GPT 🤖]")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "ai", "avatar":"🤖", "content": "我是强大的人工智能助手,您可以向我咨询法律相关问题，我可以问您详细解答"}]
for msg in st.session_state.messages:
    st.chat_message(name=msg["role"],avatar=msg["avatar"]).markdown(msg["content"])

if prompt := st.chat_input(placeholder="应该如何支付员工加班费？",max_chars = 4000,key="prompt"):
    st.session_state.messages.append({"role": "human", "avatar":"🧑", "content": prompt})

    st.chat_message(name="human",avatar="🧑").markdown(prompt)

    with st.chat_message(name="ai",avatar="🤖"):
        with st.spinner("正在生成答案..."):
            result = work.llm_serach_answer(prompt)
        st.session_state.messages.append({"role": "ai", "avatar":"🤖", "content": result})
        st.markdown(result)
