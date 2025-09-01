
 QLoRA Log Explainer (Qwen2.5-7B-Instruct)

A fine-tuned QLoRA model that automatically explains complex logs with clear “Cause + Fix” outputs, reducing debugging time for developers.



## Project Highlights

1. **Problem Statement:** Developers often waste time interpreting cryptic logs; this project fine-tunes a large language model (LLM) to give quick **Cause + Fix** summaries.

2. **Base Model:** Used **Qwen/Qwen2.5-7B-Instruct**, optimized with **QLoRA (LoRA + 4-bit quantization)** to run efficiently on a single Colab GPU.

3. **Dataset:** Collected/synthesized log lines paired with human-written explanations and fixes, stored in CSV format (`instruction,input,output`).

4. **Prompt Template:** Enforced a strict and predictable output:

   ```
   Cause:
   <2–3 lines>
   Fix:
   <1 line>
   ```

5. **Training Setup:**

   * Hugging Face **Transformers + TRL + PEFT + bitsandbytes**
   * Effective batch size: 8 (grad accumulation)
   * Trained for 1–3 epochs with learning rate 2e-4

6. **Adapter Saving:** Only the **LoRA adapters + tokenizer** (\~150MB) were saved; the 7B base is loaded from Hugging Face at runtime.

7. **Evaluation:**

   * Validation loss reduced from **0.94 → 0.60**
   * Perplexity dropped from **2.56 → 1.82**
   * Confirmed the model generalizes beyond training samples.

8. **Inference Pipeline:** Added a `test_model()` helper that:

   * Takes any log line
   * Builds the prompt
   * Runs `model.generate()`
   * Returns a clean, single **Cause + Fix** block.

9. **Results:** On unseen logs, the model consistently explains the error in 2–3 lines and proposes a concise, actionable fix in 1 line.

10. **Tech Stack:**
    Python, PyTorch, Hugging Face Transformers, TRL, PEFT, bitsandbytes, QLoRA, Colab, Qwen2.5-7B-Instruct.

