def test_smoke_train():
    # Simple smoke test: importa train
    import src.train as trainmod
    assert hasattr(trainmod, 'train')
