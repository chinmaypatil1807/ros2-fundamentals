# ROS2 Fundamentals – Week 1

This repository documents my foundational practice with ROS2 communication primitives using Python.

The goal of this week was to strengthen core ROS2 concepts before progressing into higher-level systems such as Nav2 and autonomous navigation.

---

## Implemented Concepts

- Publisher / Subscriber nodes  
- Service / Client communication  
- Custom topic creation  
- ROS2 workspace structuring  
- Package setup and debugging build issues  

---

## Architectural Understanding

- **Topics** enable asynchronous, continuous communication  
  (e.g., sensor data streams, velocity commands such as `/cmd_vel`).

- **Services** implement synchronous request–response interactions  
  (e.g., triggering actions or requesting specific data).

- **Actions** (conceptual understanding) are suited for long-running, goal-oriented, and cancellable tasks  
  (e.g., navigation to a pose).

---

## Packages Included

### `my_first_pkg`
Basic control experiments:
- Simple publisher  
- cmd_vel publisher  
- Turn controller  
- Wall stop logic  

### `test_workspace`
Core communication practice:
- Publisher / Subscriber implementation  
- Service / Client implementation  

---

## Build Instructions

```bash
colcon build
source install/setup.bash
