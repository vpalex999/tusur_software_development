from sources.config.config import Config


def test_set_target_dir():
    config = Config(dest_dir=r'data/node_test')

    assert config.dest_dir == 'data/node_test'
