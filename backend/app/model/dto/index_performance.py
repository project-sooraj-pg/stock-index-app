from typing import List

from backend.app.model.serializable import SerializableBaseModel
from backend.app.model.core.index_performance import IndexPerformance


class IndexPerformancesDto(SerializableBaseModel):
    status: str = "SUCCESS"
    results: List[IndexPerformance]