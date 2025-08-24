import gradio as gr
from rag_query import search_papers


def query_interface(question, top_k):
    results = search_papers(question, n_results=top_k)
    print(results)
    if not results:
        return "No results found."

    formatted = ""
    for i, paper in enumerate(results, start=1):
        formatted += f"### {i}. {paper['title']}\n"
        formatted += f"- **Authors:**  {paper['authors']} \n"
        if paper['affiliations']:
            formatted += f"- **Affiliations:** {paper['affiliations']} \n"
        formatted += f"- **Snippet:** {paper['text']}\n\n"
    return formatted


def launch_app():
    with gr.Blocks() as demo:
        gr.Markdown("# 🔍 CS.CV Research Paper Search")
        with gr.Row():
            query = gr.Textbox(label="Enter your question", placeholder="e.g., Recent advances in Vision Transformers")
            top_k = gr.Slider(1, 10, value=3, step=1, label="Top K results")
        output = gr.Markdown()

        run_btn = gr.Button("Search")
        run_btn.click(fn=query_interface, inputs=[query, top_k], outputs=output)

    demo.launch(share=False)


if __name__ == "__main__":
    launch_app()