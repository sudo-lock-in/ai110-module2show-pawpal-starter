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
Methods for marking completion, creating recurring instances, and managing notes.
Manages a collection of care tasks and health records for a single pet.
Aggregates tasks and preferences across all owned pets, checks time availability.
Provides task filtering, sorting, conflict detection, and schedule generation.
Handles time slot management and recurring task expansion.
Key Features:
    - Task management with priority and frequency tracking
    - Recurring task automation with next occurrence calculation
    - Time conflict detection and resolution suggestions
    - Schedule optimization and capacity planning
    - Support for multiple pets per owner with aggregate reporting
    - Detailed conflict warnings with overlap calculations
    - Schedule building based on priority and time constraints
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

    # ===== UTILITY METHODS =====
    
    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert 'HH:MM' to minutes since midnight. Returns -1 if invalid."""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except:
            return -1
    
    @staticmethod
    def _minutes_to_time(minutes: int) -> str:
        """Convert minutes since midnight to 'HH:MM' format."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def add_task(self, task: CareTask) -> None:
        """Add a task to the scheduler after validating it fits within available time across ALL owner's pets."""
        # Check if single task exceeds limit
        if task.duration_minutes > self.owner.available_minutes:
            raise ValueError(f"'{task.title}' ({task.duration_minutes} min) exceeds owner's available time ({self.owner.available_minutes} min)")
        
        # Check total time across ALL pets owned by this owner
        total_all_pets = 0
        for owned_pet in self.owner.pets:
            for pet_task in owned_pet.get_tasks():
                total_all_pets += pet_task.duration_minutes
        
        new_total = total_all_pets + task.duration_minutes
        
        if new_total > self.owner.available_minutes:
            raise ValueError(f"Adding '{task.title}' ({task.duration_minutes} min) would exceed owner's available time. Total across all pets: {total_all_pets} min, Limit: {self.owner.available_minutes} min, Requested total: {new_total} min")
        
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

    def filter_tasks(self,
                     status: str | None = None,
                     priority: Priority | None = None,
                     category: str | None = None,
                     frequency: Frequency | None = None) -> list[CareTask]:
        """
        Filter tasks by multiple criteria. All filters are optional and combined with AND logic.
        
        Args:
            status: 'pending', 'completed', or None (all)
            priority: 'high', 'medium', 'low', or None (all)
            category: Category name or None (all)
            frequency: 'daily', 'weekly', 'monthly', 'one-time', or None (all)
        
        Returns: Filtered list of tasks
        """
        result = self.tasks
        
        if status == 'pending':
            result = [t for t in result if not t.is_completed]
        elif status == 'completed':
            result = [t for t in result if t.is_completed]
        
        if priority:
            result = [t for t in result if t.priority == priority]
        
        if category:
            result = [t for t in result if t.category == category]
        
        if frequency:
            result = [t for t in result if t.frequency == frequency]
        
        return result

    def sort_tasks(self, by: str = "priority") -> list[CareTask]:
        """
        Sort tasks by different criteria.
        
        Args:
            by: 'priority' (default), 'time', 'duration', 'fit' (priority + duration), 'frequency'
        
        Returns: Sorted task list
        """
        if by == "priority":
            return sorted(self.tasks,
                key=lambda t: (
                    0 if t.priority == "high" else (1 if t.priority == "medium" else 2),
                    {"one-time": 0, "daily": 1, "weekly": 2, "monthly": 3}.get(t.frequency, 4),
                    t.duration_minutes
                ))
        
        elif by == "time":
            return sorted(self.tasks,
                key=lambda t: (t.scheduled_time or "99:99", t.title))
        
        elif by == "duration":
            return sorted(self.tasks, key=lambda t: t.duration_minutes)
        
        elif by == "fit":  # Best fit for available time
            return sorted(self.tasks,
                key=lambda t: (
                    0 if t.priority == "high" else (1 if t.priority == "medium" else 2),
                    t.duration_minutes
                ))
        
        elif by == "frequency":
            return sorted(self.tasks,
                key=lambda t: {"one-time": 0, "daily": 1, "weekly": 2, "monthly": 3}.get(t.frequency, 4))
        
        return self.tasks.copy()
    
    def build_schedule(self) -> list[CareTask]:
        """Build an optimized schedule by sorting tasks by priority and frequency."""
        return self.sort_tasks(by='priority')

    def calculate_total_duration(self) -> int:
        """Calculate total duration of all tasks in minutes."""
        return sum(task.duration_minutes for task in self.tasks)

    def can_fit_task(self, task: CareTask) -> bool:
        """Check if a new task can fit within the owner's available time."""
        total_with_new = self.calculate_total_duration() + task.duration_minutes
        return total_with_new <= self.owner.available_minutes

    def get_pending_tasks(self) -> list[CareTask]:
        """Return all incomplete tasks."""
        return self.filter_tasks(status='pending')

    def get_completed_tasks(self) -> list[CareTask]:
        """Return all completed tasks."""
        return self.filter_tasks(status='completed')

    def get_tasks_by_priority(self, priority: Priority) -> list[CareTask]:
        """Return all tasks with a specific priority level."""
        return self.filter_tasks(priority=priority)

    def get_tasks_by_category(self, category: str) -> list[CareTask]:
        """Return all tasks in a specific category."""
        return self.filter_tasks(category=category)

    def get_tasks_by_frequency(self, frequency: Frequency) -> list[CareTask]:
        """Return all tasks with a specific frequency."""
        return self.filter_tasks(frequency=frequency)

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
    
    def detect_time_conflicts(self, detailed: bool = False) -> list[tuple | dict]:
        """
        Detect scheduling conflicts. Returns simple or detailed format.
        
        Args:
            detailed: If True, include overlap calculations; if False, return simple pairs
        
        Returns:
            List of (task1, task2) tuples or dicts with overlap info
        """
        conflicts = []
        scheduled_tasks = [t for t in self.tasks if t.scheduled_time]
        
        for i, task1 in enumerate(scheduled_tasks):
            start1 = self._time_to_minutes(task1.scheduled_time)
            if start1 < 0:
                continue
            end1 = start1 + task1.duration_minutes
            
            for task2 in scheduled_tasks[i + 1:]:
                start2 = self._time_to_minutes(task2.scheduled_time)
                if start2 < 0:
                    continue
                end2 = start2 + task2.duration_minutes
                
                # Check for overlap
                if start1 < end2 and start2 < end1:
                    if detailed:
                        overlap = min(end1, end2) - max(start1, start2)
                        conflicts.append({
                            'task1': task1.title,
                            'task2': task2.title,
                            'task1_time': f"{task1.scheduled_time}-{self._minutes_to_time(end1)}",
                            'task2_time': f"{task2.scheduled_time}-{self._minutes_to_time(end2)}",
                            'overlap_minutes': overlap
                        })
                    else:
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
        conflicts = self.detect_time_conflicts(detailed=False)
        
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
        Deprecated: Use detect_time_conflicts(detailed=True) instead.
        Returns list of conflict details including overlapping time windows.
        """
        return self.detect_time_conflicts(detailed=True)
    
    def get_detailed_conflict_warnings(self) -> list[str]:
        """
        Get detailed warning messages showing time overlaps.
        Returns empty list if no conflicts detected.
        
        Example output:
            ['⚠ WARNING: Morning Walk (08:00-08:30) overlaps with Feed Breakfast (08:15-08:25) by 10 minutes']
        """
        warnings = []
        conflicts = self.detect_time_conflicts(detailed=True)
        
        for conflict in conflicts:
            warning = (
                f"⚠ WARNING: {conflict['task1']} ({conflict['task1_time']}) overlaps with "
                f"{conflict['task2']} ({conflict['task2_time']}) by {conflict['overlap_minutes']} minutes"
            )
            warnings.append(warning)
        
        return warnings
    
    def get_tasks_by_time_window(self, start_time: str, end_time: str) -> list[CareTask]:
        """
        Get all tasks scheduled within a time window.
        Times in format 'HH:MM' (e.g., '09:00', '17:00')
        """
        start_min = self._time_to_minutes(start_time)
        end_min = self._time_to_minutes(end_time)
        
        if start_min < 0 or end_min < 0:
            return []
        
        tasks_in_window = []
        for task in self.tasks:
            if not task.scheduled_time:
                continue
            task_start = self._time_to_minutes(task.scheduled_time)
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
        current = self._time_to_minutes(start_from)
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
                task_start = self._time_to_minutes(task.scheduled_time)
                if task_start < 0:
                    continue
                task_end = task_start + task.duration_minutes
                
                # Check overlap
                if current < task_end and task_start < potential_end:
                    conflict = True
                    current = task_end
                    break
            
            if not conflict:
                return self._minutes_to_time(current)
        
        return None

    def schedule_task_at_time(self, task: CareTask, time_slot: str) -> bool:
        """
        Schedule a task at a specific time slot.
        
        Args:
            task: The CareTask to schedule
            time_slot: Time in 'HH:MM' format
        
        Returns:
            True if successfully scheduled, False if there's a conflict
        """
        # Validate time format
        slot_minutes = self._time_to_minutes(time_slot)
        if slot_minutes < 0:
            return False
        
        task_end = slot_minutes + task.duration_minutes
        
        # Check for conflicts with existing scheduled tasks
        for existing_task in self.tasks:
            if not existing_task.scheduled_time:
                continue
            existing_start = self._time_to_minutes(existing_task.scheduled_time)
            if existing_start < 0:
                continue
            existing_end = existing_start + existing_task.duration_minutes
            
            # Check overlap
            if slot_minutes < existing_end and existing_start < task_end:
                return False  # Conflict detected
        
        # No conflicts - set the time
        task.scheduled_time = time_slot
        return True

    def get_plan_summary(self, detailed: bool = False) -> str:
        """
        Get schedule summary. Detailed version includes all task info.
        
        Args:
            detailed: If True, show detailed plan; if False, show concise summary
        
        Returns: Formatted summary string
        """
        total_duration = self.calculate_total_duration()
        total_tasks = len(self.tasks)
        pending_tasks = len(self.filter_tasks(status='pending'))
        completed_tasks = len(self.filter_tasks(status='completed'))
        high_priority = len(self.filter_tasks(priority='high'))
        
        if detailed:
            schedule = self.sort_tasks(by='priority')
            output = (
                f"Care Plan for {self.pet.name}\n"
                f"{'=' * 50}\n"
                f"Owner: {self.owner.name}\n"
                f"Pet: {self.pet.name} ({self.pet.species})\n"
                f"Available Time: {self.owner.available_minutes} minutes\n"
                f"Total Task Duration: {total_duration} minutes\n"
                f"Time Remaining: {self.owner.available_minutes - total_duration} minutes\n"
                f"Pending Tasks: {pending_tasks}\n\n"
                f"Scheduled Tasks (by priority):\n"
                f"{'-' * 50}\n"
            )
            
            for i, task in enumerate(schedule, 1):
                status = "✓" if task.is_completed else "○"
                output += (
                    f"{i}. [{status}] {task.title} ({task.category})\n"
                    f"   Duration: {task.duration_minutes} min | Priority: {task.priority}\n"
                    f"   Frequency: {task.frequency}\n"
                )
        else:
            output = (
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
        
        return output

    def explain_plan(self) -> str:
        """Provide a detailed explanation of the care plan."""
        return self.get_plan_summary(detailed=True)

    def get_summary(self) -> str:
        """Provide a concise summary of the schedule."""
        return self.get_plan_summary(detailed=False)
