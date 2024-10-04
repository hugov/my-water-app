import logging

from app.repositories.report_repository import ReportRepository

logger = logging.getLogger(__name__)

class ReportService:

    # Order

    @staticmethod
    def report_sales(start_date, end_date):
        _report = ReportRepository.report_sales(start_date, end_date)
        return _report

    