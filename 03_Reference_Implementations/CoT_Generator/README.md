# Sovereign CoT Generator (MVP)

> **Status**: Reference Implementation v1.0  
> **Concept**: *Pre-Polished Chain-of-Thought Generation for Recursive Self-Improvement*  
> **Author**: David Tom Foss

## 1. System Overview
The **Sovereign CoT Generator** is a specialized pipeline designed to create high-quality, synthetic training data for Large Language Models (LLMs). 
Standard LLMs struggle with complex reasoning because their training data is mostly "Final Answers". This system generates the **"Hidden Thinking Process"** (Chain of Thought - CoT) that leads to the correct answer.

It uses a **Vertical-Specific Architecture**:
*   **Legal Reasoning Module**: IRAC (Issue, Rule, Application, Conclusion) structure.
*   **Medical Diagnostic Module**: Differential Diagnosis steps.
*   **Coding Logic Module**: Psuedocode -> Plan -> Implementation.

## 2. Technical Architecture

### Code Logic (`generator.py`)
The `PrePolishedCoTGenerator` class implements a template-based generation engine:
1.  **Ingest Context**: Takes a raw query (e.g., "Is this contract valid?").
2.  **Select Strategy**: Determines the domain (Legal/Medical/General).
3.  **Expand Reasoning**:
    *   *Step 1*: Deconstruct the prompt.
    *   *Step 2*: Recall relevant knowledge/rules.
    *   *Step 3*: Apply logic step-by-step.
    *   *Step 4*: Synthesize conclusion.
4.  **Polish**: Formats the output into structured Markdown ideal for Fine-Tuning (SFT).

### CLI Wrapper (`cli.py`)
Provides a terminal interface to batch-process prompts, making it easy to generate datasets of 1000s of CoT examples.

## 3. Strategic Novelty vs. SOTA
*   **SOTA (OpenAI o1)**: Uses Reinforcement Learning (RL) to *learn* to think.
*   **Sovereign Approach**: Uses **Synthetic Seeding**. By explicitly programming the "Thinking Structure" for specific verticals (Legal/Med), we can train smaller models (7B/13B) to outperform larger ones on specific tasks without needing massive RL compute.

## 4. Usage

**Generate a Single CoT**:
```bash
python -m cot_generator.cli --prompt "Explain Quantum Entanglement" --domain science
```

**Output format**:
```markdown
# Mental Sandbox
1.  **Analysis**: The user is asking for a definition of Quantum Entanglement.
2.  **Key Concepts**: Wave function, superposition, non-locality.
3.  **Analogy Strategy**: Use the "Spinning Coin" or "Gloves" analogy.
4.  **Drafting**: Start with technical definition, then simplify.

# Final Output
Quantum Entanglement is a physical phenomenon where...
```

## 5. Impact for Portfolio
This codebase serves as the **Data Factory** for the entire Sovereign AI ecosystem. It allows us to create proprietary datasets that no competitor possesses.


---
**© 2025 David Tom Foss // R&D**
### 🔓 Open Innovation Policy
> **"Security through Obscurity is dead."**

This architecture was originally developed as a proprietary IP asset (Patent Pending). However, in light of the accelerating capabilities of AI-driven cyber threats in 2025, **David Tom Foss // R&D** has transitioned to an **Open Source / Reference Implementation** strategy ("Publish Fast" vs "Patent Slow"). 

We believe that critical defense infrastructure must be:
1.  **Transparent**: Auditable by the global security community.
2.  **Standardized**: Establishing de-facto protocols rather than walled gardens.
3.  **Resilient**: Hardened by public scrutiny (Linus's Law).

*This code is released under the MIT License to encourage rapid adoption and fork-based innovation.*
