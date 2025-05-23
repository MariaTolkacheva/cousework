import argparse
import logging
from pathlib import Path

from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

from rag.get_embedding_function import get_embedding_function

CHROMA_PATH = str(Path.home() / "cousework/rag/chroma")

MODELTYPE = "llama3.2"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

COMPARE_TEMPLATE_CONTEXT = """
Compare the answers based only on the following context:

{context}

---

Compare the correct answer {correct_ans} ans user answer {user_ans} based on the above context
"""

COMPARE_TEMPLATE = """Compare the correct answers {correct_ans} ans user answers {user_ans} \
    and give your feedback for each question"""


VERBOSITY_LEVELS = {
    0: logging.WARNING,  # Default if no -v is provided
    1: logging.INFO,     # -v
    2: logging.DEBUG,    # -vv
    3: logging.NOTSET,   # -vvv (logs everything)
}


def setup_logging(verbosity: int):
    level = VERBOSITY_LEVELS.get(min(verbosity, 3), logging.NOTSET)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


logger = logging.getLogger(__name__)


def query_rag(query_text: str):
    logger.debug("preparing the database")
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=embedding_function)

    logger.info("Search the DB")
    results = db.similarity_search_with_score(query_text, k=10)

    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    logger.warning(f'prompt is {prompt}')

    model = OllamaLLM(model=MODELTYPE)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


def compare_results(user_ans: str, correct_ans: str):
    prompt_template = ChatPromptTemplate.from_template(COMPARE_TEMPLATE)
    prompt = prompt_template.format(
        user_ans=user_ans, correct_ans=correct_ans)
    logger.info('prompt for comparing is %s', prompt)

    model = OllamaLLM(model=MODELTYPE)
    response_text = model.invoke(prompt)
    return response_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (-v, -vv, -vvv)"
    )
    args = parser.parse_args()
    setup_logging(args.verbose)

    query_text = args.query_text
    query_rag(query_text)


if __name__ == "__main__":
    main()
