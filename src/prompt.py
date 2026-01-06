class PromptTemplate:
    @staticmethod
    def build(context, question):
        return f"""
You are a financial analyst assistant for CrediTrust Financial.
Answer the user's question using only the complaint excerpts below.

If the context does not contain enough information, say:
"I do not have enough information to answer that."

Context:
{context}

Question:
{question}

Answer:
"""
