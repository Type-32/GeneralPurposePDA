# General Purpose PDA
I'm working on this thing as a sort-of passion project, just to mess around and learn how hardware development works.

Oh, and to also practice writing python since I haven't done so for a long time.

> [!MATERIALS]
> - ESP32-S3-Touch-4.3-LCD from **WaveShare**
> - 3D printed case (.stl files here later)
> - A Type-C cable on both ends or on one end
> - A computer with a USB/Type-C port

I use macOS. I don't know if this will work on Windows or Linux, but I'll try to make it work on those platforms. (If it doesn't work on other platforms)

## OS Architecture in Code Implementation
I'm writing this in a separate section because it clarifies some things, for me, and for you, the user.

### Iteration 1
The graph below is the first iteration of the OS architecture. My current code (October 11, 2024, 10:40 AM UTC+8) can be represented with the graph.
```mermaid
graph TD
    subgraph OS_Program["OS Program"]
        Load["load() (Entry Point)"]
        Main["async main()"]
        
        subgraph OS_Aync["OS Async Thread"]
            
            subgraph Async_UI_Thread["Async UI Thread"]
                System_UI["System UI (Upper Layer)"]
                App_UI["App UI (Lower Layer)"]
                
                
                
                System_UI --> App_UI
                App_UI --> System_UI
            end
            subgraph Garbage_Collector ["Async GC"]
                GC_Collect["Collect Garbage"]
                GC_Collect --Every Minute--> GC_Collect
            end
        end
    end
    
    Program_Entry[Program Entry] --> OS_Program
    Load --> Main
    Main --> OS_Aync
```

This architecture is clear, simple, and easy to understand. However, it's not quite functional. Here's the downsides:
- The System UI and App UI are in the same thread. This means that if the System UI or the App UI is still processing or has multiple `asyncio.sleep()` calls, the entire thread will be delayed.
- The GC is not controlled by the OS. It's just a simple loop that runs every minute. This is not efficient and can cause performance issues.
- The Application Logic layer is not yet implemented.

### Iteration 2
```mermaid
---
title: "PDA-OS Code Impl. Architecture"
---
graph TD
    subgraph OS_Program["OS Program"]
        Load["load() (Entry Point)"]
        Main["async main()"]
        
        subgraph OS_Aync["OS Async Thread"]
            Controller["OS Async Thread Controller"]
            
            subgraph Async_System_UI_Thread["Async System UI Thread"]
                Notifications
                Modals
                Status["Status Indicators"]
            end
            
            subgraph Async_App_UI_Thread["Async App UI Thread"]
                App_UI["App UI (Lower Layer)"]
            end
            
            subgraph Garbage_Collector ["Async GC"]
                GC_Collect["Collect Garbage"]
                GC_Interval --> GC_Collect
                GC_Collect --> GC_Interval
            end
            
            Controller --> Async_System_UI_Thread --> Async_App_UI_Thread
            Controller --> GC_Interval
        end
    end
    
    subgraph Globals["OS Globals"]
        subgraph App_Architecture["Application Architecture"]
            App_Data_Model["App Data"]
            App_Logic["App Logic"]
            App_API["App API"]
        end
        subgraph OS_Level_API["OS-Level API"]
            Notifications_API["Notifications API"]
            Modals_API["Modals API"]
            Settings_API["Settings API"]
            Internet_API["Internet API (connectivity.py)"]
        end
        
        App_Data_Model --> App_Logic
        App_API --> App_Logic
        App_Logic --> App_UI
        
        Notifications_API --> Notifications
        Modals_API --> Modals
        Settings_API --> Status
        Internet_API --> Status
    end
    
    Program_Entry[Program Entry] --> OS_Program
    Program_Entry --> Globals
    Load --> Main
    Main --> Controller
```

- The Application Logic layer is now implemented.
- A New and better Async Jobs system
- The GC is now controlled by the OS. It's now a loop that runs every controlled duration

