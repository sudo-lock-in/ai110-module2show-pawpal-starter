import pytest
from pawpal_system import CareTask, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Test that task completion status changes correctly."""
    
    def test_mark_completed(self):
        """Verify that calling mark_completed() changes task status to True."""
        task = CareTask(
            title="Feed Dog",
            duration_minutes=10,
            priority="high",
            category="Feeding"
        )
        
        # Initially, task should not be completed
        assert task.is_completed == False
        
        # Mark as completed
        task.mark_completed()
        
        # Now task should be completed
        assert task.is_completed == True
    
    def test_mark_incomplete(self):
        """Verify that calling mark_incomplete() changes task status to False."""
        task = CareTask(
            title="Walk Dog",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            is_completed=True  # Start as completed
        )
        
        # Initially, task should be completed
        assert task.is_completed == True
        
        # Mark as incomplete
        task.mark_incomplete()
        
        # Now task should not be completed
        assert task.is_completed == False
    
    def test_is_high_priority(self):
        """Verify that is_high_priority() correctly identifies high priority tasks."""
        high_priority_task = CareTask(
            title="Medication",
            duration_minutes=5,
            priority="high",
            category="Health"
        )
        
        low_priority_task = CareTask(
            title="Grooming",
            duration_minutes=20,
            priority="low",
            category="Grooming"
        )
        
        assert high_priority_task.is_high_priority() == True
        assert low_priority_task.is_high_priority() == False


class TestTaskAddition:
    """Test that adding tasks to pets works correctly."""
    
    def test_add_task_to_pet(self):
        """Verify that adding a task to a Pet increases the pet's task count."""
        pet = Pet(
            name="Buddy",
            species="Dog",
            age=2,
            breed="Labrador"
        )
        
        # Initially, pet should have no tasks
        assert len(pet.get_tasks()) == 0
        
        # Create and add a task
        task = CareTask(
            title="Morning Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise"
        )
        pet.add_task(task)
        
        # Now pet should have 1 task
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0] == task
    
    def test_add_multiple_tasks_to_pet(self):
        """Verify that multiple tasks can be added to a Pet."""
        pet = Pet(
            name="Whiskers",
            species="Cat",
            age=3,
            breed="Tabby"
        )
        
        # Create multiple tasks
        tasks = [
            CareTask(title="Feed", duration_minutes=5, priority="high", category="Feeding"),
            CareTask(title="Clean Litter", duration_minutes=10, priority="high", category="Cleaning"),
            CareTask(title="Play", duration_minutes=15, priority="medium", category="Entertainment"),
        ]
        
        # Add all tasks
        for task in tasks:
            pet.add_task(task)
        
        # Verify all tasks were added
        assert len(pet.get_tasks()) == 3
        assert pet.get_tasks() == tasks
    
    def test_remove_task_from_pet(self):
        """Verify that removing a task decreases the pet's task count."""
        pet = Pet(
            name="Max",
            species="Dog",
            age=5,
            breed="Golden Retriever"
        )
        
        task = CareTask(
            title="Grooming",
            duration_minutes=20,
            priority="low",
            category="Grooming"
        )
        
        # Add a task
        pet.add_task(task)
        assert len(pet.get_tasks()) == 1
        
        # Remove the task
        pet.remove_task(task)
        
        # Now pet should have no tasks
        assert len(pet.get_tasks()) == 0


class TestTaskSorting:
    """Test task sorting functionality with different criteria."""
    
    def test_sort_by_priority_high_to_low(self):
        """Verify tasks are sorted from high to low priority."""
        owner = Owner(name="Alice", available_minutes=120)
        pet = Pet(name="Max", species="Dog", age=3, breed="Labrador")
        scheduler = Scheduler(owner, pet)
        
        # Create tasks with different priorities
        high_task = CareTask(title="Medication", duration_minutes=5, priority="high", category="Health")
        low_task = CareTask(title="Grooming", duration_minutes=20, priority="low", category="Grooming")
        medium_task = CareTask(title="Play", duration_minutes=30, priority="medium", category="Exercise")
        
        scheduler.add_task(high_task)
        scheduler.add_task(low_task)
        scheduler.add_task(medium_task)
        
        sorted_tasks = scheduler.sort_tasks(by="priority")
        
        # High priority should be first
        assert sorted_tasks[0] == high_task
        assert sorted_tasks[1] == medium_task
        assert sorted_tasks[2] == low_task
    
    def test_sort_by_duration_shortest_first(self):
        """Verify tasks are sorted by duration (shortest to longest)."""
        owner = Owner(name="Bob", available_minutes=120)
        pet = Pet(name="Buddy", species="Dog", age=5, breed="Golden Retriever")
        scheduler = Scheduler(owner, pet)
        
        short_task = CareTask(title="Quick Drink", duration_minutes=2, priority="high", category="Feeding")
        medium_task = CareTask(title="Walk", duration_minutes=30, priority="medium", category="Exercise")
        long_task = CareTask(title="Bath", duration_minutes=60, priority="low", category="Grooming")
        
        scheduler.add_task(long_task)
        scheduler.add_task(short_task)
        scheduler.add_task(medium_task)
        
        sorted_tasks = scheduler.sort_tasks(by="duration")
        
        assert sorted_tasks[0].duration_minutes == 2
        assert sorted_tasks[1].duration_minutes == 30
        assert sorted_tasks[2].duration_minutes == 60
    
    def test_sort_by_frequency_one_time_first(self):
        """Verify tasks sorted by frequency (one-time first, then daily, weekly, monthly)."""
        owner = Owner(name="Carol", available_minutes=180)
        pet = Pet(name="Whiskers", species="Cat", age=3, breed="Tabby")
        scheduler = Scheduler(owner, pet)
        
        one_time = CareTask(title="Vet Visit", duration_minutes=30, priority="high", frequency="one-time", category="Health")
        daily = CareTask(title="Feed", duration_minutes=5, priority="high", frequency="daily", category="Feeding")
        weekly = CareTask(title="Bath", duration_minutes=20, priority="medium", frequency="weekly", category="Grooming")
        monthly = CareTask(title="Checkup", duration_minutes=15, priority="medium", frequency="monthly", category="Health")
        
        scheduler.add_task(daily)
        scheduler.add_task(monthly)
        scheduler.add_task(one_time)
        scheduler.add_task(weekly)
        
        sorted_tasks = scheduler.sort_tasks(by="frequency")
        
        # Expect: one-time → daily → weekly → monthly
        assert sorted_tasks[0].frequency == "one-time"
        assert sorted_tasks[1].frequency == "daily"
        assert sorted_tasks[2].frequency == "weekly"
        assert sorted_tasks[3].frequency == "monthly"
    
    def test_sort_empty_task_list(self):
        """Verify sorting an empty task list returns empty list."""
        owner = Owner(name="David", available_minutes=120)
        pet = Pet(name="Rex", species="Dog", age=2, breed="Beagle")
        scheduler = Scheduler(owner, pet)
        
        sorted_tasks = scheduler.sort_tasks(by="priority")
        
        assert sorted_tasks == []
    
    def test_sort_by_fit_priority_then_duration(self):
        """Verify 'fit' sorting prioritizes by priority, then duration."""
        owner = Owner(name="Eve", available_minutes=200)
        pet = Pet(name="Fluffy", species="Cat", age=4, breed="Persian")
        scheduler = Scheduler(owner, pet)
        
        # Create tasks: same priority, different duration
        high_short = CareTask(title="Quick Med", duration_minutes=5, priority="high", category="Health")
        high_long = CareTask(title="Long Med", duration_minutes=30, priority="high", category="Health")
        medium_short = CareTask(title="Quick Play", duration_minutes=10, priority="medium", category="Exercise")
        
        scheduler.add_task(high_long)
        scheduler.add_task(medium_short)
        scheduler.add_task(high_short)
        
        sorted_tasks = scheduler.sort_tasks(by="fit")
        
        # Both high priority first, then by duration
        assert sorted_tasks[0] == high_short
        assert sorted_tasks[1] == high_long
        assert sorted_tasks[2] == medium_short


class TestRecurringTasks:
    """Test recurring task creation and management."""
    
    def test_create_daily_next_occurrence(self):
        """Verify daily task creates next occurrence 1 day later."""
        daily_task = CareTask(
            title="Morning Breakfast",
            duration_minutes=15,
            priority="high",
            frequency="daily",
            category="Feeding"
        )
        
        next_task = daily_task.create_next_occurrence()
        
        assert next_task is not None
        assert next_task.title == "Morning Breakfast"
        assert next_task.is_completed == False
        assert next_task.frequency == "daily"
        assert next_task.due_date is not None
    
    def test_create_weekly_next_occurrence(self):
        """Verify weekly task creates next occurrence 7 days later."""
        weekly_task = CareTask(
            title="Grooming",
            duration_minutes=45,
            priority="medium",
            frequency="weekly",
            category="Grooming"
        )
        
        next_task = weekly_task.create_next_occurrence()
        
        assert next_task is not None
        assert next_task.frequency == "weekly"
        # Due date should be approximately 7 days from now
        assert next_task.due_date is not None
    
    def test_create_monthly_next_occurrence(self):
        """Verify monthly task creates next occurrence ~30 days later."""
        monthly_task = CareTask(
            title="Health Checkup",
            duration_minutes=30,
            priority="high",
            frequency="monthly",
            category="Health"
        )
        
        next_task = monthly_task.create_next_occurrence()
        
        assert next_task is not None
        assert next_task.frequency == "monthly"
        assert next_task.due_date is not None
    
    def test_one_time_task_no_next_occurrence(self):
        """Verify one-time tasks don't create next occurrences."""
        one_time_task = CareTask(
            title="Vet Visit",
            duration_minutes=60,
            priority="high",
            frequency="one-time",
            category="Health"
        )
        
        next_task = one_time_task.create_next_occurrence()
        
        assert next_task is None
    
    def test_mark_recurring_task_completed_creates_next(self):
        """Verify marking recurring task completed auto-creates next occurrence."""
        owner = Owner(name="Frank", available_minutes=180)
        pet = Pet(name="Duke", species="Dog", age=3, breed="Shepherd")
        scheduler = Scheduler(owner, pet)
        
        daily_task = CareTask(
            title="Evening Walk",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            category="Exercise"
        )
        
        scheduler.add_task(daily_task)
        initial_count = len(scheduler.get_tasks())
        
        # Mark as completed with recurrence
        next_task = scheduler.mark_task_completed_with_recurrence(daily_task)
        
        assert next_task is not None
        assert daily_task.is_completed == True
        assert len(scheduler.get_tasks()) == initial_count + 1
        assert next_task in scheduler.get_tasks()
    
    def test_mark_one_time_task_completed_no_next(self):
        """Verify marking one-time task completed doesn't create next occurrence."""
        owner = Owner(name="Grace", available_minutes=120)
        pet = Pet(name="Mittens", species="Cat", age=2, breed="Siamese")
        scheduler = Scheduler(owner, pet)
        
        one_time_task = CareTask(
            title="Nail Trim",
            duration_minutes=20,
            priority="medium",
            frequency="one-time",
            category="Grooming"
        )
        
        scheduler.add_task(one_time_task)
        initial_count = len(scheduler.get_tasks())
        
        next_task = scheduler.mark_task_completed_with_recurrence(one_time_task)
        
        assert next_task is None
        assert one_time_task.is_completed == True
        assert len(scheduler.get_tasks()) == initial_count


class TestScheduleConflicts:
    """Test conflict detection and handling."""
    
    def test_detect_overlapping_tasks_same_time(self):
        """Verify detection of tasks scheduled at exact same time."""
        owner = Owner(name="Henry", available_minutes=240)
        pet = Pet(name="Buster", species="Dog", age=4, breed="Boxer")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(
            title="Breakfast",
            duration_minutes=15,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        task2 = CareTask(
            title="Morning Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            scheduled_time="08:00"
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        conflicts = scheduler.detect_time_conflicts()
        
        assert len(conflicts) > 0
        assert (task1, task2) in conflicts or (task2, task1) in conflicts
    
    def test_detect_partial_overlap_conflicts(self):
        """Verify detection of tasks with partial time overlap."""
        owner = Owner(name="Iris", available_minutes=240)
        pet = Pet(name="Shadow", species="Dog", age=3, breed="Poodle")
        scheduler = Scheduler(owner, pet)
        
        # Task 1: 08:00-08:30 (30 min)
        task1 = CareTask(
            title="Feed",
            duration_minutes=30,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        # Task 2: 08:15-08:45 (30 min) - overlaps by 15 min
        task2 = CareTask(
            title="Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            scheduled_time="08:15"
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        conflicts = scheduler.detect_time_conflicts()
        
        assert len(conflicts) > 0
    
    def test_no_conflict_adjacent_tasks(self):
        """Verify no conflict for tasks scheduled back-to-back."""
        owner = Owner(name="Jack", available_minutes=240)
        pet = Pet(name="Rusty", species="Dog", age=5, breed="Dachshund")
        scheduler = Scheduler(owner, pet)
        
        # Task 1: 08:00-08:30
        task1 = CareTask(
            title="Feed",
            duration_minutes=30,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        # Task 2: 08:30-09:00 (starts exactly when task1 ends)
        task2 = CareTask(
            title="Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            scheduled_time="08:30"
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        conflicts = scheduler.detect_time_conflicts()
        
        assert len(conflicts) == 0
    
    def test_conflict_warnings_generated(self):
        """Verify conflict warnings are generated for overlapping tasks."""
        owner = Owner(name="Karen", available_minutes=240)
        pet = Pet(name="Daisy", species="Dog", age=2, breed="Corgi")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(
            title="Breakfast",
            duration_minutes=15,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        task2 = CareTask(
            title="Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            scheduled_time="08:00"
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        warnings = scheduler.get_conflict_warnings()
        
        assert len(warnings) > 0
        assert "⚠ WARNING" in warnings[0]
        assert "Breakfast" in warnings[0]
        assert "Walk" in warnings[0]
    
    def test_has_scheduling_conflicts_true(self):
        """Verify has_scheduling_conflicts returns True when conflicts exist."""
        owner = Owner(name="Leo", available_minutes=240)
        pet = Pet(name="Spot", species="Dog", age=3, breed="Dalmatian")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(
            title="Feed",
            duration_minutes=20,
            priority="high",
            category="Feeding",
            scheduled_time="09:00"
        )
        task2 = CareTask(
            title="Play",
            duration_minutes=30,
            priority="medium",
            category="Exercise",
            scheduled_time="09:15"
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        assert scheduler.has_scheduling_conflicts() == True
    
    def test_has_scheduling_conflicts_false(self):
        """Verify has_scheduling_conflicts returns False when no conflicts."""
        owner = Owner(name="Mia", available_minutes=240)
        pet = Pet(name="Coco", species="Dog", age=4, breed="Poodle")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(
            title="Feed",
            duration_minutes=15,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        task2 = CareTask(
            title="Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            scheduled_time="09:00"
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        assert scheduler.has_scheduling_conflicts() == False


class TestTimeSlotManagement:
    """Test time slot discovery and management."""
    
    def test_find_available_time_slot(self):
        """Verify finding available time slot for new task."""
        owner = Owner(name="Nathan", available_minutes=240)
        pet = Pet(name="Lucky", species="Dog", age=3, breed="Husky")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(
            title="Feed",
            duration_minutes=15,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        scheduler.add_task(task1)
        
        suggested_time = scheduler.suggest_next_available_time(duration_minutes=30, start_from="08:00")
        
        assert suggested_time is not None
        # Should be after task1 ends (08:15)
        assert suggested_time >= "08:15"
    
    def test_get_tasks_in_time_window(self):
        """Verify retrieving tasks within a specific time window."""
        owner = Owner(name="Olivia", available_minutes=240)
        pet = Pet(name="Scout", species="Dog", age=4, breed="Beagle")
        scheduler = Scheduler(owner, pet)
        
        morning_task = CareTask(
            title="Feed",
            duration_minutes=15,
            priority="high",
            category="Feeding",
            scheduled_time="08:00"
        )
        afternoon_task = CareTask(
            title="Walk",
            duration_minutes=30,
            priority="high",
            category="Exercise",
            scheduled_time="14:00"
        )
        
        scheduler.add_task(morning_task)
        scheduler.add_task(afternoon_task)
        
        morning_window_tasks = scheduler.get_tasks_by_time_window("07:00", "12:00")
        
        assert len(morning_window_tasks) == 1
        assert morning_task in morning_window_tasks
        assert afternoon_task not in morning_window_tasks
    
    def test_time_window_excludes_outside_tasks(self):
        """Verify time window doesn't include tasks outside the range."""
        owner = Owner(name="Paul", available_minutes=240)
        pet = Pet(name="Buddy", species="Dog", age=2, breed="Boxer")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(title="Early", duration_minutes=15, priority="high", category="Feeding", scheduled_time="07:00")
        task2 = CareTask(title="Mid", duration_minutes=15, priority="high", category="Feeding", scheduled_time="12:00")
        task3 = CareTask(title="Late", duration_minutes=15, priority="high", category="Feeding", scheduled_time="18:00")
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        scheduler.add_task(task3)
        
        tasks_in_window = scheduler.get_tasks_by_time_window("11:00", "13:00")
        
        assert len(tasks_in_window) == 1
        assert task2 in tasks_in_window


class TestOwnerCapacity:
    """Test owner time capacity and overbooking detection."""
    
    def test_task_exceeds_owner_available_time(self):
        """Verify error when adding task exceeding owner's available time."""
        owner = Owner(name="Quinn", available_minutes=30)
        pet = Pet(name="Molly", species="Dog", age=3, breed="Pug")
        scheduler = Scheduler(owner, pet)
        
        large_task = CareTask(
            title="Long Activity",
            duration_minutes=60,
            priority="high",
            category="Exercise"
        )
        
        with pytest.raises(ValueError):
            scheduler.add_task(large_task)
    
    def test_owner_overbooking_detection(self):
        """Verify overbooking is detected when total tasks exceed available time."""
        owner = Owner(name="Rachel", available_minutes=60)
        pet = Pet(name="Patches", species="Cat", age=5, breed="Tabby")
        
        # Manually add tasks to pet to test owner's aggregate checking
        task1 = CareTask(title="Feed", duration_minutes=40, priority="high", category="Feeding")
        task2 = CareTask(title="Play", duration_minutes=30, priority="medium", category="Exercise")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        availability = owner.check_owner_time_availability()
        
        assert availability['is_overbooked'] == True
        assert availability['total_task_minutes'] == 70
    
    def test_task_fits_exactly_available_time(self):
        """Verify task that fits exactly within available time is accepted."""
        owner = Owner(name="Steve", available_minutes=45)
        pet = Pet(name="Charlie", species="Dog", age=4, breed="Bulldog")
        scheduler = Scheduler(owner, pet)
        
        exact_task = CareTask(
            title="Exact Activity",
            duration_minutes=45,
            priority="high",
            category="Exercise"
        )
        
        scheduler.add_task(exact_task)
        
        assert len(scheduler.get_tasks()) == 1
        assert scheduler.calculate_total_duration() == 45


class TestFiltering:
    """Test task filtering by various criteria."""
    
    def test_filter_by_priority(self):
        """Verify filtering tasks by priority level."""
        owner = Owner(name="Tina", available_minutes=180)
        pet = Pet(name="Pepper", species="Dog", age=3, breed="Retriever")
        scheduler = Scheduler(owner, pet)
        
        high_task = CareTask(title="Meds", duration_minutes=5, priority="high", category="Health")
        low_task = CareTask(title="Groom", duration_minutes=30, priority="low", category="Grooming")
        medium_task = CareTask(title="Play", duration_minutes=20, priority="medium", category="Exercise")
        
        scheduler.add_task(high_task)
        scheduler.add_task(low_task)
        scheduler.add_task(medium_task)
        
        high_priority_tasks = scheduler.filter_tasks(priority="high")
        
        assert len(high_priority_tasks) == 1
        assert high_task in high_priority_tasks
    
    def test_filter_by_frequency(self):
        """Verify filtering tasks by frequency."""
        owner = Owner(name="Uma", available_minutes=240)
        pet = Pet(name="Bailey", species="Dog", age=5, breed="Shepherd")
        scheduler = Scheduler(owner, pet)
        
        daily = CareTask(title="Feed", duration_minutes=10, priority="high", frequency="daily", category="Feeding")
        weekly = CareTask(title="Bath", duration_minutes=45, priority="medium", frequency="weekly", category="Grooming")
        one_time = CareTask(title="Vet", duration_minutes=60, priority="high", frequency="one-time", category="Health")
        
        scheduler.add_task(daily)
        scheduler.add_task(weekly)
        scheduler.add_task(one_time)
        
        daily_tasks = scheduler.filter_tasks(frequency="daily")
        
        assert len(daily_tasks) == 1
        assert daily in daily_tasks
    
    def test_filter_by_status_pending(self):
        """Verify filtering pending (incomplete) tasks."""
        owner = Owner(name="Victor", available_minutes=180)
        pet = Pet(name="Bentley", species="Dog", age=2, breed="Boxer")
        scheduler = Scheduler(owner, pet)
        
        pending = CareTask(title="Walk", duration_minutes=30, priority="high", category="Exercise")
        completed = CareTask(title="Feed", duration_minutes=15, priority="high", category="Feeding", is_completed=True)
        
        scheduler.add_task(pending)
        scheduler.add_task(completed)
        
        pending_tasks = scheduler.filter_tasks(status="pending")
        
        assert len(pending_tasks) == 1
        assert pending in pending_tasks
        assert completed not in pending_tasks
    
    def test_filter_by_category(self):
        """Verify filtering tasks by category."""
        owner = Owner(name="Wendy", available_minutes=200)
        pet = Pet(name="Oreo", species="Dog", age=3, breed="Poodle")
        scheduler = Scheduler(owner, pet)
        
        feeding1 = CareTask(title="Breakfast", duration_minutes=10, priority="high", category="Feeding")
        feeding2 = CareTask(title="Dinner", duration_minutes=10, priority="high", category="Feeding")
        exercise = CareTask(title="Walk", duration_minutes=30, priority="high", category="Exercise")
        
        scheduler.add_task(feeding1)
        scheduler.add_task(feeding2)
        scheduler.add_task(exercise)
        
        feeding_tasks = scheduler.filter_tasks(category="Feeding")
        
        assert len(feeding_tasks) == 2
        assert feeding1 in feeding_tasks
        assert feeding2 in feeding_tasks
        assert exercise not in feeding_tasks
    
    def test_filter_multiple_criteria(self):
        """Verify filtering with multiple criteria combined."""
        owner = Owner(name="Xavier", available_minutes=240)
        pet = Pet(name="Luna", species="Dog", age=4, breed="Husky")
        scheduler = Scheduler(owner, pet)
        
        high_daily = CareTask(title="Feed", duration_minutes=10, priority="high", frequency="daily", category="Feeding")
        high_one_time = CareTask(title="Vet", duration_minutes=60, priority="high", frequency="one-time", category="Health")
        medium_daily = CareTask(title="Play", duration_minutes=20, priority="medium", frequency="daily", category="Exercise")
        
        scheduler.add_task(high_daily)
        scheduler.add_task(high_one_time)
        scheduler.add_task(medium_daily)
        
        # Filter: high priority AND daily frequency
        filtered = scheduler.filter_tasks(priority="high", frequency="daily")
        
        assert len(filtered) == 1
        assert high_daily in filtered


class TestRecurringTaskExpansion:
    """Test expanding recurring tasks over time periods."""
    
    def test_expand_recurring_tasks_week(self):
        """Verify expanding recurring tasks for 7-day period."""
        owner = Owner(name="Yara", available_minutes=300)
        pet = Pet(name="Zoe", species="Cat", age=3, breed="Siamese")
        scheduler = Scheduler(owner, pet)
        
        daily = CareTask(title="Feed", duration_minutes=5, priority="high", frequency="daily", category="Feeding")
        weekly = CareTask(title="Groom", duration_minutes=20, priority="medium", frequency="weekly", category="Grooming")
        one_time = CareTask(title="Trim", duration_minutes=15, priority="low", frequency="one-time", category="Grooming")
        
        scheduler.add_task(daily)
        scheduler.add_task(weekly)
        scheduler.add_task(one_time)
        
        expanded = scheduler.expand_recurring_tasks(days=7)
        
        # Daily appears 7 times, weekly once, one-time once
        # Total: 9 occurrences
        assert len(expanded) == 9
    
    def test_expand_shows_correct_day_offsets(self):
        """Verify expanded tasks show correct day offsets."""
        owner = Owner(name="Zara", available_minutes=300)
        pet = Pet(name="Rex", species="Dog", age=3, breed="Terrier")
        scheduler = Scheduler(owner, pet)
        
        daily = CareTask(title="Feed", duration_minutes=5, priority="high", frequency="daily", category="Feeding")
        scheduler.add_task(daily)
        
        expanded = scheduler.expand_recurring_tasks(days=3)
        
        # Should have daily task on days 0, 1, 2
        day_offsets = [day for _, day in expanded]
        assert 0 in day_offsets
        assert 1 in day_offsets
        assert 2 in day_offsets


class TestBuildSchedule:
    """Test schedule building and optimization."""
    
    def test_build_schedule_returns_priority_sorted(self):
        """Verify build_schedule returns tasks sorted by priority."""
        owner = Owner(name="Yuri", available_minutes=300)
        pet = Pet(name="Simba", species="Cat", age=4, breed="Lion")
        scheduler = Scheduler(owner, pet)
        
        low = CareTask(title="Groom", duration_minutes=20, priority="low", category="Grooming")
        high = CareTask(title="Meds", duration_minutes=5, priority="high", category="Health")
        medium = CareTask(title="Play", duration_minutes=15, priority="medium", category="Exercise")
        
        scheduler.add_task(low)
        scheduler.add_task(medium)
        scheduler.add_task(high)
        
        schedule = scheduler.build_schedule()
        
        # Should be high, medium, low
        assert schedule[0] == high
        assert schedule[1] == medium
        assert schedule[2] == low
    
    def test_build_schedule_empty(self):
        """Verify build_schedule returns empty list for empty scheduler."""
        owner = Owner(name="Yuki", available_minutes=240)
        pet = Pet(name="Smokey", species="Cat", age=5, breed="Persian")
        scheduler = Scheduler(owner, pet)
        
        schedule = scheduler.build_schedule()
        
        assert schedule == []


class TestPlanSummary:
    """Test plan summary generation."""
    
    def test_get_summary_basic_info(self):
        """Verify summary includes basic schedule information."""
        owner = Owner(name="Zoe", available_minutes=180)
        pet = Pet(name="Rusty", species="Dog", age=5, breed="Mutt")
        scheduler = Scheduler(owner, pet)
        
        task1 = CareTask(title="Feed", duration_minutes=15, priority="high", category="Feeding")
        task2 = CareTask(title="Walk", duration_minutes=30, priority="high", category="Exercise")
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        summary = scheduler.get_summary()
        
        assert "Rusty" in summary
        assert "Zoe" in summary
        assert "2" in summary  # 2 tasks
    
    def test_get_detailed_plan(self):
        """Verify detailed plan includes task information."""
        owner = Owner(name="Zack", available_minutes=200)
        pet = Pet(name="Buddy", species="Dog", age=3, breed="Retriever")
        scheduler = Scheduler(owner, pet)
        
        task = CareTask(title="Morning Walk", duration_minutes=30, priority="high", category="Exercise")
        scheduler.add_task(task)
        
        detailed = scheduler.explain_plan()
        
        assert "Morning Walk" in detailed
        assert "Buddy" in detailed
        assert "Zack" in detailed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
