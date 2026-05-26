import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.agente import executar
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from datasets import Dataset

GOLDEN_SET = Path(__file__).parent / "golden_set.json"
MAX_AMOSTRAS = 5


def _build_ragas_llm():
    return LangchainLLMWrapper(ChatGroq(model="llama-3.1-8b-instant", temperature=0))


def _build_ragas_embeddings():
    return LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    )


def calcular_metricas(perguntas: list[dict]) -> dict:
    amostra = perguntas[:MAX_AMOSTRAS]
    print(f"Avaliando {len(amostra)} de {len(perguntas)} pergunta(s) (MAX_AMOSTRAS={MAX_AMOSTRAS})...")
    rows = []
    for item in amostra:
        print(f"  → {item['pergunta'][:60]}...")
        resultado = executar(item["pergunta"])
        rows.append({
            "question": item["pergunta"],
            "answer": resultado["resposta"],
            "contexts": resultado["contexts"] or ["sem contexto"],
            "ground_truth": item.get("resposta_esperada", ""),
        })

    dataset = Dataset.from_list(rows)
    run_config = RunConfig(
        timeout=120,
        max_retries=2,
        max_wait=60,
        max_workers=2,
    )
    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
        llm=_build_ragas_llm(),
        embeddings=_build_ragas_embeddings(),
        run_config=run_config,
        raise_exceptions=False,
    )
    return scores


def rodar():
    with open(GOLDEN_SET, encoding="utf-8") as f:
        perguntas = json.load(f)

    scores = calcular_metricas(perguntas)
    print("\n=== Resultado RAGAS ===")
    print(scores)


if __name__ == "__main__":
    rodar()
