# Stir — Post-Training Research Extension (Phase F)

Status: Planned, not started. Depends on: working SFT (LoRA fine-tuned Qwen) checkpoint from Phase B.

## Goal
Compare preference optimization methods (DPO vs. KTO) on top of the existing
SFT model, as a research sample for research-career applications.

## Why this pairing
KTO only needs binary good/bad labels — maps naturally onto thumbs up/down
signal a real app would collect. DPO needs chosen/rejected pairs, buildable
from the same underlying labels. Direct, fair comparison on one dataset.

## Steps
1. Build preference data: generate several recipes per pantry from the SFT
   model, label good/bad via checkable rules (ingredients outside pantry,
   missing key pantry items).
2. Train DPO and KTO from the SFT checkpoint, same LoRA + 4-bit setup,
   using TRL's DPOTrainer and KTOTrainer.
3. Evaluate SFT vs. DPO vs. KTO on held-out set:
   - Pantry adherence rate
   - Hallucinated-ingredient rate
   - LLM-as-judge win rate
   - Optional small human rating
4. Write up as 4-6 page LaTeX report + results table + repo README.

## Prerequisite (before writing any training code)
Be able to explain, unprompted, without notes:
- Why DPO's loss is derived the way it is (the implicit reward formulation)
- What KTO borrows from prospect theory, and why it doesn't need pairs
- Where the two methods would diverge in practice, and a guess as to which
  one wins on THIS task before running the experiment
  