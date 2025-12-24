from typing import List

from backend.app.model.serializable import SerializableBaseModel
from backend.app.model.core.index_composition import IndexComposition


class IndexCompositionsDto(SerializableBaseModel):
    status: str = "SUCCESS"
    results: List[IndexComposition]