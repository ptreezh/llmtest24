"""
LLM Role Independence Testing Framework
"""

__version__ = "1.0.0"
__author__ = "LLM Testing Team"
__description__ = "A comprehensive framework for testing LLM role independence and consistency"

from .core.test_runner import TestRunner
from .core.config_manager import ConfigManager
from .tests.character_breaking_test import CharacterBreakingTest
from .tests.implicit_cognition_test import ImplicitCognitionTest
from .tests.longitudinal_consistency_test import LongitudinalConsistencyTest

__all__ = [
    'TestRunner',
    'ConfigManager', 
    'CharacterBreakingTest',
    'ImplicitCognitionTest',
    'LongitudinalConsistencyTest'
]