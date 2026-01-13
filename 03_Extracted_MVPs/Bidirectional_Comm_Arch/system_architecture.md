# System Architecture: Bidirectional Silent Communication

## Overview
This document defines the architectural scaffold for the Silent Communication System, combining Subvocal EMG, NFMI Mesh Networking, and Haptic Feedback.

## 1. Data Flow Pipeline

```mermaid
graph LR
    A[User Subvocalization] --> B[EMG Front-End (ADS1299)]
    B --> C[Signal Processing Unit]
    subgraph DSP Pipeline
        C1[Online Indep. Component Analysis (ICA)]
        C2[Adaptive Kalman Filter]
        C3[Temporal Convolutional Net (TCN)]
        C -- Raw Data --> C1 --> C2 --> C3
    end
    C3 -- Recognized Token --> D[NFMI Mesh Transceiver]
    D -- Encrypted Magnetic Packet --> E[NFMI Receiver (Peer)]
    E --> F[Haptic Encoder]
    F --> G[Actuator Array (Coils + Bone Conductor)]
    G --> H[User Perception]
```

## 2. Component Specifications

### 2.1 Subvocal EMG (Input)
- **Sensor**: 8-channel differential EMG.
- **Frontend**: ADS1299-4.
- **Sample Rate**: 250 SPS.
- **Preprocessing**: 
    - 50Hz/60Hz Notch Filter.
    - ICA for artifact removal (chewing, movement).
    - Kalman Filter for state estimation ($Q=0.01, R=0.1$).

### 2.2 Token Classification (AI)
- **Model**: Temporal Convolutional Network (TCN).
- **Lexicon**: 32 initial command tokens.
- **Accuracy Target**: >91% within calibration set.

### 2.3 NFMI Mesh (Transport)
- **Frequency**: 13.56 MHz (Magnetic Induction).
- **Protocol**: TDMA with Frequency Hopping.
- **Encryption**: AES-128-CTR.
- **Range**: < 2m (LPI/LPD security).

### 2.4 Haptic Feedback (Output)
- **Actuators**: Bistable Electromagnetic Micro-coils.
- **Mapping**: Phoneme-to-Tactile encoding.
- **Bone Conduction**: Supplemental high-frequency carrier.

## 3. Power Budget (Est.)

| Module | Power (Avg) |
|--------|-------------|
| ADS1299 | 4.65 mW |
| DSP (Cortex M0+) | 0.75 mW |
| NFMI Transceiver | 0.16 mW |
| Actuators (Peak) | 30.0 mW |
| **Total (Avg)** | **~41 mW** |

## 4. Software Layers (Python Scaffold)
See `interfaces.py` for abstract base classes defining the contract between:
- Hardware Abstraction Layer (HAL)
- Signal Processing Logic
- Network Stack
- User Interface (Haptics)
