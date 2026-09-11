import dspy
from dotenv import load_dotenv
from fastapi import FastAPI
from openinference.instrumentation.dspy import DSPyInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from phoenix.otel import register

from pipeline import Pipeline

load_dotenv()  # reads OPENAI_API_KEY from .env

# --- Tracing: must run before any DSPy calls ---
tracer_provider = register(project_name="dspy-pipeline")
DSPyInstrumentor().instrument(tracer_provider=tracer_provider)

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

app = FastAPI()
FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
pipeline = Pipeline()


@app.get("/ask")
def ask(question: str):
    return {"answer": pipeline(question=question).answer}
