# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - Upcoming

### Added
- **`test.py`**: Added a monolithic showcase script demonstrating all features logically and beautifully.
- **Improved API Stability**: Enhanced internal components to deal correctly with missing configurations.

### Changed
- **`README.md`**: Vastly improved and updated documentation.
- Removed legacy test files and refactored overall repository cleanliness safely.

### Fixed
- **`tables.py`**: Fully resolved the duplicated vertical boundaries on tables drawing logic where table lines appeared distorted.
- **`components.py` `checkbox` function**: Addressed the lack of `_process_text_for_printing` mapping, enabling inline formats parsing directly outside of the `act()` block safely utilizing `builtins.print`.
- **`components.py` missing imports**: Added `builtins` and `_process_text_for_printing` references to prevent crashing while typing options.
- **`animations.py` `loading_legacy` function**: Implemented the missing logic so the execution falls properly back into `_loading_context_manager` and blocks execution seamlessly.

## [0.4.0] - Previous

### Added
- **`Panel` Component**: New component (`pn`) for displaying text within a styled, bordered box.
- **Theming System**: Global theming support with `set_theme()` (`sth`) and `get_theme()` (`gth`) to customize component colors from a central place.
- **Smart `color_rules` for `input`**:
  - Now supports lists of words for a single color (e.g., `{"green": ["yes", "y"]}`).
- **Short & Super-Short Aliases**: Added a comprehensive set of aliases for all major components to speed up development (e.g., `prog`, `me`, `pn`, `pr`).
- **Clickable Actions**: Implemented `ActionTagManager` (`am`) to create interactive, mouse-clickable text in the terminal.

### Changed
- **Refactored Color Parser**: Completely rewrote the core color tag parser (`_process_text_for_printing`) to be a robust, recursive, parser-like engine.

### Fixed
- **Nested & Multiple Color Tags**: Resolved a critical, long-standing bug where nested tags and multiple tags on the same line were not rendered correctly. The new parser handles all cases flawlessly.
- **`menu` Component**: Fixed a major rendering bug that caused text artifacts and incorrect overwriting when navigating choices.
- **`progress` Component**: Fixed color tags not being applied to the progress bar.
- **`logger` Component**: Fixed color tags in log messages not being rendered.
- **`Layout` Component**: Fixed an `UnboundLocalError` crash during the rendering process.

---

*This changelog was initiated after the initial development phase. Earlier versions are not documented.*