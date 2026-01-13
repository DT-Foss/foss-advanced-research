# Hardware Trust Anchor (TPM 2.0 / SGX)

> **Status:** Reference Implementation (Simulation Only)
> **Standard:** TCG TPM 2.0 Profile

## Overview
This module demonstrates **Remote Attestation** using a Trusted Platform Module (TPM). It simulates a "Measured Boot" sequence where every stage of the bootloader chain extends a hash into the TPM's Platform Configuration Registers (PCRs).

## Scientific Core
The security model relies on the **Chain of Trust**:

$$
PCR_{new} = \text{Hash}(PCR_{old} || \text{Hash}(Data))
$$

This operation is irreversible. Remote Attestation allows a server to verify the `PCR_quote` against a known "Golden Policy" to detect rootkits or BIOS creates.

## Visualization
The [tpm_attestation.png](./tpm_attestation.png) chart visualizes a failed integrity check where PCR 09 (Kernel) deviates from the reference value, indicating a potential kernel-level compromise.

## Usage
```bash
python tpm_attestation.py
```
