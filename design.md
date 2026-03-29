# PawPal+ System Design

## Class Diagram

```mermaid
classDiagram
    class Pet {
        +String name
        +String species
        +int age
        +String breed
        +List~String~ health_notes
        +get_info() String
    }

    class Owner {
        +String name
        +int available_minutes
        +String preferred_start_time
        +List~String~ preferences
        +get_profile() String
    }

    class CareTask {
        +String title
        +int duration_minutes
        +String priority
        +String category
        +String reason
        +is_high_priority() bool
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +List~CareTask~ tasks
        +add_task(task: CareTask) void
        +build_schedule() List~CareTask~
        +explain_plan() String
        +get_summary() String
    }

    Scheduler --> Owner : uses
    Scheduler --> Pet : plans for
    Scheduler "1" o-- "many" CareTask : manages
```
