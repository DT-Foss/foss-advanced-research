import numpy as np
import base64
import json

class RingLWESimulator:
    """
    Didactic Simulator for Ring-LWE (Learning With Errors over Rings).
    The foundation of modern FHE schemes (BGV, BFV, CKKS).
    
    Parameters:
        n (int): Polynomial degree (power of 2)
        q (int): Modulus
        sigma (float): Noise standard deviation
    
    Ring: R_q = Z_q[x] / (x^n + 1)
    """
    def __init__(self, n=256, q=3329, sigma=3.0):
        self.n = n
        self.q = q
        self.sigma = sigma
    
    def _poly_add(self, p1, p2):
        """Add two polynomials in Z_q[x]"""
        return (p1 + p2) % self.q
        
    def _poly_mul(self, p1, p2):
        """
        Multiply two polynomials in R_q.
        Multiplication modulo (x^n + 1).
        Slow O(n^2) convolution for demonstration (FFT would be O(n log n)).
        """
        # Linear convolution
        res = np.zeros(2 * self.n, dtype=int)
        for i in range(self.n):
            for j in range(self.n):
                res[i + j] += p1[i] * p2[j]
        
        # Reduction modulo x^n + 1
        # x^n = -1, x^(n+1) = -x, etc.
        # res[k] maps to res[k] for k < n
        # res[n+k] maps to -res[k]
        out = np.zeros(self.n, dtype=int)
        for i in range(2 * self.n):
            idx = i % self.n
            sign = -1 if (i // self.n) % 2 == 1 else 1
            out[idx] += sign * res[i]
            
        return out % self.q

    def sample_poly_uniform(self):
        """Sample polynomial with coefficients uniform in [0, q-1]"""
        return np.random.randint(0, self.q, size=self.n)
        
    def sample_poly_noise(self):
        """Sample small error polynomial from Gaussian distribution"""
        noise = np.random.normal(0, self.sigma, size=self.n).astype(int)
        return noise % self.q

    def keygen(self):
        """
        Generate (SecretKey, PublicKey) pair.
        s <- DiscreteGaussian (or Ternary)
        A <- Uniform(R_q)
        e <- DiscreteGaussian
        b = -A*s + e
        pk = (b, A)
        sk = s
        """
        s = self.sample_poly_noise() # Simplified secret key (usually ternary)
        A = self.sample_poly_uniform()
        e = self.sample_poly_noise()
        
        # Calculate b = -A*s + e
        # Negate A
        neg_A = self._poly_mul(A, np.full(self.n, -1))
        As = self._poly_mul(neg_A, s)
        b = self._poly_add(As, e)
        
        return s, (b, A)

class WASMPolyglotContainer:
    """
    WASM Container that acts as a secure enclave using FHE interfaces.
    """
    def __init__(self):
        print("Initializing WASM Polyglot Container with Ring-LWE Crypto Core...")
        self.lwe_sim = RingLWESimulator(n=128, q=1024) # Small params for demo speed
        self.sk, self.pk = self.lwe_sim.keygen()
        print("✅ Ring-LWE Keypair Generated.")
        
    def get_public_key_json(self):
        b, A = self.pk
        return json.dumps({
            "b": b.tolist()[:10], # Truncated for display
            "A": A.tolist()[:10],
            "param_n": self.lwe_sim.n,
            "note": "Truncated for display"
        })

if __name__ == "__main__":
    container = WASMPolyglotContainer()
    print(f"Public Key Fragment: {container.get_public_key_json()}")
