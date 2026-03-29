import streamlit as st
from pawpal_system import CareTask, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

# Initialize session state for owner
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=120,
        preferred_start_time="08:00"
    )

if "pets" not in st.session_state:
    st.session_state.pets = []

if "schedulers" not in st.session_state:
    st.session_state.schedulers = {}

owner = st.session_state.owner

# Owner configuration
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col2:
    owner.available_minutes = st.number_input("Available minutes", value=owner.available_minutes, min_value=15, max_value=480)

st.markdown("### Add Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

col1, col2 = st.columns(2)
with col1:
    breed = st.text_input("Breed", value="Mixed")
with col2:
    age = st.number_input("Age (years)", value=2, min_value=0, max_value=25)

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, breed=breed, age=age)
    st.session_state.pets.append(new_pet)
    owner.add_pet(new_pet)
    st.session_state.schedulers[pet_name] = Scheduler(owner, new_pet)
    st.success(f"✓ {pet_name} added!")
    st.rerun()

if st.session_state.pets:
    st.write(f"**Pets ({len(st.session_state.pets)}):**")
    for pet in st.session_state.pets:
        st.write(f"• {pet.name} ({pet.species}, {pet.age} years old)")

st.markdown("### Add Task to Pet")

if st.session_state.pets:
    selected_pet = st.selectbox("Select pet", [p.name for p in st.session_state.pets])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    
    category = st.text_input("Category", value="Exercise")
    description = st.text_area("Description", value="")
    
    if st.button("Add Task"):
        try:
            new_task = CareTask(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                category=category,
                description=description
            )
            
            # Add task to selected pet and scheduler
            pet = owner.find_pet_by_name(selected_pet)
            if pet:
                scheduler = st.session_state.schedulers[selected_pet]
                scheduler.add_task(new_task)
                st.success(f"✓ Task '{task_title}' added to {selected_pet}!")
                st.rerun()
        except ValueError as e:
            st.error(f"✗ Error: {e}")
else:
    st.info("Add a pet first to create tasks.")

st.divider()

st.subheader("Build Schedule")

if st.session_state.pets:
    selected_pet_for_schedule = st.selectbox("View schedule for:", [p.name for p in st.session_state.pets], key="schedule_selector")
    
    if st.button("Generate Schedule"):
        pet = owner.find_pet_by_name(selected_pet_for_schedule)
        scheduler = st.session_state.schedulers[selected_pet_for_schedule]
        
        if scheduler.get_tasks():
            # Display the care plan
            st.markdown("#### 📋 Care Plan")
            st.text(scheduler.explain_plan())
            
            # Display the summary
            st.markdown("#### 📊 Summary")
            st.text(scheduler.get_summary())
            
            # Display tasks by priority
            st.markdown("#### 🎯 Tasks by Priority")
            col1, col2, col3 = st.columns(3)
            with col1:
                high = scheduler.get_tasks_by_priority("high")
                st.metric("High Priority", len(high))
            with col2:
                med = scheduler.get_tasks_by_priority("medium")
                st.metric("Medium Priority", len(med))
            with col3:
                low = scheduler.get_tasks_by_priority("low")
                st.metric("Low Priority", len(low))
            
            # Display pending vs completed
            st.markdown("#### ✓ Task Status")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Pending", len(scheduler.get_pending_tasks()))
            with col2:
                st.metric("Completed", len(scheduler.get_completed_tasks()))
        else:
            st.info(f"No tasks added for {selected_pet_for_schedule} yet.")
else:
    st.info("Add a pet and tasks to generate a schedule.")
