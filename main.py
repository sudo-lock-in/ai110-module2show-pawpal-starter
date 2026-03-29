from pawpal_system import CareTask, Pet, Owner, Scheduler

# Create an Owner
owner = Owner(
    name="Sarah",
    available_minutes=120,
    preferred_start_time="08:00",
    preferences=["morning walks", "interactive play"]
)

# Create two Pets
dog = Pet(
    name="Max",
    species="Dog",
    age=3,
    breed="Golden Retriever",
    weight=32.5
)

cat = Pet(
    name="Whiskers",
    species="Cat",
    age=5,
    breed="Tabby",
    weight=4.2
)

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create a Scheduler for the dog
dog_scheduler = Scheduler(owner, dog)

# Add tasks for the dog with different durations and priorities
task1 = CareTask(
    title="Morning Walk",
    duration_minutes=30,
    priority="high",
    frequency="daily",
    category="Exercise",
    description="Take Max for a morning walk in the park for exercise and bathroom break"
)

task2 = CareTask(
    title="Feed Breakfast",
    duration_minutes=10,
    priority="high",
    frequency="daily",
    category="Feeding",
    description="Serve premium dog food with fresh water"
)

task3 = CareTask(
    title="Playtime",
    duration_minutes=20,
    priority="medium",
    frequency="daily",
    category="Entertainment",
    description="Interactive play with toys to keep Max mentally stimulated"
)

task4 = CareTask(
    title="Grooming",
    duration_minutes=15,
    priority="low",
    frequency="weekly",
    category="Grooming",
    description="Brush coat and check for any skin issues"
)

# Add tasks to the scheduler
for task in [task1, task2, task3, task4]:
    dog_scheduler.add_task(task)

# Add some notes to tasks
task1.add_note("Max prefers off-leash play at the park")
task2.add_note("Use the organic grain-free kibble")

# Create a Scheduler for the cat
cat_scheduler = Scheduler(owner, cat)

# Add tasks for the cat
cat_task1 = CareTask(
    title="Feed Breakfast",
    duration_minutes=5,
    priority="high",
    frequency="daily",
    category="Feeding",
    description="Serve wet food in the morning"
)

cat_task2 = CareTask(
    title="Clean Litter Box",
    duration_minutes=10,
    priority="high",
    frequency="daily",
    category="Cleaning",
    description="Scoop and replace litter"
)

cat_task3 = CareTask(
    title="Interactive Play",
    duration_minutes=15,
    priority="medium",
    frequency="daily",
    category="Entertainment",
    description="Play with feather toy or laser pointer"
)

# Add tasks to cat scheduler
for task in [cat_task1, cat_task2, cat_task3]:
    cat_scheduler.add_task(task)

# Mark one task as completed
task2.mark_completed()

# Print Today's Schedule
print("=" * 70)
print("TODAY'S SCHEDULE - PAW PAL SYSTEM".center(70))
print("=" * 70)
print()

# Print Owner Profile
print("OWNER INFORMATION")
print("-" * 70)
print(owner.get_profile())
print()

# Print Dog's Schedule
print("=" * 70)
print("DOG - MAX'S CARE PLAN")
print("=" * 70)
print()
print(dog_scheduler.explain_plan())
print()
print(dog_scheduler.get_summary())
print()

# Print Cat's Schedule
print("=" * 70)
print("CAT - WHISKERS' CARE PLAN")
print("=" * 70)
print()
print(cat_scheduler.explain_plan())
print()
print(cat_scheduler.get_summary())
print()

# Print Owner's aggregate information
print("=" * 70)
print("OWNER'S COMPLETE TASK OVERVIEW")
print("=" * 70)
all_tasks = owner.get_all_tasks()
all_pending = owner.get_all_pending_tasks()
high_priority = owner.get_high_priority_tasks()

print(f"Total Tasks Across All Pets: {len(all_tasks)}")
print(f"Pending Tasks: {len(all_pending)}")
print(f"High Priority Tasks: {len(high_priority)}")
print()

print("All High Priority Tasks:")
for task in high_priority:
    pet_name = "Max" if task in dog_scheduler.get_tasks() else "Whiskers"
    print(f"  • {task.title} ({pet_name}) - {task.duration_minutes} min")
print()

print("=" * 70)
