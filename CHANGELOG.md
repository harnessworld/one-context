# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Breaking:** Python import package is now `one_context`. Use `python -m one_context` when the `onecxt` script is not on `PATH`.
- **Breaking:** Workspace root environment variable is `ONECXT_ROOT` only; older alternate env vars are no longer read.
- **Breaking:** Adapter-generated filenames use the `onecxt-{workspace-id}` prefix (e.g. `.cursor/rules/onecxt-dev.mdc`) instead of the previous default prefix.
- Context export JSON field `kind` is now `one-context` (replacing the previous context kind string).
- Console entry point remains `onecxt`.

### Added

- GitHub Actions workflow to run `doctor` and the test suite on Python 3.10–3.13.
