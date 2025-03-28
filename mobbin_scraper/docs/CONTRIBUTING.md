# Contributing to Mobbin Flow Scraper

Thank you for your interest in contributing to the Mobbin Flow Scraper project! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate when contributing to this project. We aim to foster an inclusive and welcoming environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Create a new branch** for your feature or bugfix
4. **Install dependencies** as specified in the README.md

## Development Environment Setup

To set up your development environment:

1. Install Python 3.7 or higher
2. Install the required packages:
   ```bash
   pip install python-dotenv boto3 pydantic browser-use
   pip install pytest pytest-cov black mypy flake8  # For development
   ```
3. Copy `.env.mobbin_scraper.example` to `.env.mobbin_scraper` and update with your credentials

## Code Structure

The project is organized as follows:

- `scrape_mobbin_flow_tree.py`: Main script containing all scraping logic
- `README.md`: Project documentation
- `.env.mobbin_scraper`: Environment variables configuration
- `checkpoints/`: Directory for storing progress checkpoints
- `logs/`: Directory for log files

## Coding Style

We follow PEP 8 style guidelines with a few specific rules:

- Line length maximum of 100 characters
- Use type hints for all function parameters and return values
- Document functions with docstrings
- Run `black` for code formatting

## Pull Request Process

1. **Update documentation** if your changes affect the user experience or API
2. **Add tests** for new functionality
3. **Run the test suite** to ensure nothing breaks
4. **Create a Pull Request** with a clear description of your changes
5. **Address review comments** if requested by maintainers

## Testing

Before submitting your PR, make sure your changes pass all tests:

```bash
# Run linting
black scrape_mobbin_flow_tree.py
flake8 scrape_mobbin_flow_tree.py
mypy scrape_mobbin_flow_tree.py

# Run tests (if applicable)
pytest -xvs
```

## Feature Requests and Bug Reports

- **Feature requests**: Open an issue with the label "enhancement"
- **Bug reports**: Open an issue with the label "bug" and include:
  - Clear description of the issue
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment information (OS, Python version, etc.)

## Areas for Contribution

We welcome contributions in the following areas:

1. **Performance improvements**: Making the scraper faster or more efficient
2. **Error handling**: Improving resilience against network issues or site changes
3. **New features**: Adding functionality like rate limiting, proxy support, etc.
4. **Documentation**: Improving or expanding the existing documentation
5. **Testing**: Adding automated tests

## Code Review Process

All submissions require review before merging:

1. At least one maintainer must approve the changes
2. All CI checks must pass
3. Code should follow project standards and practices

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

## Questions?

If you have any questions about contributing, feel free to open an issue with the label "question".

Thank you for helping improve the Mobbin Flow Scraper! 