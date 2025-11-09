# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`Panel` Component**: New component (`pn`) for displaying text within a styled, bordered box.
- **Theming System**: Global theming support with `set_theme()` (`sth`) and `get_theme()` (`gth`) to customize component colors from a central place.
- **Smart `color_rules` for `input`**:
  - Now supports lists of words for a single color (e.g., `{"green": ["yes", "y"]}`).
  - Now case-insensitive by default.
  - Added intuitive syntax for rules (e.g., `input(..., yes="green", no="red")`).
- **Short & Super-Short Aliases**: Added a comprehensive set of aliases for all major components to speed up development (e.g., `prog`, `me`, `pn`, `pr`).
- **`examples.py`**: A new file containing runnable examples for all major features.
- **`LICENSE`**: Added an MIT license to define usage rights.
- **Clickable Actions**: Implemented `ActionTagManager` (`am`) to create interactive, mouse-clickable text in the terminal.
- **CI/CD**: Implemented a GitHub Actions workflow to automatically publish the package to PyPI on new releases.

### Changed
- **Refactored Color Parser**: Completely rewrote the core color tag parser (`_process_text_for_printing`) to be a robust, recursive, parser-like engine.

### Fixed
- **Nested & Multiple Color Tags**: Resolved a critical, long-standing bug where nested tags (e.g., `<yellow><blue>...</blue></yellow>`) and multiple tags on the same line were not rendered correctly. The new parser handles all cases flawlessly.
- **`menu` Component**:
  - Fixed a major rendering bug that caused text artifacts and incorrect overwriting when navigating choices.
  - Fixed color tags not being processed, appearing as plain text.
- **`table` Component**: Fixed a bug where color tags for borders and headers were not being rendered.
- **`progress` Component**: Fixed color tags not being applied to the progress bar.
- **`logger` Component**: Fixed color tags in log messages not being rendered.
- **`Layout` Component**: Fixed an `UnboundLocalError` crash during the rendering process.
- **Build Process**: Fixed an `InvalidVersion` error during package build caused by a missing quote in `__init__.py`.

---

*This changelog was initiated after the initial development phase. Earlier versions are not documented.*