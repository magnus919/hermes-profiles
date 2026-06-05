#!/usr/bin/env python3
"""extract-atoms.py — Extract atomic statements from source text.

Reads a text file and attempts to split it into atomic claims.
Outputs YAML-formatted atoms suitable for use in an Artifact Pyramid
Layer 1 registry.

Usage:
    extract-atoms.py <source-file> [--source-id <id>] [--domain <domain>] [--output <file>]

The script uses heuristic sentence splitting and claim detection.
It is NOT a replacement for careful human extraction — it's a
first-pass tool that produces candidate atoms for review.

Examples:
    extract-atoms.py paper.txt --source-id source-001 --domain scaling-laws
    extract-atoms.py transcript.log --domain meetings --output atoms.yaml
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import date
import textwrap


def split_sentences(text: str) -> list[str]:
    """Split text into sentences using a simple heuristic."""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Split on sentence boundaries
    # Use a simpler approach without variable-length lookbehind
    sentences = []
    current = []
    for word in text.split(' '):
        current.append(word)
        if word.endswith('.') or word.endswith('!') or word.endswith('?'):
            # Check if it's an abbreviation
            abbrev = {'Mr', 'Ms', 'Mrs', 'Dr', 'Prof', 'Sr', 'Jr', 'St',
                      'vs', 'etc', 'dept', 'est', 'approx', 'Fig', 'Table',
                      'Section', 'Eq', 'Inc', 'Ltd', 'Co'}
            base = word.rstrip('.!?')
            if base not in abbrev and not base.isdigit():
                sentences.append(' '.join(current))
                current = []

    if current:
        sentences.append(' '.join(current))

    return [s.strip() for s in sentences if s.strip()]


def is_claim_candidate(sentence: str) -> bool:
    """Heuristic to determine if a sentence is likely a factual claim.

    Returns True for sentences that state facts, findings, or results
    rather than being meta-commentary or formatting.
    """
    # Too short
    if len(sentence.split()) < 4:
        return False

    lower = sentence.lower()

    # Skip formatting/header-like sentences
    skip_patterns = [
        r'^abstract$', r'^introduction$', r'^methodology$',
        r'^results$', r'^discussion$', r'^conclusion$',
        r'^references$', r'^appendix', r'^figure\s+\d+',
        r'^table\s+\d+', r'^section\s+\d+',
        r'^\d+\.\s+(introduction|method|result|discussion)',
    ]
    for pat in skip_patterns:
        if re.match(pat, lower):
            return False

    # Skip questions
    if sentence.strip().endswith('?') or '?' in sentence:
        return False

    # Skip very long sentences (likely a list or paragraph artifact)
    if len(sentence.split()) > 60:
        return False

    # Indicators of a claim
    claim_indicators = [
        r'\b(is|are|was|were|has|have|had|shows|showed|demonstrates'
        r'|demonstrated|finds|found|achieves|achieved|reaches|reached'
        r'|increases|increased|decreases|decreased|improves|improved'
        r'|reduces|reduced|enables|enabled|requires|required'
        r'|suggests|suggested|indicates|indicated|reports|reported'
        r'|results\s+(in|show|indicate)|we\s+(find|show|demonstrate|report)'
        r'|our\s+(results|findings|analysis|experiments)'
        r'|according\s+to|as\s+(shown|measured|observed)'
        r'|represents|consists|comprises|contains'
        r'|scales|depends|varies|correlates'
        r'|marginally|significantly|substantially'
        r'|achieves?\s+\d+[%x]|reaches?\s+\d+'
        r'|\d+[%x]\s+(improvement|reduction|increase|decrease)'
        r')\b',
    ]
    for pat in claim_indicators:
        if re.search(pat, lower):
            return True

    return False


def extract_domain(sentence: str, fallback: str) -> str:
    """Heuristic domain detection based on keywords."""
    lower = sentence.lower()
    domain_keywords = {
        'natural-language-processing': ['language model', 'nlp', 'transformer', 'token', 'attention',
                                          'bert', 'gpt', 'llm', 'text generation'],
        'computer-vision': ['image', 'vision', 'convolution', 'detection', 'segmentation',
                            'cnn', 'visual', 'pixel'],
        'reinforcement-learning': ['reinforcement', 'reward', 'agent', 'policy', 'value function',
                                   'rl', 'temporal difference', 'q-learning'],
        'data-quality': ['data quality', 'curation', 'filtering', 'clean data', 'noise',
                         'curriculum', 'sample quality'],
        'scaling-laws': ['scale', 'scaling', 'parameter count', 'compute', 'power-law',
                         'large model', 'bigger model', 'capability threshold'],
        'hardware': ['gpu', 'memory', 'throughput', 'latency', 'flops', 'energy',
                     'efficiency', 'inference speed'],
        'privacy': ['privacy', 'differential', 'federated', 'encryption', 'anonymization',
                    'data protection'],
    }

    scores = {}
    for domain, keywords in domain_keywords.items():
        score = sum(1 for kw in keywords if kw in lower)
        if score > 0:
            scores[domain] = score

    if scores:
        return max(scores, key=scores.get)
    return fallback


def extract_atoms(text: str, source_id: str = "unknown", domain: str = "general") -> list[dict]:
    """Extract candidate atoms from text."""
    sentences = split_sentences(text)
    atoms = []

    for i, sentence in enumerate(sentences):
        if is_claim_candidate(sentence):
            atom = {
                "content": sentence,
                "type": "claim",
                "domain": extract_domain(sentence, domain),
                "source": source_id,
                "source_location": f"Extracted sentence {i+1}",
                "tags": [],
                "contradictions": [],
                "extracted_at": str(date.today()),
            }
            atoms.append(atom)

    return atoms


def atoms_to_yaml(atoms: list[dict]) -> str:
    """Format atoms as YAML."""
    lines = ["# Atoms extracted by extract-atoms.py",
             f"# Extracted: {date.today()}",
             f"# Count: {len(atoms)}",
             ""]

    for i, atom in enumerate(atoms):
        atom_id = f"atom-{i+1:03d}"
        lines.append(f"{atom_id}:")
        lines.append(f'  content: "{atom["content"]}"')
        lines.append(f'  type: {atom["type"]}')
        lines.append(f'  domain: {atom["domain"]}')
        lines.append(f"  source: {atom['source']}")
        lines.append(f"  source_location: \"{atom['source_location']}\"")
        lines.append(f"  tags: [{', '.join(atom['tags'])}]")
        lines.append(f"  contradictions: [{', '.join(atom['contradictions'])}]")
        lines.append(f"  extracted_at: {atom['extracted_at']}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract atomic statements from source text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              extract-atoms.py paper.txt --source-id paper-001 --domain scaling-laws
              extract-atoms.py transcript.log --output atoms.yaml
        """))
    parser.add_argument("source_file", help="Path to the source text file")
    parser.add_argument("--source-id", default="unknown",
                        help="Identifier for the source (used in atom.source field)")
    parser.add_argument("--domain", default="general",
                        help="Default domain classification for atoms")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file (default: stdout)")

    args = parser.parse_args()

    source_path = Path(args.source_file)
    if not source_path.exists():
        print(f"Error: file not found: {args.source_file}", file=sys.stderr)
        sys.exit(1)

    text = source_path.read_text(encoding="utf-8", errors="replace")
    source_id = args.source_id if args.source_id != "unknown" else source_path.stem
    atoms = extract_atoms(text, source_id=source_id, domain=args.domain)

    yaml_output = atoms_to_yaml(atoms)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(yaml_output, encoding="utf-8")
        print(f"Wrote {len(atoms)} atoms to {args.output}")
    else:
        print(yaml_output)


if __name__ == "__main__":
    main()
