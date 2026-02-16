import traceback

try:
    import rag.rag_pipeline
    print("MODULE IMPORTED")
except Exception:
    traceback.print_exc()
