from sources.config import Config


def test_check_run_config_none():

    config = Config()

    assert config.run_config is None


def test_check_run_config_not_None():
    
    config = Config({'run_config': 'somefile.json'})

    assert config.run_config == 'somefile.json'
