from backend.app.service.index_composition import IndexCompositionService
from backend.app.service.index_performance import IndexPerformanceService


class IndexExportUseCase:

    def __init__(self, index_performance_service: IndexPerformanceService, index_composition_service: IndexCompositionService):
        self.index_performance_service = index_performance_service
        self.index_composition_service = index_composition_service

    def build_export_dataset(self, index_performance_service: IndexPerformanceService, index_composition_service):
        performance = await self.index_performance_service.get_index_performance(start_date, end_date)
        composition = await self.index_composition_service.get_daily_composition(start_date, end_date)
        changes = await self.index_composition_service.get_composition_changes(start_date, end_date)

        return {
            "Index Performance": performance,
            "Daily Compositions": composition,
            "Composition Changes": changes,
        }

def get_index_export_use_case():
    return IndexExportUseCase()