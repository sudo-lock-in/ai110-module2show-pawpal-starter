# PawPal+ Project Reflection

## 1. System Design

The app should be able to store pet info, track pet care tasks, consider constraints, and produce a daily plan.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The system uses four classes: Pet (pet profile), Owner (owner profile + time budget), CareTask (a single schedulable task), and Scheduler (builds and explains the daily plan). 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes and three changes were made:

1. Fixed relationship directions: The original diagram had Owner --> Scheduler, but Scheduler is the class that holds owner and pet as attributes. The arrows were reversed to Scheduler --> Owner and Scheduler --> Pet to reflect what the code actually expresses.

2. Removed CareTask.reason: The initial design put a reason field on CareTask, but reasoning about why a task was chosen belongs to the Scheduler, not the task itself. It was removed from CareTask since explain_plan() on Scheduler is the right place for that logic.

3. Replaced priority str with Priority = Literal["low", "medium", "high"]: A plain string allowed invalid values like "urgent" to pass silently. Using Literal enforces the allowed values at the type level without adding a fifth class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considered time (overlapping & exceeding), priority, and start preferences. I decided that time availability mattered the most since regardless of preference or priority if there is not enough time to do something, you simply cannot do it.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My Scheduler has many features and accounts for a lot of things, which makes it more complex and the code less readable. I believe the tradeoff is worth it to ensure that the schedules being made consider various aspects to create quality plans for owners.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
