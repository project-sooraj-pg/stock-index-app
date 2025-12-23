from backend.app.core.configuration import configuration
from backend.app.model.param.index_construction import BuildIndexParams
from backend.app.model.param.index_retrieval import IndexPerformanceParams, IndexCompositionParams, CompositionChangesParams


class ComputeService:

    async def build_index(self, params: BuildIndexParams) -> str:
        pass

    async def get_index_performance(self, params: IndexPerformanceParams):
        pass

    async def get_index_composition(self, params: IndexCompositionParams):
        pass

    async def get_composition_changes(self, params: CompositionChangesParams):
        pass


def get_compute_service():
    return ComputeService()

