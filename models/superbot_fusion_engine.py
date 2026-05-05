"""Superbot Fusion Engine - Combines multiple quotes into cohesive superbots.

Takes 2+ quotes from different themes and creates new 'superbots' that:
- Combine the logic from multiple quotes
- Create new insights by merging themes
- Apply same linguistic devices
- Work across all registers
- Include resilience (drift, decay, failsafe, restore)
"""

import json
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class FusionStrategy(Enum):
    """How to combine quotes."""
    LINEAR = "linear"  # Quote A then Quote B
    NESTED = "nested"  # Quote A inside Quote B's logic
    PARALLEL = "parallel"  # Both quotes run together
    CONTRAST = "contrast"  # Quote A vs Quote B
    SYNTHESIS = "synthesis"  # New insight from both
    CYCLE = "cycle"  # Quote A → Quote B → Quote A
    RECURSIVE = "recursive"  # Quote contains itself with new layer


class ThemeType(Enum):
    """Quote themes."""
    SOLITUDE = "solitude"
    DISCOMFORT = "discomfort"
    SYSTEMS = "systems"
    HOME = "home"
    POSITIVITY = "positivity"
    FEEDBACK = "feedback"
    OBSERVATION = "observation"
    PLANNING = "planning"


@dataclass
class QuoteSource:
    """A single source quote."""
    text: str
    theme: ThemeType
    register: str
    quote_type: str  # COMPLETE, SUMMARY, HYPERBOLE, etc
    code: str
    linguistic_devices: List[str]
    key_concepts: List[str]


@dataclass
class SuperbotFusion:
    """A combined superbot quote."""
    id: str
    strategy: FusionStrategy
    source_codes: List[str]  # Which quotes were combined
    themes: List[ThemeType]  # What themes it covers
    content: str  # The actual combined quote
    register: str  # Which style it uses
    linguistic_devices: List[str]  # Techniques used
    key_concepts: List[str]  # Main ideas
    logic_flow: str  # How it connects the quotes
    fusion_score: float  # Quality 0-1
    created_at: str
    
    # Resilience
    drift_score: float = 0.0
    decay_level: float = 1.0
    failsafe_status: str = "NORMAL"
    checkpoint_hash: str = ""


class SuperbotFusionEngine:
    """Creates superbots by combining multiple quotes."""
    
    def __init__(self):
        self.quotes_cache = {}
        self.superbots = []
        self.checkpoints = []
    
    def fuse_quotes(self, 
                   quote1: QuoteSource, 
                   quote2: QuoteSource,
                   strategy: FusionStrategy = FusionStrategy.SYNTHESIS,
                   register: Optional[str] = None) -> SuperbotFusion:
        """Combine two quotes into one superbot.
        
        Args:
            quote1: First source quote
            quote2: Second source quote
            strategy: How to combine them
            register: Output style (if None, use quote1's register)
            
        Returns:
            SuperbotFusion: The combined quote
        """
        register = register or quote1.register
        
        # Create the fused content based on strategy
        if strategy == FusionStrategy.LINEAR:
            content = self._fuse_linear(quote1, quote2, register)
        elif strategy == FusionStrategy.NESTED:
            content = self._fuse_nested(quote1, quote2, register)
        elif strategy == FusionStrategy.PARALLEL:
            content = self._fuse_parallel(quote1, quote2, register)
        elif strategy == FusionStrategy.CONTRAST:
            content = self._fuse_contrast(quote1, quote2, register)
        elif strategy == FusionStrategy.SYNTHESIS:
            content = self._fuse_synthesis(quote1, quote2, register)
        elif strategy == FusionStrategy.CYCLE:
            content = self._fuse_cycle(quote1, quote2, register)
        elif strategy == FusionStrategy.RECURSIVE:
            content = self._fuse_recursive(quote1, quote2, register)
        else:
            content = self._fuse_synthesis(quote1, quote2, register)
        
        # Combine linguistic devices
        devices = list(set(quote1.linguistic_devices + quote2.linguistic_devices))
        
        # Combine concepts
        concepts = list(set(quote1.key_concepts + quote2.key_concepts))
        
        # Calculate fusion score (0-1 based on coherence)
        fusion_score = self._calculate_fusion_score(quote1, quote2, strategy)
        
        # Create superbot
        superbot = SuperbotFusion(
            id=self._generate_id(quote1, quote2, strategy),
            strategy=strategy,
            source_codes=[quote1.code, quote2.code],
            themes=[quote1.theme, quote2.theme],
            content=content,
            register=register,
            linguistic_devices=devices,
            key_concepts=concepts,
            logic_flow=self._describe_logic(quote1, quote2, strategy),
            fusion_score=fusion_score,
            created_at=datetime.now().isoformat(),
            checkpoint_hash=self._create_checkpoint(content)
        )
        
        self.superbots.append(superbot)
        return superbot
    
    def fuse_multiple(self,
                     quotes: List[QuoteSource],
                     strategy: FusionStrategy = FusionStrategy.SYNTHESIS) -> SuperbotFusion:
        """Combine 3+ quotes into one superbot.
        
        Combines quotes iteratively: (quote1 + quote2) + quote3, etc.
        """
        if len(quotes) < 2:
            raise ValueError("Need at least 2 quotes to fuse")
        
        # Start with first two
        result_quote = quotes[0]
        for i in range(1, len(quotes)):
            fused = self.fuse_quotes(result_quote, quotes[i], strategy)
            # Convert back to QuoteSource for next iteration
            result_quote = QuoteSource(
                text=fused.content,
                theme=quotes[i].theme,  # Use latest theme
                register=fused.register,
                quote_type="FUSED",
                code=fused.id,
                linguistic_devices=fused.linguistic_devices,
                key_concepts=fused.key_concepts
            )
        
        return fused
    
    # === FUSION STRATEGIES ===
    
    def _fuse_linear(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """LINEAR: Quote A then Quote B."""
        return f"{q1.text} And then, {q2.text}"
    
    def _fuse_nested(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """NESTED: Quote A's logic inside Quote B."""
        return f"{q2.text} Because {q1.text.lower()}"
    
    def _fuse_parallel(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """PARALLEL: Both quotes at once."""
        return f"{q1.text} At the same time, {q2.text}"
    
    def _fuse_contrast(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """CONTRAST: Quote A vs Quote B."""
        return f"On one hand, {q1.text.lower()} On the other hand, {q2.text.lower()}"
    
    def _fuse_synthesis(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """SYNTHESIS: Create new insight combining both."""
        # Extract key insight from each
        concepts_1 = " and ".join(q1.key_concepts[:2])
        concepts_2 = " and ".join(q2.key_concepts[:2])
        return f"When you combine {concepts_1} with {concepts_2}, you discover something powerful. {q1.text.lower()} This means {q2.text.lower()}"
    
    def _fuse_cycle(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """CYCLE: Quote A → Quote B → Quote A (circular logic)."""
        return f"{q1.text} This leads to {q2.text.lower()} Which brings you back to: {q1.text.lower()}"
    
    def _fuse_recursive(self, q1: QuoteSource, q2: QuoteSource, register: str) -> str:
        """RECURSIVE: Quote contains itself with new layer."""
        return f"{q1.text} But here's the deeper part: {q2.text} And this applies to everything in {q1.text.lower()}"
    
    # === UTILITIES ===
    
    def _calculate_fusion_score(self, q1: QuoteSource, q2: QuoteSource, 
                                strategy: FusionStrategy) -> float:
        """Score how well two quotes combine (0-1).
        
        Higher score = better fit.
        - Same theme: +0.3
        - Shared concepts: +0.2 per concept
        - Same register: +0.2
        - Different themes (good contrast): +0.1
        """
        score = 0.5  # baseline
        
        # Theme similarity
        if q1.theme == q2.theme:
            score += 0.3
        elif strategy in [FusionStrategy.CONTRAST, FusionStrategy.SYNTHESIS]:
            score += 0.15  # Different themes work well for contrast/synthesis
        
        # Concept overlap
        overlap = set(q1.key_concepts) & set(q2.key_concepts)
        score += len(overlap) * 0.05
        
        # Register match
        if q1.register == q2.register:
            score += 0.2
        
        # Strategy fit
        if strategy in [FusionStrategy.SYNTHESIS, FusionStrategy.CONTRAST]:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _describe_logic(self, q1: QuoteSource, q2: QuoteSource, 
                       strategy: FusionStrategy) -> str:
        """Describe how the quotes connect."""
        mappings = {
            FusionStrategy.LINEAR: f"Sequential: {q1.theme.value} → {q2.theme.value}",
            FusionStrategy.NESTED: f"Dependent: {q1.theme.value} explains {q2.theme.value}",
            FusionStrategy.PARALLEL: f"Concurrent: {q1.theme.value} + {q2.theme.value} happen together",
            FusionStrategy.CONTRAST: f"Antithetical: {q1.theme.value} vs {q2.theme.value}",
            FusionStrategy.SYNTHESIS: f"Integrated: {q1.theme.value} + {q2.theme.value} = new insight",
            FusionStrategy.CYCLE: f"Circular: {q1.theme.value} ↔ {q2.theme.value} ↔ {q1.theme.value}",
            FusionStrategy.RECURSIVE: f"Layered: {q1.theme.value} contains {q2.theme.value}",
        }
        return mappings.get(strategy, "Unknown logic")
    
    def _generate_id(self, q1: QuoteSource, q2: QuoteSource, 
                    strategy: FusionStrategy) -> str:
        """Create unique ID for superbot."""
        combined = f"{q1.code}_{q2.code}_{strategy.value}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    def _create_checkpoint(self, content: str) -> str:
        """Create hash checkpoint for resilience."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def export_superbot(self, superbot: SuperbotFusion) -> Dict:
        """Export superbot as dictionary."""
        return {
            **asdict(superbot),
            "strategy": superbot.strategy.value,
            "themes": [t.value for t in superbot.themes]
        }
    
    def export_all_superbots(self) -> List[Dict]:
        """Export all superbots."""
        return [self.export_superbot(sb) for sb in self.superbots]


# === EXAMPLES ===

if __name__ == "__main__":
    engine = SuperbotFusionEngine()
    
    # Define two source quotes
    quote_solitude = QuoteSource(
        text="Solitude is where you develop healthy practices and build independence.",
        theme=ThemeType.SOLITUDE,
        register="EN_CORE_PHILOSOPHY",
        quote_type="COMPLETE",
        code="AB_SOLITUDE_COMPLETE_EN",
        linguistic_devices=["metaphor", "antithesis"],
        key_concepts=["solitude", "independence", "practices"]
    )
    
    quote_discomfort = QuoteSource(
        text="Discomfort tells you something needs to change; it's a gift that guides you.",
        theme=ThemeType.DISCOMFORT,
        register="EN_CORE_PHILOSOPHY",
        quote_type="COMPLETE",
        code="AB_DISCOMFORT_COMPLETE_EN",
        linguistic_devices=["paradox", "personification"],
        key_concepts=["discomfort", "awareness", "growth"]
    )
    
    # Create superbots using different strategies
    print("\n" + "="*70)
    print("SUPERBOT FUSION EXAMPLES")
    print("="*70)
    
    for strategy in FusionStrategy:
        superbot = engine.fuse_quotes(quote_solitude, quote_discomfort, strategy)
        print(f"\n🤖 Strategy: {strategy.value.upper()}")
        print(f"📌 Themes: {[t.value for t in superbot.themes]}")
        print(f"💬 Content:\n{superbot.content}")
        print(f"📊 Fusion Score: {superbot.fusion_score:.2f}")
        print(f"🔗 Logic Flow: {superbot.logic_flow}")
        print(f"🛡️  Failsafe: {superbot.failsafe_status}")
        print("-" * 70)
