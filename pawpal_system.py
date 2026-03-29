from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str = ""
    health_notes: list[str] = field(default_factory=list)

    def get_info(self) -> str:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferred_start_time: str = "08:00"
    preferences: list[str] = field(default_factory=list)

    def get_profile(self) -> str:
        pass


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    category: str = ""
    reason: str = ""

    def is_high_priority(self) -> bool:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[CareTask] = []

    def add_task(self, task: CareTask) -> None:
        pass

    def build_schedule(self) -> list[CareTask]:
        pass

    def explain_plan(self) -> str:
        pass

    def get_summary(self) -> str:
        pass
