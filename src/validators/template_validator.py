"""Template rendering validation for COMSOL job generation.

This module provides validation functions to check that Jinja2 templates
render correctly and produce valid Java code that can be compiled by COMSOL.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from ..config.loader import get_logger

logger = get_logger(__name__)


@dataclass
class TemplateValidationError:
    """A single template validation error.

    Attributes:
        error_type: Type of error (e.g., 'long_line', 'syntax_error')
        message: Human-readable error message
        line_number: Line number where error occurred (if applicable)
        line_content: Content of the problematic line
        severity: Error severity ('error', 'warning')
    """
    error_type: str
    message: str
    line_number: Optional[int] = None
    line_content: Optional[str] = None
    severity: str = 'error'


@dataclass
class TemplateValidationResult:
    """Result of template validation.

    Attributes:
        is_valid: Whether the rendered template is valid
        errors: List of validation errors
        warnings: List of validation warnings
    """
    is_valid: bool
    errors: List[TemplateValidationError]
    warnings: List[TemplateValidationError]

    def get_error_summary(self) -> str:
        """Get a formatted summary of all errors and warnings."""
        lines = []
        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            for err in self.errors:
                if err.line_number:
                    lines.append(f"  - Line {err.line_number}: {err.message}")
                else:
                    lines.append(f"  - {err.message}")
        if self.warnings:
            lines.append(f"Warnings ({len(self.warnings)}):")
            for warn in self.warnings:
                if warn.line_number:
                    lines.append(f"  - Line {warn.line_number}: {warn.message}")
                else:
                    lines.append(f"  - {warn.message}")
        return "\n".join(lines)


class JavaCodeValidator:
    """Validator for generated Java code."""

    # Maximum line length for Java code
    MAX_LINE_LENGTH = 120

    # Patterns that might indicate rendering issues (error level)
    ERROR_PATTERNS = [
        (r'\{\s*\{', 'Unrendered Jinja2 variable'),
        (r'\{%', 'Unrendered Jinja2 block'),
    ]

    # Patterns for code quality issues (warning level)
    WARNING_PATTERNS = [
        (r'\s{20,}', 'Excessive whitespace (20+ spaces)'),
    ]

    def __init__(self):
        """Initialize the Java code validator."""
        pass

    def validate_rendered_java(self, java_code: str) -> TemplateValidationResult:
        """Validate rendered Java code.

        Args:
            java_code: The rendered Java code as a string

        Returns:
            TemplateValidationResult with any errors or warnings found
        """
        errors = []
        warnings = []

        lines = java_code.split('\n')

        # Check each line
        for line_num, line in enumerate(lines, start=1):
            # Check line length
            if len(line) > self.MAX_LINE_LENGTH:
                warnings.append(TemplateValidationError(
                    error_type='long_line',
                    message=f'Line exceeds {self.MAX_LINE_LENGTH} characters ({len(line)} chars)',
                    line_number=line_num,
                    line_content=line[:80] + '...' if len(line) > 80 else line,
                    severity='warning'
                ))

            # Check for error patterns
            for pattern, description in self.ERROR_PATTERNS:
                if re.search(pattern, line):
                    # Skip if this looks like a Java array initializer (e.g., {{1,2,3}})
                    # which is valid Java syntax
                    if pattern == r'\{\s*\{' and re.search(r'\{\s*\{[\d\.,\s]+\}', line):
                        continue

                    errors.append(TemplateValidationError(
                        error_type='rendering_error',
                        message=f'{description}',
                        line_number=line_num,
                        line_content=line[:80] + '...' if len(line) > 80 else line,
                        severity='error'
                    ))

            # Check for warning patterns
            for pattern, description in self.WARNING_PATTERNS:
                if re.search(pattern, line):
                    warnings.append(TemplateValidationError(
                        error_type='code_quality',
                        message=f'{description}',
                        line_number=line_num,
                        line_content=line[:80] + '...' if len(line) > 80 else line,
                        severity='warning'
                    ))

        # Check for basic Java syntax issues
        syntax_errors = self._check_basic_syntax(java_code)
        errors.extend(syntax_errors)

        is_valid = len(errors) == 0

        return TemplateValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _check_basic_syntax(self, java_code: str) -> List[TemplateValidationError]:
        """Check for basic Java syntax issues.

        Args:
            java_code: The Java code to check

        Returns:
            List of validation errors found
        """
        errors = []

        # Check brace balance
        open_braces = java_code.count('{')
        close_braces = java_code.count('}')
        if open_braces != close_braces:
            errors.append(TemplateValidationError(
                error_type='brace_mismatch',
                message=f'Mismatched braces: {open_braces} opening, {close_braces} closing',
                severity='error'
            ))

        # Check bracket balance
        open_brackets = java_code.count('[')
        close_brackets = java_code.count(']')
        if open_brackets != close_brackets:
            errors.append(TemplateValidationError(
                error_type='bracket_mismatch',
                message=f'Mismatched brackets: {open_brackets} opening, {close_brackets} closing',
                severity='error'
            ))

        # Check parenthesis balance
        open_parens = java_code.count('(')
        close_parens = java_code.count(')')
        if open_parens != close_parens:
            errors.append(TemplateValidationError(
                error_type='paren_mismatch',
                message=f'Mismatched parentheses: {open_parens} opening, {close_parens} closing',
                severity='error'
            ))

        return errors

    def validate_java_file(self, file_path: Path) -> TemplateValidationResult:
        """Validate a Java file.

        Args:
            file_path: Path to the Java file

        Returns:
            TemplateValidationResult with any errors or warnings found
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                java_code = f.read()
            return self.validate_rendered_java(java_code)
        except Exception as e:
            return TemplateValidationResult(
                is_valid=False,
                errors=[TemplateValidationError(
                    error_type='file_error',
                    message=f'Failed to read file: {e}',
                    severity='error'
                )],
                warnings=[]
            )


def validate_generated_java(java_code: str) -> TemplateValidationResult:
    """Validate generated Java code.

    Convenience function for validating Java code.

    Args:
        java_code: The rendered Java code as a string

    Returns:
        TemplateValidationResult with any errors or warnings found
    """
    validator = JavaCodeValidator()
    return validator.validate_rendered_java(java_code)


def validate_java_file(file_path: Path) -> TemplateValidationResult:
    """Validate a Java file.

    Convenience function for validating a Java file.

    Args:
        file_path: Path to the Java file

    Returns:
        TemplateValidationResult with any errors or warnings found
    """
    validator = JavaCodeValidator()
    return validator.validate_java_file(file_path)
