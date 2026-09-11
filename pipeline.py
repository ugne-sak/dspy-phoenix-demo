"""
A custom DSPy pipeline. Tracing and LM setup live in run.py / app.py.

Span names come from class names (not attribute names):
    Pipeline.forward
    ├── Predict(GenerateQuery).forward -> ChatAdapter.__call__ -> LM.__call__
    └── Predict(AnswerQuestion).forward -> ChatAdapter.__call__ -> LM.__call__
"""

import dspy


class GenerateQuery(dspy.Signature):
    """Rewrite the question as a concise search query."""

    question: str = dspy.InputField()
    query: str = dspy.OutputField()


class AnswerQuestion(dspy.Signature):
    """Answer the question, using the search query as guidance."""

    question: str = dspy.InputField()
    query: str = dspy.InputField()
    answer: str = dspy.OutputField()


class Pipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.query_generator = dspy.Predict(GenerateQuery)
        self.answerer = dspy.Predict(AnswerQuestion)

    def forward(self, question):
        # Call the modules directly (not .forward()) so their spans are created.
        q = self.query_generator(question=question)
        return self.answerer(question=question, query=q.query)
