from dataclasses import dataclass, field
"""
PawPal System - Pet Care Management Module
This module provides a comprehensive system for managing pet care tasks and schedules.
It includes dataclasses for representing care tasks, pets, and pet owners, along with
a Scheduler class for organizing and optimizing pet care schedules based on priority,
frequency, and available time.
Classes:
    CareTask: Represents a single pet care task with priority, frequency, and tracking.
    Pet: Represents a pet with care tasks, health notes, and basic information.
    Owner: Represents a pet owner with available time and multiple pets.
    Scheduler: Manages and optimizes care task scheduling for a pet and owner.
Type Aliases:
    Priority: Literal type for task priority levels ("low", "medium", "high")
    Frequency: Literal type for task frequency ("one-time", "daily", "weekly", "monthly")
"""
from typing import Literal
from datetime import datetime

Priority = Literal["low", "medium", "high"]
Frequency = Literal["one-time", "daily", "weekly", "monthly"]


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: Priority
    frequency: Frequency = "one-time"
    category: str = ""
    is_completed: bool = False
    description: str = ""
    notes: list[str] = field(default_factory=list)

    def is_high_priority(self) -> bool:
        """Check if this task is high priority."""
        return self.priority == "high"

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False

    def get_task_info(self) -> str:
        """Return a detailed string representation of the task."""
        status = "✓ Completed" if self.is_completed else "○ Pending"
        return (
            f"{self.title} ({self.category})\n"
            f"  Duration: {self.duration_minutes} min | Priority: {self.priority} | Frequency: {self.frequency}\n"
            f"  Status: {status}\n"
            f"  Description: {self.description if self.description else 'N/A'}"
        )

    def add_note(self, note: str) -> None:
        """Add a note to this task."""
        self.notes.append(note)

    def get_notes(self) -> list[str]:
        """Return all notes for this task."""
        return self.notes.copy()


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str = ""
    health_notes: list[str] = field(default_factory=list)
    tasks: list[CareTask] = field(default_factory=list)
    weight: float = 0.0

    def get_info(self) -> str:
        """Return a detailed string representation of the pet."""
        health_info = "\n    ".join(self.health_notes) if self.health_notes else "No health notes"
        return (
            f"{self.name} - {self.species}\n"
            f"  Breed: {self.breed if self.breed else 'Unknown'}\n"
            f"  Age: {self.age} years | Weight: {self.weight} kg\n"
            f"  Health Notes:\n    {health_info}"
        )

    def add_task(self, task: CareTask) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: CareTask) -> None:
        """Remove a care task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[CareTask]:
        """Return all care tasks for this pet."""
        return self.tasks.copy()

    def get_pending_tasks(self) -> list[CareTask]:
        """Return all incomplete care tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed]

    def add_health_note(self, note: str) -> None:
        """Add a health note for this pet."""
        self.health_notes.append(note)

    def get_health_notes(self) -> list[str]:
        """Return all health notes for this pet."""
        return self.health_notes.copy()


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferred_start_time: str = "08:00"
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def get_profile(self) -> str:
        """Return a detailed string representation of the owner's profile."""
        pet_count = len(self.pets)
        pet_names = ", ".join([pet.name for pet in self.pets]) if self.pets else "No pets"
        return (
            f"{self.name}\n"
            f"  Available Time: {self.available_minutes} minutes\n"
            f"  Preferred Start Time: {self.preferred_start_time}\n"
            f"  Number of Pets: {pet_count}\n"
            f"  Pets: {pet_names}\n"
            f"  Preferences: {', '.join(self.preferences) if self.preferences else 'None specified'}"
        )

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets for this owner."""
        return self.pets.copy()

    def get_all_tasks(self) -> list[CareTask]:
        """Return all care tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_pending_tasks(self) -> list[CareTask]:
        """Return all incomplete care tasks from all pets."""
        pending_tasks = []
        for pet in self.pets:
            pending_tasks.extend(pet.get_pending_tasks())
        return pending_tasks

    def get_high_priority_tasks(self) -> list[CareTask]:
        """Return all high-priority tasks from all pets."""
        return [task for task in self.get_all_tasks() if task.is_high_priority()]

    def add_preference(self, preference: str) -> None:
        """Add a preference for this owner."""
        self.preferences.append(preference)

    def get_preferences(self) -> list[str]:
        """Return all preferences for this owner."""
        return self.preferences.copy()

    def find_pet_by_name(self, name: str) -> Pet | None:
        """Find a pet by name, returns None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[CareTask] = []

    def add_task(self, task: CareTask) -> None:
        """Add a task to the scheduler after validating it fits within available time."""
        if task.duration_minutes > self.owner.available_minutes:
            raise ValueError(f"'{task.title}' ({task.duration_minutes} min) exceeds owner's available time ({self.owner.available_minutes} min)")
        self.tasks.append(task)
        self.pet.add_task(task)

    def remove_task(self, task: CareTask) -> None:
        """Remove a task from the scheduler."""
        if task in self.tasks:
            self.tasks.remove(task)
        self.pet.remove_task(task)

    def get_tasks(self) -> list[CareTask]:
        """Return all tasks in the scheduler."""
        return self.tasks.copy()

    def build_schedule(self) -> list[CareTask]:
        """Build an optimized schedule by sorting tasks by priority and frequency."""
        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: (
                0 if task.priority == "high" else (1 if task.priority == "medium" else 2),
                {"one-time": 0, "daily": 1, "weekly": 2, "monthly": 3}.get(task.frequency, 4),
                task.duration_minutes
            )
        )
        return sorted_tasks

    def calculate_total_duration(self) -> int:
        """Calculate total duration of all tasks in minutes."""
        return sum(task.duration_minutes for task in self.tasks)

    def can_fit_task(self, task: CareTask) -> bool:
        """Check if a new task can fit within the owner's available time."""
        total_with_new = self.calculate_total_duration() + task.duration_minutes
        return total_with_new <= self.owner.available_minutes

    def get_pending_tasks(self) -> list[CareTask]:
        """Return all incomplete tasks."""
        return [task for task in self.tasks if not task.is_completed]

    def get_completed_tasks(self) -> list[CareTask]:
        """Return all completed tasks."""
        return [task for task in self.tasks if task.is_completed]

    def get_tasks_by_priority(self, priority: Priority) -> list[CareTask]:
        """Return all tasks with a specific priority level."""
        return [task for task in self.tasks if task.priority == priority]

    def get_tasks_by_category(self, category: str) -> list[CareTask]:
        """Return all tasks in a specific category."""
        return [task for task in self.tasks if task.category == category]

    def get_tasks_by_frequency(self, frequency: Frequency) -> list[CareTask]:
        """Return all tasks with a specific frequency."""
        return [task for task in self.tasks if task.frequency == frequency]

    def mark_task_completed(self, task: CareTask) -> None:
        """Mark a task as completed."""
        if task in self.tasks:
            task.mark_completed()

    def mark_task_incomplete(self, task: CareTask) -> None:
        """Mark a task as incomplete."""
        if task in self.tasks:
            task.mark_incomplete()

    def explain_plan(self) -> str:
        """Provide a detailed explanation of the care plan."""
        schedule = self.build_schedule()
        total_duration = self.calculate_total_duration()
        pending_count = len(self.get_pending_tasks())
        
        explanation = (
            f"Care Plan for {self.pet.name}\n"
            f"{'=' * 50}\n"
            f"Owner: {self.owner.name}\n"
            f"Pet: {self.pet.name} ({self.pet.species})\n"
            f"Available Time: {self.owner.available_minutes} minutes\n"
            f"Total Task Duration: {total_duration} minutes\n"
            f"Time Remaining: {self.owner.available_minutes - total_duration} minutes\n"
            f"Pending Tasks: {pending_count}\n\n"
            f"Scheduled Tasks (by priority):\n"
            f"{'-' * 50}\n"
        )
        
        for i, task in enumerate(schedule, 1):
            status = "✓" if task.is_completed else "○"
            explanation += (
                f"{i}. [{status}] {task.title} ({task.category})\n"
                f"   Duration: {task.duration_minutes} min | Priority: {task.priority}\n"
                f"   Frequency: {task.frequency}\n"
            )
        
        return explanation

    def get_summary(self) -> str:
        """Provide a concise summary of the schedule."""
        total_duration = self.calculate_total_duration()
        total_tasks = len(self.tasks)
        pending_tasks = len(self.get_pending_tasks())
        completed_tasks = len(self.get_completed_tasks())
        high_priority = len(self.get_tasks_by_priority("high"))
        
        summary = (
            f"SCHEDULE SUMMARY\n"
            f"{'=' * 40}\n"
            f"Pet: {self.pet.name}\n"
            f"Owner: {self.owner.name}\n"
            f"Total Tasks: {total_tasks}\n"
            f"  - Pending: {pending_tasks}\n"
            f"  - Completed: {completed_tasks}\n"
            f"  - High Priority: {high_priority}\n"
            f"Total Duration: {total_duration}/{self.owner.available_minutes} minutes\n"
            f"Status: {'✓ All tasks fit!' if total_duration <= self.owner.available_minutes else '✗ Exceeds available time'}"
        )
        
        return summary
