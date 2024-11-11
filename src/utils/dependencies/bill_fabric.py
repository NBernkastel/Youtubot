from src.services.bill_service import BillService
from src.repo.repositories import BillRepository


def bill_service_fabric():
    return BillService(BillRepository())
