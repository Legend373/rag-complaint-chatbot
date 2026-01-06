from src.retriever import Retriever
from src.generator import Generator
from src.prompt import PromptTemplate

class RAGSystem:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def ask(self, question):
        results = self.retriever.retrieve(question, k=5)

        context = "\n\n".join(
            f"[{r['product']}] {r['text']}" for r in results
        )

        prompt = PromptTemplate.build(context, question)
        answer = self.generator.generate(prompt)

        return answer, results
