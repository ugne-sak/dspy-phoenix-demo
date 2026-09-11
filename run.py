import dspy
from dotenv import load_dotenv
from openinference.instrumentation.dspy import DSPyInstrumentor
from phoenix.otel import register

from pipeline import Pipeline

load_dotenv()  # reads OPENAI_API_KEY from .env

# --- Tracing: must run before any DSPy calls ---
tracer_provider = register(project_name="dspy-pipeline")
DSPyInstrumentor().instrument(tracer_provider=tracer_provider)

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))


if __name__ == "__main__":
    result = Pipeline()(question="Why is the sky blue?")
    print(result.answer)
