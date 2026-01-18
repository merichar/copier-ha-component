# Copier Template: Home Assistant Component

Modern template for Home Assistant custom components using uv, pytest, ruff, and devcontainers.

## Quick Start

```bash
# Install prerequisites
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install copier

# Generate your component
copier copy --trust gh:merichar/copier-ha-component your-component-name
```

Follow the prompts, then see your component's `DEVELOPMENT.md` for next steps.

## Features

- Modern Python tooling (uv, ruff, pytest)
- Devcontainer support for VS Code, Emacs, Vim users
- Optional config flow for UI configuration
- Comprehensive development documentation
- Editor-agnostic configuration
- Semantic commit structure

## Prerequisites

**uv (recommended)** - Fast Python package manager

macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

*Note: pip users can substitute `uv pip` with `pip` in all commands.*

**Copier** - Template engine

```bash
uv tool install copier
# or with pipx: pipx install copier
```

### Optional

**Docker** - For devcontainer or manual testing
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS/Windows)
- [Docker Engine](https://docs.docker.com/engine/install/) (Linux)

**Your favorite editor**
- VS Code with Dev Containers extension (most common)
- Emacs with lsp-mode or eglot
- Vim/Neovim with LSP support

## Usage

Generate a new component:

```bash
copier copy --trust gh:merichar/copier-ha-component your-component-name
```

Note: The `--trust` flag is required because the template uses tasks for git initialization and helpful setup messages.

You'll be asked:
- Component name (e.g., "Acme Thermostat")
- Author information
- Whether to include config flow (UI configuration)
- IoT class (how component communicates)
- License preference

## What You Get

```
your-component-name/
├── .devcontainer/
│   ├── devcontainer.json
│   └── docker-compose.yml
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yml
├── custom_components/
│   └── your_slug/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py      (optional)
│       └── strings.json        (optional)
├── scripts/
│   └── check_version.py
├── tests/
│   └── test_init.py
├── docker-compose.yml
├── hacs.json
├── LICENSE                     (optional)
├── pyproject.toml
├── README.md
└── DEVELOPMENT.md
```

## After Generation

Three development paths:

**A. Devcontainer (Recommended)**
- Open in VS Code, reopen in container

**B. Docker manually**
```bash
docker compose -f .devcontainer/docker-compose.yml up -d
docker compose -f .devcontainer/docker-compose.yml exec devcontainer bash
```

**C. Local Python**
```bash
uv venv && source .venv/bin/activate
uv pip install -e .[dev]
pytest
```

See your component's `DEVELOPMENT.md` for complete details.

## Template Development

Want to modify or contribute to this template? See [DEVELOPMENT.md](DEVELOPMENT.md).

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Copier Documentation](https://copier.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

This project is licensed under the MIT License: See [LICENSE](LICENSE) file for details.
