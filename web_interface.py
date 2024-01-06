import streamlit as st
import os

# 本地文件的路径
file_path = "/Users/dalaoduan/project/privateGPT/poetry.lock"

# 创建一个函数来处理文件下载
def download_file():
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 使用Streamlit的下载按钮功能来触发下载
        # 这里需要将文件内容读取为字节
        with open(file_path, 'rb') as f:
            file_content = f.read()
        st.download_button("Download the file", key="download_file", data=file_content)
    else:
        st.write("The file does not exist.")

# Streamlit的app主函数
if __name__ == "__main__":
    st.title("文件下载界面")
    st.markdown("点击下面的按钮下载文件。")
    download_file()
