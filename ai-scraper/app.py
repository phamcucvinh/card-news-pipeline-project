import os
import json
import subprocess
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
import gradio as gr

subprocess.run(["playwright", "install"])
load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# LLM
repo_id = "Qwen/Qwen2.5-72B-Instruct"
llm_model_instance = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=128,
    temperature=0.5,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

# Embeddings
embedder_model_instance = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-l6-v2",
    task="feature-extraction",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

graph_config = {
    "llm": {
        "model_instance": llm_model_instance,
        "model_tokens": 100000,
    },
    "embeddings": {
        "model_instance": embedder_model_instance,
    },
}


def clean_json_string(json_str):
    json_start = json_str.find("{")
    if json_start == -1:
        json_start = json_str.find("[")
    if json_start == -1:
        return json_str
    cleaned_str = json_str[json_start:]
    try:
        json.loads(cleaned_str)
        return cleaned_str
    except json.JSONDecodeError:
        return json_str


def scrape_and_summarize(prompt, source):
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt, source=source, config=graph_config
    )
    result = smart_scraper_graph.run()
    if isinstance(result, str):
        result = clean_json_string(result)
    exec_info = smart_scraper_graph.get_execution_info()
    return result, prettify_exec_info(exec_info)


with gr.Blocks() as demo:
    gr.Markdown("# AI Scraper")
    gr.Markdown(
        "URL과 프롬프트를 입력하면 AI가 웹페이지를 분석하여 구조화된 데이터를 반환합니다."
    )
    with gr.Row():
        with gr.Column():
            prompt_input = gr.Textbox(
                label="프롬프트",
                value="이 페이지의 주요 내용을 요약해주세요",
            )
            source_input = gr.Textbox(
                label="URL",
                value="https://example.com",
            )
            scrape_button = gr.Button("스크래핑 시작")
        with gr.Column():
            result_output = gr.JSON(label="결과")
            exec_info_output = gr.Textbox(label="실행 정보")

    scrape_button.click(
        scrape_and_summarize,
        inputs=[prompt_input, source_input],
        outputs=[result_output, exec_info_output],
    )

if __name__ == "__main__":
    demo.launch()
