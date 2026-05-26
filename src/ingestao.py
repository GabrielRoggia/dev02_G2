from pathlib import Path
from dotenv import load_dotenv
import chromadb
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

DOCS_DIR = Path("documentos")
CHROMA_DIR = "chroma_db"
COLLECTION = "material"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def indexar():
    pdfs = list(DOCS_DIR.glob("*.pdf"))
    if not pdfs:
        print("Nenhum PDF encontrado em documentos/. Adicione PDFs e rode novamente.")
        return

    print(f"Carregando {len(pdfs)} PDF(s)...")
    docs = []
    for pdf in pdfs:
        loader = PyMuPDFLoader(str(pdf))
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} chunks gerados de {len(docs)} páginas")

    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(COLLECTION)

    batch = 100
    for i in range(0, len(chunks), batch):
        fatia = chunks[i : i + batch]
        vecs = embeddings.embed_documents([c.page_content for c in fatia])
        collection.add(
            embeddings=vecs,
            documents=[c.page_content for c in fatia],
            metadatas=[c.metadata for c in fatia],
            ids=[f"chunk_{i + j}" for j in range(len(fatia))],
        )
        print(f"  {min(i + batch, len(chunks))}/{len(chunks)} indexados")

    print("Indexação concluída.")


if __name__ == "__main__":
    indexar()
