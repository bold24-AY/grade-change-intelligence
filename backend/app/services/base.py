from abc import ABC, abstractmethod

class BaseService(ABC):
    """
    Abstract Service Interface for building consistent business logic classes.
    """
    
    @abstractmethod
    def get_service_status(self) -> dict:
        """Returns health/readiness status metrics of the service."""
        pass
