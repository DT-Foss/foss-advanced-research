import random
from typing import List, Dict, Any

class VerticalBase:
    """Base class for all verticals."""
    def __init__(self, vertical_name: str):
        self.vertical_name = vertical_name
        self.handcurated_mechanisms = self._load_mechanisms()
        self.causes_effects_matrix = self._load_matrix()

    def _load_mechanisms(self) -> List[Dict]:
        """Mock loader for handcurated mechanisms."""
        return [
            {
                'cause': f'{self.vertical_name} Cause A',
                'effect': f'{self.vertical_name} Effect B',
                'strength': 0.85,
                'cot_narrative': ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5'],
                'lag_min_days': 5,
                'lag_max_days': 10,
                'evidence_level': 4
            }
            for _ in range(10)
        ]

    def _load_matrix(self) -> Dict:
        """Mock loader for cause-effect matrix."""
        return {
            'causes': [f'{self.vertical_name} Cause {i}' for i in range(10)],
            'effects': [f'{self.vertical_name} Effect {i}' for i in range(5)]
        }

    def generate_batch(self, count: int = 500) -> Dict:
        """Generates a batch of CoT chains."""
        chains = []
        # 40% handcurated
        for _ in range(int(count * 0.4)):
            chains.append(self._generate_from_handcurated())
        # 60% template
        for _ in range(int(count * 0.6)):
            chains.append(self._generate_from_template())
        
        return {
            'metadata': {'vertical': self.vertical_name, 'count': count},
            'chains': chains
        }

    def _generate_from_handcurated(self) -> Dict:
        mechanism = random.choice(self.handcurated_mechanisms)
        return {
            'cause': mechanism['cause'],
            'effect': mechanism['effect'],
            'strength': mechanism['strength'],
            'confidence': 'very_high',
            'cot_narrative': mechanism['cot_narrative'],
            'lag_min_days': mechanism['lag_min_days'],
            'lag_max_days': mechanism['lag_max_days'],
            'source': 'handcurated_mechanism'
        }

    def _generate_from_template(self) -> Dict:
        cause = random.choice(self.causes_effects_matrix['causes'])
        effect = random.choice(self.causes_effects_matrix['effects'])
        return {
            'cause': cause,
            'effect': effect,
            'strength': random.uniform(0.7, 0.95),
            'confidence': 'high',
            'cot_narrative': [f"Processing {cause}", f"leads to {effect}"],
            'lag_min_days': 1,
            'lag_max_days': 30,
            'source': 'generated_with_template'
        }

class GeopoliticalVertical(VerticalBase):
    def __init__(self):
        super().__init__("GEOPOLITICAL")

class FintechVertical(VerticalBase):
    def __init__(self):
        super().__init__("FINTECH")

class PharmaVertical(VerticalBase):
    def __init__(self):
        super().__init__("PHARMA")

class PrePolishedCoTGenerator:
    def __init__(self, vertical: str):
        if vertical == "GEOPOLITICAL":
            self.engine = GeopoliticalVertical()
        elif vertical == "FINTECH":
            self.engine = FintechVertical()
        elif vertical == "PHARMA":
            self.engine = PharmaVertical()
        else:
            raise ValueError(f"Unknown vertical: {vertical}")
    
    def generate(self, count=500):
        return self.engine.generate_batch(count)
