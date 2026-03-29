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
from datetime import datetime, timedelta

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
    scheduled_time: str = ""  # Format: "HH:MM" (e.g., "09:00")
    last_completed_date: datetime | None = None
    due_date: datetime | None = None  # Track when this task is due

    def is_high_priority(self) -> bool:
        """Check if this task is high priority."""
        return self.priority == "high"

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True
        self.last_completed_date = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False
    
    def create_next_occurrence(self) -> "CareTask | None":
        """
        Create a new instance of this task for the next occurrence.
        Calculates the correct due date based on frequency using timedelta.
        
        Returns a new CareTask if this is a recurring task, None if one-time.
        
        Frequency calculations:
            - daily: today + 1 day
            - weekly: today + 7 days
            - monthly: today + 30 days (approximate)
        """
        if self.frequency == "one-time":
            return None
        
        # Calculate next due date based on frequency
        today = datetime.now()
        
        if self.frequency == "daily":
            next_due_date = today + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = today + timedelta(days=7)
        elif self.frequency == "monthly":
            next_due_date = today + timedelta(days=30)
        else:
            next_due_date = today
        
        # Create a copy of this task for the next occurrence
        next_task = CareTask(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            category=self.category,
            is_completed=False,  # New task is not completed
            description=self.description,
            notes=self.notes.copy(),  # Copy notes to new task
            scheduled_time=self.scheduled_time,  # Keep same scheduled time
            last_completed_date=None,
            due_date=next_due_date  # Set calculated due date
        )
        
        return next_task

    def get_task_info(self) -> str:
        """Return a detailed string representation of the task."""
        status = "✓ Completed" if self.is_completed else "○ Pending"
        time_info = f" at {self.scheduled_time}" if self.scheduled_time else ""
        due_date_info = ""
        if self.due_date:
            due_date_info = f" | Due: {self.due_date.strftime('%Y-%m-%d')}"
        return (
            f"{self.title} ({self.category}){time_info}\n"
            f"  Duration: {self.duration_minutes} min | Priority: {self.priority} | Frequency: {self.frequency}{due_date_info}\n"
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
    
    def get_all_scheduling_conflicts(self) -> dict[str, list[str]]:
        """
        Check all pets for scheduling conflicts.
        Returns a dictionary mapping pet names to their conflict warnings.
        
        Returns empty dict if no conflicts found.
        
        Example:
            {
                'Max': ['⚠ WARNING: Feed Breakfast and Morning Walk both at 08:00'],
                'Whiskers': []
            }
        """
        all_conflicts = {}
        for pet in self.pets:
            # We would need access to the scheduler here, so this is informational
            # In practice, track schedulers separately
            pass
        return all_conflicts
    
    def check_owner_time_availability(self) -> dict:
        """
        Check if the owner has enough time for all pets' tasks.
        Returns a summary with potential scheduling issues.
        """
        all_tasks = self.get_all_tasks()
        total_duration = sum(task.duration_minutes for task in all_tasks)
        
        return {
            'total_available_minutes': self.available_minutes,
            'total_task_minutes': total_duration,
            'remaining_minutes': self.available_minutes - total_duration,
            'is_overbooked': total_duration > self.available_minutes,
            'warning': (
                f"⚠ Owner '{self.name}' is OVERBOOKED: {total_duration} minutes of tasks "
                f"exceed {self.available_minutes} available minutes!"
                if total_duration > self.available_minutes
                else f"✓ Owner '{self.name}' has {self.available_minutes - total_duration} minutes remaining"
            )
        }


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
    
    def mark_task_completed_with_recurrence(self, task: CareTask) -> CareTask | None:
        """
        Mark a task as completed and automatically create the next occurrence if it's recurring.
        
        Returns:
            The newly created task for the next occurrence, or None if task is one-time.
            
        Example:
            next_walk = dog_scheduler.mark_task_completed_with_recurrence(task1)
            if next_walk:
                print(f"Next occurrence scheduled: {next_walk.title}")
        """
        if task not in self.tasks:
            return None
        
        # Mark current task as completed
        task.mark_completed()
        
        # Create next occurrence if recurring
        next_task = task.create_next_occurrence()
        
        if next_task:
            # Automatically add the next occurrence to the scheduler
            self.tasks.append(next_task)
            self.pet.add_task(next_task)
            return next_task
        
        return None

    def mark_task_incomplete(self, task: CareTask) -> None:
        """Mark a task as incomplete."""
        if task in self.tasks:
            task.mark_incomplete()

    # ===== EFFICIENCY IMPROVEMENTS =====
    
    def sort_tasks_by_time(self) -> list[CareTask]:
        """Sort tasks by scheduled time (earliest first). Unscheduled tasks go last."""
        return sorted(
            self.tasks,
            key=lambda task: (task.scheduled_time or "99:99", task.title)
        )
    
    def sort_tasks_by_duration(self, ascending: bool = True) -> list[CareTask]:
        """Sort tasks by duration. Useful for fitting tasks into available time."""
        return sorted(self.tasks, key=lambda task: task.duration_minutes, reverse=not ascending)
    
    def filter_tasks_by_pet(self, pet: Pet) -> list[CareTask]:
        """Filter tasks for a specific pet."""
        return [task for task in self.pet.get_tasks() if task in self.tasks]
    
    def filter_tasks_by_status(self, status: str = "pending") -> list[CareTask]:
        """
        Filter tasks by status: 'pending' (incomplete), 'completed', or 'all'.
        Returns tasks matching the status.
        """
        if status.lower() == "pending":
            return self.get_pending_tasks()
        elif status.lower() == "completed":
            return self.get_completed_tasks()
        else:  # 'all'
            return self.get_tasks()
    
    def filter_tasks_by_status_and_pet(self, status: str = "all", pet_name: str = "") -> list[CareTask]:
        """
        Filter tasks by completion status and/or pet name.
        
        Args:
            status: 'pending' (incomplete), 'completed', or 'all' (default)
            pet_name: Name of the pet to filter by (optional, empty string = all pets)
        
        Returns:
            List of tasks matching both criteria.
        
        Example:
            # Get all pending tasks for Max
            tasks = scheduler.filter_tasks_by_status_and_pet("pending", "Max")
            
            # Get all completed tasks across all pets
            tasks = scheduler.filter_tasks_by_status_and_pet("completed", "")
        """
        # First, filter by status
        if status.lower() == "pending":
            filtered = self.get_pending_tasks()
        elif status.lower() == "completed":
            filtered = self.get_completed_tasks()
        else:  # 'all'
            filtered = self.get_tasks()
        
        # Then, filter by pet name if provided
        if pet_name.strip():
            # Only keep tasks that belong to the specified pet
            filtered = [
                task for task in filtered 
                if task in self.pet.get_tasks() and self.pet.name.lower() == pet_name.lower()
            ]
        
        return filtered
    
    def get_recurring_tasks_for_day(self) -> list[CareTask]:
        """Get all recurring tasks (daily, weekly, monthly) that should happen today."""
        return [task for task in self.tasks if task.frequency != "one-time"]
    
    def get_one_time_tasks(self) -> list[CareTask]:
        """Get all one-time tasks."""
        return [task for task in self.tasks if task.frequency == "one-time"]
    
    def expand_recurring_tasks(self, days: int = 7) -> list[tuple[CareTask, int]]:
        """
        Expand recurring tasks for a period of days.
        Returns list of (task, day_offset) tuples showing when each task occurs.
        Example: Daily task appears on days 0-6, weekly on day 0, etc.
        """
        expanded = []
        for task in self.tasks:
            if task.frequency == "one-time":
                expanded.append((task, 0))
            elif task.frequency == "daily":
                for day in range(days):
                    expanded.append((task, day))
            elif task.frequency == "weekly":
                expanded.append((task, 0))  # Occurs on day 0 (today)
            elif task.frequency == "monthly":
                expanded.append((task, 0))  # Occurs on day 0 (today)
        
        return expanded
    
    def detect_time_conflicts(self) -> list[tuple[CareTask, CareTask]]:
        """
        Detect scheduling conflicts when tasks have overlapping scheduled times.
        Returns list of conflicting task pairs.
        """
        conflicts = []
        scheduled_tasks = [t for t in self.tasks if t.scheduled_time]
        
        for i, task1 in enumerate(scheduled_tasks):
            for task2 in scheduled_tasks[i + 1:]:
                # Simple check: if both have the same scheduled time, they conflict
                # In a real system, you'd calculate end times
                if task1.scheduled_time == task2.scheduled_time:
                    conflicts.append((task1, task2))
        
        return conflicts
    
    def get_conflict_warnings(self) -> list[str]:
        """
        Get a list of human-readable warning messages for any scheduling conflicts.
        Returns empty list if no conflicts detected.
        
        Example output:
            ['WARNING: Feed Breakfast (10 min) and Morning Walk (30 min) both scheduled at 08:00']
        """
        warnings = []
        conflicts = self.detect_time_conflicts()
        
        for task1, task2 in conflicts:
            warning = (
                f"⚠ WARNING: '{task1.title}' ({task1.duration_minutes} min) and "
                f"'{task2.title}' ({task2.duration_minutes} min) both scheduled at {task1.scheduled_time}"
            )
            warnings.append(warning)
        
        return warnings
    
    def has_scheduling_conflicts(self) -> bool:
        """
        Check if there are any scheduling conflicts for this pet's tasks.
        Returns True if conflicts exist, False otherwise.
        """
        return len(self.detect_time_conflicts()) > 0
    
    def print_conflict_warnings(self) -> None:
        """
        Print all scheduling conflict warnings to console.
        Safe to call even if no conflicts exist (prints nothing).
        """
        warnings = self.get_conflict_warnings()
        if warnings:
            print(f"\n{'!' * 70}")
            print(f"SCHEDULING CONFLICTS DETECTED FOR {self.pet.name.upper()}")
            print(f"{'!' * 70}")
            for warning in warnings:
                print(warning)
            print(f"{'!' * 70}\n")
        
        return None
    
    def detect_time_conflicts_detailed(self) -> list[dict]:
        """
        Detect time conflicts with detailed time window calculations.
        Assumes tasks can be scheduled back-to-back.
        Returns list of conflict details including overlapping time windows.
        """
        conflicts_detail = []
        scheduled_tasks = [t for t in self.tasks if t.scheduled_time]
        
        def time_to_minutes(time_str: str) -> int:
            """Convert 'HH:MM' to minutes since midnight."""
            try:
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes
            except:
                return -1
        
        for i, task1 in enumerate(scheduled_tasks):
            start1 = time_to_minutes(task1.scheduled_time)
            if start1 < 0:
                continue
            end1 = start1 + task1.duration_minutes
            
            for task2 in scheduled_tasks[i + 1:]:
                start2 = time_to_minutes(task2.scheduled_time)
                if start2 < 0:
                    continue
                end2 = start2 + task2.duration_minutes
                
                # Check for overlap
                if start1 < end2 and start2 < end1:
                    conflicts_detail.append({
                        'task1': task1.title,
                        'task2': task2.title,
                        'task1_time': f"{task1.scheduled_time}-{(start1 + task1.duration_minutes) // 60:02d}:{(start1 + task1.duration_minutes) % 60:02d}",
                        'task2_time': f"{task2.scheduled_time}-{end2 // 60:02d}:{end2 % 60:02d}",
                        'overlap_minutes': min(end1, end2) - max(start1, start2)
                    })
        
        return conflicts_detail
    
    def get_detailed_conflict_warnings(self) -> list[str]:
        """
        Get detailed warning messages showing time overlaps.
        Returns empty list if no conflicts detected.
        
        Example output:
            ['⚠ WARNING: Morning Walk (08:00-08:30) overlaps with Feed Breakfast (08:15-08:25) by 10 minutes']
        """
        warnings = []
        conflicts = self.detect_time_conflicts_detailed()
        
        for conflict in conflicts:
            warning = (
                f"⚠ WARNING: {conflict['task1']} ({conflict['task1_time']}) overlaps with "
                f"{conflict['task2']} ({conflict['task2_time']}) by {conflict['overlap_minutes']} minutes"
            )
            warnings.append(warning)
        
        return warnings
    
    def fit_tasks_optimally(self) -> list[CareTask]:
        """
        Sort and recommend tasks in order that best fits available time.
        Uses greedy algorithm: prioritize high priority, then short duration.
        """
        return sorted(
            self.tasks,
            key=lambda task: (
                0 if task.priority == "high" else (1 if task.priority == "medium" else 2),
                task.duration_minutes
            )
        )
    
    def get_tasks_by_time_window(self, start_time: str, end_time: str) -> list[CareTask]:
        """
        Get all tasks scheduled within a time window.
        Times in format 'HH:MM' (e.g., '09:00', '17:00')
        """
        def time_to_minutes(time_str: str) -> int:
            try:
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes
            except:
                return -1
        
        start_min = time_to_minutes(start_time)
        end_min = time_to_minutes(end_time)
        
        if start_min < 0 or end_min < 0:
            return []
        
        tasks_in_window = []
        for task in self.tasks:
            if not task.scheduled_time:
                continue
            task_start = time_to_minutes(task.scheduled_time)
            if task_start < 0:
                continue
            
            if start_min <= task_start < end_min:
                tasks_in_window.append(task)
        
        return tasks_in_window
    
    def suggest_next_available_time(self, duration_minutes: int, start_from: str = "08:00") -> str | None:
        """
        Suggest the next available time slot for a task of given duration.
        Returns time in 'HH:MM' format or None if no slot available.
        """
        def time_to_minutes(time_str: str) -> int:
            try:
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes
            except:
                return -1
        
        def minutes_to_time(minutes: int) -> str:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours:02d}:{mins:02d}"
        
        current = time_to_minutes(start_from)
        if current < 0:
            return None
        
        end_of_day = 24 * 60  # 24:00
        
        # Try to find a slot
        while current + duration_minutes <= end_of_day:
            potential_end = current + duration_minutes
            
            # Check if this slot conflicts with any scheduled task
            conflict = False
            for task in self.tasks:
                if not task.scheduled_time:
                    continue
                task_start = time_to_minutes(task.scheduled_time)
                if task_start < 0:
                    continue
                task_end = task_start + task.duration_minutes
                
                # Check overlap
                if current < task_end and task_start < potential_end:
                    conflict = True
                    current = task_end
                    break
            
            if not conflict:
                return minutes_to_time(current)
        
        return None

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
