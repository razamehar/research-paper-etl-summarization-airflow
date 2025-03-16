import arxiv
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def load_models():
    load_dotenv()
    model = ChatOpenAI(max_tokens = 40)
    return model

client = arxiv.Client()

def fetch_papers(query, max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = client.results(search)

    papers = []
    for result in results:
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "published": result.published.strftime("%Y-%m-%d"),
            "url": result.entry_id
        })
    return papers


def summarize_text(text):
    model = load_models()

    prompt = PromptTemplate(
        template=""" 
        Please generate a short summary of the provided text {text}.
        """,
        input_variables=['text'],
    )
    parser = StrOutputParser()

    chain = prompt | model | parser
    result = chain.invoke({'text': text})

    return result