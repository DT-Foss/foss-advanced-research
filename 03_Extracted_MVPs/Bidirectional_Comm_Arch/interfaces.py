from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EMGSignal:
    timestamp: float
    channels: List[float] # 8 channels
    quality_index: float

@dataclass
class Token:
    id: int
    label: str
    confidence: float

class IEMGFrontEnd(ABC):
    """Interface for the ADS1299-based EMG Acquisition Unit."""
    
    @abstractmethod
    def initialize(self, gain: int, sample_rate: int) -> bool:
        """Configure ADC settings."""
        pass

    @abstractmethod
    def read_frame(self) -> EMGSignal:
        """Read a frame of EMG data (250 SPS)."""
        pass

class ISignalProcessor(ABC):
    """Interface for the Signal Processing Pipeline (ICA -> Kalman -> TCN)."""
    
    @abstractmethod
    def process_signal(self, raw_signal: EMGSignal) -> EMGSignal:
        """Apply noise cancellation (ICA) and adaptive filtering (Kalman)."""
        pass
        
    @abstractmethod
    def decode_token(self, processed_signal: EMGSignal) -> Optional[Token]:
        """TCN Inference to classify speech tokens."""
        pass

class INFMIMeshTransceiver(ABC):
    """Interface for the 13.56 MHz NFMI Mesh Network."""
    
    @abstractmethod
    def start_tdma_slot(self, slot_id: int):
        """Sync to TDMA slot structure (8ms windows)."""
        pass
        
    @abstractmethod
    def broadcast_packet(self, payload: bytes, encrypt: bool = True):
        """Send data via magnetic induction."""
        pass
        
    @abstractmethod
    def receive_packet(self) -> bytes:
        """Listen for incoming packets."""
        pass

class IHapticFeedback(ABC):
    """Interface for Transcutaneous Non-Acoustic Perceptive Stimulation."""
    
    @abstractmethod
    def encode_stimulus(self, token: Token):
        """Map recognized token to haptic pattern."""
        pass
        
    @abstractmethod
    def actuate_coil(self, coil_id: int, intensity: float, duration_ms: float):
        """Trigger electromagnetic actuator."""
        pass
        
    @abstractmethod
    def actuate_bone_conductor(self, frequency: float, amplitude: float):
        """Trigger piezoelectric bone conductor."""
        pass
