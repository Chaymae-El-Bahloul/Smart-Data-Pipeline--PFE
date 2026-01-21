from ingestion.ingestion import ingest_data
from preprocessing.preprocessing import preprocess
from processing.processing import process
from adaptation.adaptation import adapt
from storage.storage import store
from visualization.visualization import visualize

def main():
    data = ingest_data()
    data = preprocess(data)
    data = process(data)
    adapt({"latency": 120})
    store(data)
    visualize(data)

if __name__ == "__main__":
    main()
