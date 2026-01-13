import tensorflow as tf
import numpy as np
from typing import Tuple, Optional

class ChaosEnhancedPolicyGAN(tf.keras.Model):
    """GAN-System [103a] mit Adversarial-Härtung und Chaos-Integration"""
    
    def __init__(self, policy_dim: int = 256, chaos_dim: int = 3, name='ChaosGAN'):
        super(ChaosEnhancedPolicyGAN, self).__init__(name=name)
        self.policy_dim = policy_dim
        self.chaos_dim = chaos_dim
        self.r_param = 3.99 # Logistic map parameter for chaos
        self.adversarial_threshold = 0.8
        
        # Generator mit Chaos-Conditioning [103a1]
        self.generator = self._build_chaos_conditioned_generator()
        
        # Adversarial-gehärteter Multi-Task Discriminator [103a2]
        self.discriminator = self._build_hardened_discriminator()
        
        # Chaos-Integration Layer [103a3]
        self.chaos_processor = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='tanh', name='chaos_dense1'),
            tf.keras.layers.BatchNormalization(name='chaos_bn1'),
            tf.keras.layers.Dense(64, activation='relu', name='chaos_dense2'),
            tf.keras.layers.Dropout(0.2, name='chaos_dropout'),
            tf.keras.layers.Dense(32, activation='tanh', name='chaos_output')
        ], name='chaos_processor')
        
    def _build_chaos_conditioned_generator(self) -> tf.keras.Model:
        """Generator mit Chaos-State-Conditioning"""
        # Noise Input
        noise_input = tf.keras.layers.Input(shape=(100,), name='noise')
        # Chaos Input
        chaos_input = tf.keras.layers.Input(shape=(self.chaos_dim,), name='chaos_state')
        
        # Chaos-Verarbeitung
        chaos_processed = tf.keras.layers.Dense(64, activation='tanh')(chaos_input)
        chaos_processed = tf.keras.layers.BatchNormalization()(chaos_processed)
        
        # Fusion von Noise und Chaos
        combined = tf.keras.layers.concatenate([noise_input, chaos_processed])
        
        # Generator-Netzwerk
        x = tf.keras.layers.Dense(256, activation='relu')(combined)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        
        # Policy Output
        policy_output = tf.keras.layers.Dense(
            self.policy_dim, 
            activation='sigmoid', 
            name='policy_output'
        )(x)
        
        return tf.keras.Model(
            inputs=[noise_input, chaos_input], 
            outputs=policy_output, 
            name='chaos_generator'
        )
        
    def _build_hardened_discriminator(self) -> tf.keras.Model:
        """Adversarial-gehärteter Multi-Task Discriminator"""
        policy_input = tf.keras.layers.Input(shape=(self.policy_dim,), name='policy_input')
        
        # Hauptnetzwerk mit erhöhter Dropout-Rate für Adversarial-Resistenz
        x = tf.keras.layers.Dense(512, activation='leaky_relu')(policy_input)
        x = tf.keras.layers.Dropout(0.5)(x)  # Erhöhte Dropout-Rate
        x = tf.keras.layers.Dense(256, activation='leaky_relu')(x)
        x = tf.keras.layers.Dropout(0.4)(x)
        x = tf.keras.layers.Dense(128, activation='leaky_relu')(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        
        # Multi-Task Outputs
        # 1. Haupt-Authentizität (real/fake)
        authenticity = tf.keras.layers.Dense(1, activation='sigmoid', name='authenticity')(x)
        
        # 2. Adversarial-Detektion
        adversarial_score = tf.keras.layers.Dense(2, activation='softmax', name='adversarial')(x)
        
        # 3. Policy-Qualität
        quality_score = tf.keras.layers.Dense(3, activation='softmax', name='quality')(x)
        
        return tf.keras.Model(
            inputs=policy_input,
            outputs={
                'authenticity': authenticity,
                'adversarial': adversarial_score, 
                'quality': quality_score
            },
            name='hardened_discriminator'
        )
    
    def _generate_logistic_map_sequence(self, length: int, x0: Optional[float] = None) -> np.ndarray:
        """Generates a chaotic sequence using the Logistic Map: x_{n+1} = r * x_n * (1 - x_n)"""
        if x0 is None:
            x0 = np.random.random()
        
        sequence = np.zeros(length)
        x = x0
        for i in range(length):
            x = self.r_param * x * (1.0 - x)
            sequence[i] = x
        return sequence

    def generate_chaos_conditioned_policy(self, chaos_state: Optional[np.ndarray] = None, batch_size: int = 1) -> np.ndarray:
        """Generiere Policy-Variante basierend auf Chaos-Zustand [105]"""
        
        # If no chaos state provided, generate one using true math
        if chaos_state is None:
            # Generate chaos for each dimension
            chaos_matrix = np.array([self._generate_logistic_map_sequence(self.chaos_dim) for _ in range(batch_size)])
            chaos_state = chaos_matrix.reshape(batch_size, self.chaos_dim) # [Batch, Dim]
        # Chaos-Features verarbeiten
        chaos_features = self.chaos_processor(chaos_state.reshape(1, -1))
        
        # Noise mit Chaos-Conditioning
        noise = tf.random.normal([batch_size, 100])
        chaos_expanded = tf.repeat(chaos_features, batch_size, axis=0)
        
        # Policy-Generierung
        policy_variant = self.generator([noise, chaos_expanded])
        return policy_variant.numpy()
    
    def adversarial_score(self, policy_variant: np.ndarray) -> float:
        """Berechne Adversarial-Score für Policy-Filtering"""
        discrimination = self.discriminator(policy_variant)
        adversarial_prob = discrimination['adversarial'][0][1].numpy()  # P(adversarial)
        return float(adversarial_prob)
    
    def filter_adversarial_policies(self, policy_variants: np.ndarray) -> np.ndarray:
        """Filtere Policies mit Adversarial-Score > 0.8"""
        valid_policies = []
        for policy in policy_variants:
            if self.adversarial_score(policy) <= self.adversarial_threshold:
                valid_policies.append(policy)
        return np.array(valid_policies)
