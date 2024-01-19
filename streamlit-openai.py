import openai
import streamlit as st

def generate_title_description_with_openai(keyword, openai_api_key, brand_name):
    openai.api_key = openai_api_key

    prompt_text = (
        f"請 aussie_i的語言為繁體中文。根據 Google SEO 的最佳實踐，為關鍵字 '{keyword}' 生成一個吸引人的 SEO title 和 description。"
        f"確保內容簡潔明了，包含關鍵字，並且符合 '{brand_name}' 的品牌定位。"
        f"請在生成的標題前加上「SEO標題：」，在描述前加上「SEO描述：」"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 或 "gpt-4.0-turbo"
        messages=[
            {"role": "system", "content": "您即將與 AI 談論 SEO 標題和描述的生成。"},
            {"role": "user", "content": prompt_text}
        ]
    )
    
    return response['choices'][0]['message']['content']

def parse_generated_content(content):
    # 定義可能的標題和描述前綴
    title_prefixes = ["SEO標題：", "SEO 標題：","標題：", "SEO Title:", "Title:", "SEO标题：", "标题：", "SEO title:", "SEO Title：", " SEO title：", "SEO 寶典：", "SEO Title：", "SEO標題:", "標題:", "SEO title：", "Title：", "標題「"]
    description_prefixes = ["SEO描述：","SEO 描述：", "描述：", "SEO Description:", "Description:", "Meta Description:", "Description：", "SEO description：", "SEO描述:", "描述:", "SEO description:", "Description：", "META description：", "描述："]

    title, description = "", ""
    title_start, description_start = -1, -1

    # 尋找符合的標題前綴
    for title_prefix in title_prefixes:
        title_start = content.find(title_prefix)
        if title_start != -1:
            # 跳過前綴並找到描述的開始
            description_starts = [content.find(d, title_start) for d in description_prefixes if content.find(d, title_start) != -1]
            if description_starts:
                description_start = min(description_starts)
            break

    if title_start != -1 and description_start != -1:
        title = content[title_start + len(title_prefix):description_start].strip()
        # 找到符合的描述前綴
        for description_prefix in description_prefixes:
            if description_start == content.find(description_prefix):
                description = content[description_start + len(description_prefix):].strip()
                break

    return title, description


# Streamlit界面的主要部分
def main():
    st.title("SEO標題和描述生成器")
    
    # 側欄標題
    st.sidebar.header("生成SEO單一標題和描述")

    # 輸入API密鑰
    openai_api_key = st.sidebar.text_input("請輸入OpenAI API密鑰", type="password")

    # 輸入關鍵字
    keyword = st.text_input("輸入關鍵字")

    # 輸入品牌名稱
    brand_name = st.text_input("請輸入品牌名稱", "Bella")

    # 按鈕觸發生成
    if st.button("生成SEO標題和描述"):
        if openai_api_key and brand_name and keyword:
            generated_content = generate_title_description_with_openai(keyword, openai_api_key, brand_name)
            title, description = parse_generated_content(generated_content)
            st.subheader("生成的SEO標題")
            st.write(title)
            st.subheader("生成的SEO描述")
            st.write(description)
        else:
            st.error("請確保所有欄位都填寫完整。")

# 執行Streamlit應用程序
if __name__ == "__main__":
    main()