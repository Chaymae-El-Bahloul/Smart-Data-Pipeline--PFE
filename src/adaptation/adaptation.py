def adapt(metrics):
    """
    Module d'auto-adaptation basé sur des métriques simples.
    """
    print("Module d'auto-adaptation...")

    if metrics["latency"] > 100:
        decision = "switch_to_stream"
    else:
        decision = "batch_mode"

    print(f"Décision d'adaptation : {decision}")
    return decision
