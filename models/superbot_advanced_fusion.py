"""Advanced Superbot Fusion - Multi-quote combinations with smart logic.

Builds on basic fusion with:
- Semantic coherence checking
- Automatic strategy selection
- Cross-theme pattern detection
- Quality scoring
- Resilience integration
"""

import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CoherenceLevel(Enum):
    """How well quotes fit together."""
    POOR = 0.0
    WEAK = 0.3
    MODERATE = 0.6
    GOOD = 0.8
    EXCELLENT = 0.95


class SuperbotAdvancedFusion:
    """Smart superbot creation with semantic coherence."""
    
    def __init__(self):
        self.theme_adjacencies = self._build_theme_graph()
        self.concept_relationships = self._build_concept_graph()
    
    def _build_theme_graph(self) -> Dict[str, List[Tuple[str, float]]]:
        """Define which themes connect well together.
        
        Returns:
            Dict mapping theme → [(connected_theme, compatibility_score), ...]
        """
        return {
            "solitude": [
                ("home", 0.95),
                ("observation", 0.90),
                ("systems", 0.85),
                ("discomfort", 0.80),
                ("feedback", 0.75),
                ("planning", 0.85),
                ("positivity", 0.70),
            ],
            "discomfort": [
                ("growth", 0.95),
                ("feedback", 0.90),
                ("observation", 0.85),
                ("solitude", 0.80),
                ("planning", 0.75),
                ("systems", 0.70),
                ("home", 0.80),
            ],
            "systems": [
                ("routine", 0.95),
                ("feedback", 0.90),
                ("home", 0.85),
                ("planning", 0.85),
                ("solitude", 0.75),
                ("observation", 0.80),
            ],
            "home": [
                ("solitude", 0.95),
                ("planning", 0.90),
                ("feedback", 0.85),
                ("positivity", 0.85),
                ("systems", 0.80),
                ("observation", 0.75),
            ],
            "feedback": [
                ("systems", 0.90),
                ("observation", 0.90),
                ("discomfort", 0.85),
                ("planning", 0.85),
                ("solitude", 0.75),
                ("growth", 0.85),
            ],
            "planning": [
                ("home", 0.90),
                ("systems", 0.85),
                ("observation", 0.85),
                ("feedback", 0.80),
                ("solitude", 0.80),
                ("positivity", 0.75),
            ],
            "observation": [
                ("feedback", 0.90),
                ("planning", 0.85),
                ("solitude", 0.85),
                ("systems", 0.80),
                ("intuition", 0.90),
                ("safety", 0.85),
            ],
            "positivity": [
                ("routine", 0.95),
                ("home", 0.85),
                ("solitude", 0.70),
                ("planning", 0.75),
                ("observation", 0.70),
            ],
        }
    
    def _build_concept_graph(self) -> Dict[str, List[Tuple[str, float]]]:
        """Define which concepts naturally connect.
        
        Returns:
            Dict mapping concept → [(related_concept, relationship_strength), ...]
        """
        return {
            "independence": [
                ("self-trust", 0.95),
                ("solitude", 0.90),
                ("resilience", 0.90),
                ("growth", 0.85),
                ("discomfort", 0.80),
            ],
            "routine": [
                ("structure", 0.95),
                ("consistency", 0.90),
                ("systems", 0.85),
                ("discipline", 0.90),
                ("energy", 0.80),
            ],
            "feedback": [
                ("awareness", 0.95),
                ("growth", 0.90),
                ("observation", 0.85),
                ("decision-making", 0.85),
                ("connection", 0.80),
            ],
            "home": [
                ("foundation", 0.95),
                ("safety", 0.90),
                ("reset", 0.90),
                ("clarity", 0.85),
                ("belonging", 0.85),
            ],
            "discomfort": [
                ("signal", 0.95),
                ("awareness", 0.90),
                ("growth", 0.95),
                ("change", 0.90),
                ("decision", 0.85),
            ],
            "observation": [
                ("awareness", 0.90),
                ("intuition", 0.90),
                ("planning", 0.85),
                ("safety", 0.85),
                ("clarity", 0.80),
            ],
        }
    
    def calculate_compatibility(self, themes: List[str]) -> float:
        """Rate how well multiple themes work together (0-1).
        
        Args:
            themes: List of theme strings
            
        Returns:
            Compatibility score 0-1
        """
        if len(themes) < 2:
            return 1.0
        
        scores = []
        for i, theme1 in enumerate(themes):
            for theme2 in themes[i+1:]:
                # Find adjacency
                if theme1 in self.theme_adjacencies:
                    connections = {t: score for t, score in self.theme_adjacencies[theme1]}
                    score = connections.get(theme2, 0.5)
                    scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def calculate_concept_coherence(self, concepts: List[str]) -> float:
        """Rate how coherent a set of concepts is (0-1)."""
        if len(concepts) < 2:
            return 1.0
        
        scores = []
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                if concept1 in self.concept_relationships:
                    related = {c: score for c, score in self.concept_relationships[concept1]}
                    score = related.get(concept2, 0.5)
                    scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def suggest_fusion_strategy(self, themes: List[str], 
                               quote_types: List[str]) -> str:
        """Recommend best fusion strategy for given themes.
        
        Args:
            themes: List of theme names
            quote_types: List of quote types (COMPLETE, SUMMARY, etc)
            
        Returns:
            Recommended strategy name
        """
        num_themes = len(themes)
        num_summaries = quote_types.count("SUMMARY")
        
        # Logic for strategy selection
        if num_themes == 2:
            if "discomfort" in themes and "solitude" in themes:
                return "SYNTHESIS"  # Growth cycle
            elif "home" in themes and "planning" in themes:
                return "PARALLEL"  # Both happen together
            elif "feedback" in themes:
                return "NESTED"  # Feedback explains other
            else:
                return "CONTRAST"
        
        elif num_themes == 3:
            if "home" in themes or "solitude" in themes:
                return "RECURSIVE"  # Spiral pattern
            else:
                return "SYNTHESIS"
        
        elif num_themes >= 4:
            return "RECURSIVE"  # Full lifecycle pattern
        
        return "SYNTHESIS"  # Default
    
    def generate_superbot_description(self, 
                                     themes: List[str],
                                     concepts: List[str]) -> str:
        """Auto-generate a descriptive name for the superbot."""
        # Simple name generation
        theme_names = " + ".join([t.replace("_", " ").title() for t in themes[:3]])
        if len(themes) > 3:
            theme_names += f" + {len(themes)-3} more"
        
        key_concept = concepts[0].replace("_", " ").title() if concepts else "Wisdom"
        return f"{key_concept} Through {theme_names}"


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    fusion = SuperbotAdvancedFusion()
    
    # Test 1: Theme compatibility
    themes = ["solitude", "discomfort", "feedback"]
    compat = fusion.calculate_compatibility(themes)
    print(f"Theme compatibility: {compat:.2f}")
    
    # Test 2: Concept coherence
    concepts = ["independence", "resilience", "growth", "awareness"]
    coherence = fusion.calculate_concept_coherence(concepts)
    print(f"Concept coherence: {coherence:.2f}")
    
    # Test 3: Strategy suggestion
    strategy = fusion.suggest_fusion_strategy(themes, ["COMPLETE", "COMPLETE", "COMPLETE"])
    print(f"Suggested strategy: {strategy}")
    
    # Test 4: Description generation
    desc = fusion.generate_superbot_description(themes, concepts)
    print(f"Superbot name: {desc}")
