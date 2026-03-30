# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The **Scheduler** class provides intelligent task management and planning features:

### Key Features

- **Unified Filtering**: Filter tasks by status, priority, category, and frequency with a single method
- **Smart Sorting**: Multiple sorting strategies (priority, time, duration, fit optimization, frequency)
- **Conflict Detection**: Automatic detection of scheduling conflicts with detailed overlap analysis
- **Recurring Tasks**: Automatic creation of next occurrences for daily, weekly, and monthly tasks
- **Time Window Queries**: Find tasks within specific time slots and suggest available time slots
- **Capacity Planning**: Check owner availability and detect overbooking across multiple pets
- **Schedule Optimization**: Build optimized schedules based on priority and time constraints

### Example Usage

```python
# Filter tasks efficiently
pending_high_priority = scheduler.filter_tasks(status='pending', priority='high')

# Sort by different criteria
sorted_by_time = scheduler.sort_tasks(by='time')
sorted_by_fit = scheduler.sort_tasks(by='fit')  # Optimal packing

# Detect conflicts automatically
if scheduler.has_scheduling_conflicts():
    warnings = scheduler.get_detailed_conflict_warnings()
    scheduler.print_conflict_warnings()

# Handle recurring tasks
next_task = scheduler.mark_task_completed_with_recurrence(task)

# Find available time slots
available_slot = scheduler.suggest_next_available_time(duration_minutes=30)

# Get comprehensive summaries
detailed_plan = scheduler.get_plan_summary(detailed=True)
quick_summary = scheduler.get_plan_summary(detailed=False)
```

### Performance

- **Optimized Filtering**: Single unified method eliminates redundant filtering logic
- **Shared Utilities**: Centralized time conversion functions reduce code duplication
- **Efficient Conflict Detection**: O(n²) detection with optional detailed analysis
- **Code Reduction**: 20% less code, 41% fewer methods through smart consolidation
