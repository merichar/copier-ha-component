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

Follow the prompts, then see your component's [DEVELOPMENT.md](template/DEVELOPMENT.md.jinja) for next steps.

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
├── .pre-commit-config.yaml
├── custom_components/
│   └── your_slug/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── diagnostics.py         # Debug data export
│       ├── system_health.py       # System health info
│       ├── coordinator.py         # Data fetching (polling integrations only)
│       ├── config_flow.py         # UI configuration (if enabled)
│       └── strings.json           # Translations (if config flow enabled)
├── scripts/
│   ├── check_version.py
│   ├── scaffold.py                # Add platforms/features on-demand
│   ├── SCAFFOLD.md                # Scaffold documentation
│   └── scaffolds/                 # Templates for platforms
│       ├── entity.py.jinja          # Base entity class
│       ├── ENTITY_BASE_CLASS.md     # Base entity guide
│       ├── api.py.jinja             # API client
│       ├── application_credentials.py.jinja  # OAuth
│       ├── APPLICATION_CREDENTIALS_GUIDE.md  # OAuth guide
│       ├── services.yaml.jinja      # Custom services
│       ├── sensor.py.jinja          # Sensor platform
│       ├── binary_sensor.py.jinja   # Binary sensor
│       ├── switch.py.jinja          # Switch platform
│       └── ... (more platforms)
├── tests/
│   └── test_init.py
├── docker-compose.yml
├── hacs.json
├── LICENSE                        # MIT license (optional)
├── pyproject.toml
├── README.md
└── DEVELOPMENT.md
```

**Core files included:**
- Integration core: `__init__.py`, `manifest.json`, `const.py`
- Diagnostics: `diagnostics.py`, `system_health.py`
- Coordinator: `coordinator.py` (polling integrations only)
- Config flow: `config_flow.py`, `strings.json` (if enabled)

**Platforms added on-demand:**
After generation, add platforms using the scaffold script:
```bash
python scripts/scaffold.py sensor
python scripts/scaffold.py switch
python scripts/scaffold.py api        # If you need API communication
python scripts/scaffold.py entity     # If you want shared base class
```

**Available scaffolds:**
- Base: `entity` (shared base class for multi-platform integrations)
- Communication: `api`, `application_credentials` (OAuth)
- Features: `services` (custom actions)
- Platforms: `sensor`, `binary_sensor`, `switch`, `button`, `light`, `climate`, `cover`, `fan`, `lock`
- Automation: `device_trigger`, `device_action`, `device_condition`

See generated component's [scripts/SCAFFOLD.md](template/scripts/SCAFFOLD.md) for complete scaffold documentation.

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

See generated component's [DEVELOPMENT.md](template/DEVELOPMENT.md.jinja) for complete details.

## Template Development

Want to modify or contribute to this template? See [DEVELOPMENT.md](DEVELOPMENT.md).

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Copier Documentation](https://copier.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

This project is licensed under the MIT License: See [LICENSE](LICENSE) file for details.
