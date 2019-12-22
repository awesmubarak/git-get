# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2019-12-22

### Changed

- `remove` now confirms file deletion before changing the package list
- `remove` accepts many more inputs for yes/no
- `change`'s output is now a nice table
- Underscores are used to seperate components of the generate package names

### Fixed

- Program would crash when the package list was empty

[2.2.0]: https://github.com/awesmubarak/gitget/releases/tag/v2.2.0