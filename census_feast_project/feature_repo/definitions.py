from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Int64, String
from feast.value_type import ValueType

user = Entity(
    name="user_id",
    join_keys=["user_id"],
    description="Unique user identifier",
    value_type=ValueType.INT64
)

census_file_source = FileSource(
    name="census_data_source",
    path="../data/processed/census_data.parquet",
    timestamp_field="event_timestamp"
)

census_features_view = FeatureView(
    name="census_features",
    entities=[user],
    ttl=timedelta(days=365),
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="workclass", dtype=String),
        Field(name="education", dtype=String),
        Field(name="education_num", dtype=Int64),
        Field(name="marital_status", dtype=String),
        Field(name="occupation", dtype=String),
        Field(name="relationship", dtype=String),
        Field(name="race", dtype=String),
        Field(name="sex", dtype=String),
        Field(name="capital_gain", dtype=Int64),
        Field(name="capital_loss", dtype=Int64),
        Field(name="hours_per_week", dtype=Int64),
        Field(name="native_country", dtype=String),
        Field(name="income", dtype=String),
    ],
    online=True,
    source=census_file_source,
    tags={"dataset": "census_income"}
)