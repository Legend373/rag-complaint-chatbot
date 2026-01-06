from transformers import pipeline

class Generator:
    def __init__(self):
        self.llm = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=256,
            temperature=0.2
        )

    def generate(self, prompt):
        out = self.llm(prompt)[0]["generated_text"]
        return out.split("Answer:")[-1].strip()
