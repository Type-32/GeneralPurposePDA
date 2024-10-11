# General Purpose PDA
I'm working on this thing as a sort-of passion project, just to mess around and learn how hardware development works.

Oh, and to also practice writing python since I haven't done so for a long time.

> [!MATERIALS]
> - ESP32-S3-Touch-4.3-LCD from **WaveShare**
> - 3D printed case (.stl files here later)
> - A Type-C cable on both ends or on one end
> - A computer with a USB/Type-C port

I use macOS. I don't know if this will work on Windows or Linux, but I'll try to make it work on those platforms. (If it doesn't work on other platforms)

## PDA-OS Design

I'm programming an Operating System for this little thing. I'm going to call it **PDA-OS**. Name is subject to change.

The following are graphs that illustrates the design and architecture of the OS.

### Eraser.io Graphs
[View on Eraser![](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8/preview?elements=7VZFpVqGDRQeEpiym1F4xw&type=embed)](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8?elements=7VZFpVqGDRQeEpiym1F4xw)

[View on Eraser![](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8/preview?elements=q1_MrWodHduFDftwzvMJ2g&type=embed)](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8?elements=q1_MrWodHduFDftwzvMJ2g)

[View on Eraser![](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8/preview?elements=imNGCxBYVQlN6b_r4oDvcA&type=embed)](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8?elements=imNGCxBYVQlN6b_r4oDvcA)

[View on Eraser![](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8/preview?elements=wPs7d8Z0bUTKdvVxWrPIpg&type=embed)](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8?elements=wPs7d8Z0bUTKdvVxWrPIpg)

[View on Eraser![](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8/preview?elements=wWReXQhWIR3sXBY1d6hh0g&type=embed)](https://app.eraser.io/workspace/0DAncmHruwPnXU1Gm9y8?elements=wWReXQhWIR3sXBY1d6hh0g)

### Mermaid Graphs
```mermaid
graph TD
    subgraph "Hardware Layer"
        ESP32S3[ESP32S3]
        Display
        Memory
        WiFiHW[WiFi Hardware]
    end

    subgraph "MicroPython Layer"
        MP[MicroPython Runtime]
    end

    subgraph "OS-Level"
        OSCore[OS Core]
        API[API Layer]
        FileManager[File Manager]
        SettingsManager[Settings Manager]
        NotificationManager[Notification Manager]
        WiFiManager[WiFi Manager]
        PowerManager[Power Manager]
    end

    subgraph "OS-Background-Level"
        Scheduler
        EventSystem[Event System]
    end

    subgraph "UI Layer"
        UIManager[UI Manager]
        InputHandler[Input Handler]
    end

    subgraph "Application Layer"
        DefaultApps[Default Applications]
        UserApps[User Applications]
        AppStore[App Store]
    end

    ESP32S3 --> MP
    MP --> OSCore
    OSCore --> API
    OSCore --> FileManager
    OSCore --> SettingsManager
    OSCore --> NotificationManager
    OSCore --> WiFiManager
    OSCore --> PowerManager
    OSCore --> Scheduler
    OSCore --> EventSystem
    OSCore --> UIManager
    API --> DefaultApps
    API --> UserApps
    API --> AppStore
    UIManager --> InputHandler
    ESP32S3 --> Display
    ESP32S3 --> Memory
    ESP32S3 --> WiFiHW
```

```mermaid
graph TD
    subgraph "OS Core"
        Init[Initialize System]
        LoadConfig[Load Configuration]
        StartManagers[Start System Managers]
        StartScheduler[Start Scheduler]
        StartEventSystem[Start Event System]
        StartUI[Start UI]
        LoadDefaultApps[Load Default Apps]
    end

    subgraph "File Manager"
        FM_Init[Initialize]
        FM_Read[Read File]
        FM_Write[Write File]
        FM_Delete[Delete File]
        FM_List[List Files]
    end

    subgraph "Settings Manager"
        SM_Init[Initialize]
        SM_Get[Get Setting]
        SM_Set[Set Setting]
        SM_Save[Save Settings]
        SM_Load[Load Settings]
    end

    subgraph "Notification Manager"
        NM_Init[Initialize]
        NM_Create[Create Notification]
        NM_Update[Update Notification]
        NM_Delete[Delete Notification]
        NM_List[List Notifications]
    end

    subgraph "WiFi Manager"
        WM_Init[Initialize]
        WM_Connect[Connect to WiFi]
        WM_Disconnect[Disconnect WiFi]
        WM_Status[Get WiFi Status]
        WM_ScanNetworks[Scan Networks]
    end

    subgraph "Power Manager"
        PM_Init[Initialize]
        PM_Sleep[Enter Sleep Mode]
        PM_Wake[Wake from Sleep]
        PM_Status[Get Power Status]
    end

    Init --> LoadConfig
    LoadConfig --> StartManagers
    StartManagers --> StartScheduler
    StartScheduler --> StartEventSystem
    StartEventSystem --> StartUI
    StartUI --> LoadDefaultApps

    StartManagers --> FM_Init
    StartManagers --> SM_Init
    StartManagers --> NM_Init
    StartManagers --> WM_Init
    StartManagers --> PM_Init
```

```mermaid
graph TD
    subgraph "Scheduler"
        Sch_Init[Initialize]
        Sch_AddTask[Add Task]
        Sch_RemoveTask[Remove Task]
        Sch_RunTasks[Run Tasks]
        Sch_Sleep[Sleep Until Next Task]
    end

    subgraph "Event System"
        ES_Init[Initialize]
        ES_Subscribe[Subscribe to Event]
        ES_Unsubscribe[Unsubscribe from Event]
        ES_Publish[Publish Event]
        ES_ProcessEvents[Process Events]
    end

    Sch_Init --> Sch_AddTask
    Sch_AddTask --> Sch_RunTasks
    Sch_RunTasks --> Sch_Sleep
    Sch_Sleep --> Sch_RunTasks
    Sch_RemoveTask --> Sch_RunTasks

    ES_Init --> ES_Subscribe
    ES_Subscribe --> ES_Publish
    ES_Publish --> ES_ProcessEvents
    ES_Unsubscribe --> ES_ProcessEvents
```

```mermaid
graph TD
    subgraph "UI Manager"
        UI_Init[Initialize]
        UI_DrawScreen[Draw Screen]
        UI_UpdateScreen[Update Screen]
        UI_ShowPopup[Show Popup]
        UI_HidePopup[Hide Popup]
    end

    subgraph "Input Handler"
        IH_Init[Initialize]
        IH_PollInput[Poll Input]
        IH_ProcessInput[Process Input]
        IH_DispatchEvent[Dispatch Input Event]
    end

    UI_Init --> UI_DrawScreen
    UI_DrawScreen --> UI_UpdateScreen
    UI_UpdateScreen --> UI_ShowPopup
    UI_ShowPopup --> UI_HidePopup

    IH_Init --> IH_PollInput
    IH_PollInput --> IH_ProcessInput
    IH_ProcessInput --> IH_DispatchEvent
    IH_DispatchEvent --> UI_UpdateScreen
```

```mermaid
graph TD
    subgraph "Application Manager"
        AM_Init[Initialize]
        AM_LoadApp[Load Application]
        AM_UnloadApp[Unload Application]
        AM_StartApp[Start Application]
        AM_StopApp[Stop Application]
    end

    subgraph "Default Applications"
        DA_Settings[Settings App]
        DA_FileExplorer[File Explorer]
        DA_AppStore[App Store]
    end

    subgraph "User Applications"
        UA_Install[Install User App]
        UA_Uninstall[Uninstall User App]
        UA_Update[Update User App]
    end

    subgraph "App Store"
        AS_Browse[Browse Apps]
        AS_Download[Download App]
        AS_Update[Update App]
    end

    AM_Init --> AM_LoadApp
    AM_LoadApp --> AM_StartApp
    AM_StopApp --> AM_UnloadApp

    AM_LoadApp --> DA_Settings
    AM_LoadApp --> DA_FileExplorer
    AM_LoadApp --> DA_AppStore

    UA_Install --> AM_LoadApp
    UA_Uninstall --> AM_UnloadApp
    UA_Update --> AM_LoadApp

    AS_Browse --> AS_Download
    AS_Download --> UA_Install
    AS_Update --> UA_Update
```

```mermaid
graph TD
    subgraph "API Layer"
        API_Init[Initialize API]
        API_RegisterApp[Register Application]
        API_UnregisterApp[Unregister Application]
    end

    subgraph "File API"
        FA_Open[Open File]
        FA_Read[Read File]
        FA_Write[Write File]
        FA_Close[Close File]
        FA_Delete[Delete File]
    end

    subgraph "Settings API"
        SA_GetSetting[Get Setting]
        SA_SetSetting[Set Setting]
        SA_SaveSettings[Save Settings]
    end

    subgraph "Notification API"
        NA_CreateNotification[Create Notification]
        NA_UpdateNotification[Update Notification]
        NA_RemoveNotification[Remove Notification]
    end

    subgraph "WiFi API"
        WA_Connect[Connect to WiFi]
        WA_Disconnect[Disconnect from WiFi]
        WA_GetStatus[Get WiFi Status]
    end

    subgraph "Power API"
        PA_Sleep[Enter Sleep Mode]
        PA_Wake[Wake from Sleep]
        PA_GetStatus[Get Power Status]
    end

    subgraph "Event API"
        EA_Subscribe[Subscribe to Event]
        EA_Unsubscribe[Unsubscribe from Event]
        EA_PublishEvent[Publish Event]
    end

    subgraph "UI API"
        UIA_DrawElement[Draw UI Element]
        UIA_UpdateElement[Update UI Element]
        UIA_RemoveElement[Remove UI Element]
    end

    API_Init --> API_RegisterApp
    API_RegisterApp --> API_UnregisterApp

    API_Init --> FA_Open
    API_Init --> SA_GetSetting
    API_Init --> NA_CreateNotification
    API_Init --> WA_Connect
    API_Init --> PA_Sleep
    API_Init --> EA_Subscribe
    API_Init --> UIA_DrawElement
```

# OS Architecture in Code Implementation
I'm writing this in a separate section because it clarifies some things, for me, and for you, the user.

## Iteration 1
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

## Iteration 2
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