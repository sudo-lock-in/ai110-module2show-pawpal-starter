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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
