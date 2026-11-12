import re
import numpy as np
import pandas as pd
import spacy

# Load English NLP pipeline
# Setup: pip install spacy pandas numpy && python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# Model Anchor Lexicon defined in Ph.D. Proposal (Section 3, Phase I)
MODEL_ANCHORS = [
    "crucially",
    "indeed",
    "defining hallmark",
    "testament to",
    "tapestry",
    "delve",
    "paramount",
    "landscape",
    "underscores",
    "moreover",
    "furthermore",
]

# Sample texts mapped to the Five-Stage Taxonomy
taxonomy_samples = {
    "Stage 1 (Completely AI)": (
        "Crucially, the evolution of digital journalism is a defining hallmark"
        " of the modern information landscape. Indeed, as artificial"
        " intelligence continues to reshape media ecosystems, it is paramount"
        " that organizations delve into robust governance frameworks."
        " Moreover, this transformation underscores the intricate tapestry of"
        " technological innovation and public trust."
    ),
    "Stage 3 (Human + Light AI Edit)": (
        "Digital journalism faces unprecedented structural shifts as generative"
        " models enter daily newsrooms. While automated tools can assist with"
        " basic copy-editing, editors must maintain strict oversight over"
        " source verification. Without human accountability, public trust in"
        " established broadsheets will steadily erode."
    ),
    "Stage 5 (Organic Human)": (
        "Every evening before the print edition locks, sub-editors confront a"
        " silent flood of synthetic press copy. Machine-generated paragraphs"
        " read smoothly on the surface, yet they strip away the local"
        " etymological grit and hard-won sourcing that give investigative"
        " reporting its civic teeth."
    ),
}


def run_forensic_audit(text):
  doc = nlp(text)
  words = [token.text.lower() for token in doc if token.is_alpha]
  total_words = len(words)

  # 1. Lexical Diversity (Type-Token Ratio)
  ttr = len(set(words)) / total_words if total_words > 0 else 0

  # 2. Structural Entropy (Sentence Length Variance / Standard Deviation)
  sent_lengths = [
      len([t for t in sent if t.is_alpha]) for sent in doc.sents
  ]
  sentence_variance = np.std(sent_lengths) if sent_lengths else 0

  # 3. Model Anchor Frequency (per 100 words)
  text_lower = text.lower()
  anchor_hits = sum(
      len(re.findall(r"\b" + re.escape(anchor) + r"\b", text_lower))
      for anchor in MODEL_ANCHORS
  )
  anchor_density = (anchor_hits / total_words) * 100 if total_words > 0 else 0

  return {
      "Word Count": total_words,
      "Lexical Diversity (TTR)": round(ttr, 3),
      "Structural Entropy (Sent SD)": round(sentence_variance, 2),
      "Model Anchor Hits": anchor_hits,
      "Anchor Density (%)": round(anchor_density, 2),
  }


if __name__ == "__main__":
  audit_results = {
      stage: run_forensic_audit(sample)
      for stage, sample in taxonomy_samples.items()
  }
  df = pd.DataFrame(audit_results).T
  print("\n=== CONTENT PROVENANCE FORENSIC AUDIT ===\n")
  print(df.to_string())

