import json
import hopsworks


def get_connection():
    """Connect to Hopsworks with the correct host."""
    with open('../config/config.json', 'r') as f:
        config = json.load(f)

    project = hopsworks.login(
        host=config.get('host', 'eu-west.cloud.hopsworks.ai'),
        api_key_value=config['api_key']
    )
    return project


def get_feature_store():
    """Connect and return the feature store."""
    project = get_connection()
    return project.get_feature_store(), project