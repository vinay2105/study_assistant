import numpy as np
import faiss

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from .models import Chunk, Chat


def get_or_create_chunk(note, key):
    if Chunk.objects.filter(note=note).exists():
        return get_chunk(note)
    return create_chunk(note, key)


def get_chunk(note):
    return list(
        Chunk.objects
        .filter(note=note)
        .order_by("chunk_index")
    )


def create_chunk(note, key):

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        api_key=key,
        task_type="retrieval_document"
    )

    text = note.content
    words = text.split()

    chunk_size = 100
    overlap = 20

    chunks = []

    for i in range(0, len(words), chunk_size - overlap):

        chunk_text = " ".join(words[i:i + chunk_size])

        if not chunk_text.strip():
            continue

        embedding = embedding_model.embed_documents([chunk_text])[0]

        chunk_obj = Chunk.objects.create(
            note=note,
            text=chunk_text,
            chunk_index=i // (chunk_size - overlap),
            embedding=embedding
        )

        chunks.append(chunk_obj)

    return chunks


def get_embedding(note):

    embeddings = [
        chunk.embedding
        for chunk in Chunk.objects
        .filter(note=note)
        .order_by("chunk_index")
    ]

    if not embeddings:
        return np.array([])

    return np.array(embeddings).astype("float32")


def prepare_context(note, chunks, embedding, question, key):

    if embedding.size == 0:
        return ""

    dim = embedding.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embedding)

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        api_key=key,
        task_type="retrieval_query"
    )

    question_embedding = embedding_model.embed_query(question)
    question_embedding = (
        np.array(question_embedding)
        .astype("float32")
        .reshape(1, -1)
    )

    distances, indices = index.search(question_embedding, 3)

    rag_context = "\n".join(
        chunks[i].text
        for i in indices[0]
        if i < len(chunks)
    )

    chats = list(
        Chat.objects
        .filter(note=note)
        .order_by("-created_at")[:10]
    )

    chats.reverse()

    chat_context = "\n".join(
        f"{'User' if c.role == 'user' else 'Assistant'}: {c.text}"
        for c in chats
    )

    return (
        f"Knowledge context:\n{rag_context}\n\n"
        f"Conversation history:\n{chat_context} Respond in clean plain text only, without Markdown or special symbols, using simple sentences and neat line breaks suitable for a basic chat interface. "
    )


def generate_response(context, question, key):

    chat = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash-lite",
        api_key=key
    )

    messages = [
        SystemMessage(
            content="You are a helpful assistant that answers questions based on the provided context."
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion:\n{question}"
        )
    ]

    response = chat.invoke(messages)

    return response.content



