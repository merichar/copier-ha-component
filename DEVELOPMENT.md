# Copier Template Development Guide

Guide for working on the copier-ha-component template itself.

## Setup for Template Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/merichar/copier-ha-component.git
   cd copier-ha-component
   ```

2. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   *Note: pip users can substitute `uv` commands with pip equivalents.*

3. **Install copier**:
   ```bash
   uv tool install copier
   # or with pipx: pipx install copier
   ```

4. **Install pre-commit** (recommended):
   ```bash
   uv tool install pre-commit
   # or with pipx: pipx install pre-commit

   pre-commit install
   ```

   This ensures your template changes are validated before committing.

## Template Structure

```
copier-ha-component/
├── .pre-commit-config.yaml         # Pre-commit hooks for template repo
├── copier.yml                      # Template configuration and questions
├── DEVELOPMENT.md                  # This file
├── LICENSE                         # MIT license for template
├── README.md                       # User-facing documentation
├── scripts/
│   └── release.sh                  # Template release script
├── tests/
│   └── copier/
│       └── default-answers.yml     # Test answers for pre-commit validation
└── template/                       # Files that get copied/templated
    ├── .devcontainer/
    │   ├── devcontainer.json.jinja
    │   └── docker-compose.yml
    ├── .editorconfig
    ├── .gitignore
    ├── .pre-commit-config.yaml.jinja
    ├── custom_components/
    │   └── {{ component_slug }}/
    │       ├── __init__.py.jinja
    │       ├── manifest.json.jinja
    │       ├── const.py.jinja
    │       ├── entity.py.jinja        # Base entity (all types)
    │       ├── sensor.py.jinja        # Example platform
    │       ├── coordinator.py.jinja   # Conditional: polling only
    │       ├── api.py.jinja           # Conditional: all except 'none'
    │       ├── config_flow.py.jinja   # Conditional: if enabled
    │       └── strings.json.jinja     # Conditional: if config flow
    ├── scripts/
    │   └── check_version.py.jinja
    ├── tests/
    │   └── test_init.py.jinja
    ├── DEVELOPMENT.md.jinja
    ├── docker-compose.yml.jinja
    ├── hacs.json.jinja
    ├── LICENSE.jinja
    ├── pyproject.toml.jinja
    └── README.md.jinja
```

## Key Files

### copier.yml

Defines:
- Questions asked during generation
- Default values and validation
- Conditional file inclusion via `_exclude`
- Post-generation tasks via `_tasks`
- Post-generation message via `_message_after_copy`

**Important settings**:
- `_templates_suffix: .jinja` - Files ending in `.jinja` get templated
- `_subdirectory: template` - Use `template/` as source directory

### template/ Directory

Contains all files that will be copied to generated projects.

**File naming:**
- `.jinja` suffix: File gets templated, suffix removed during generation
- No suffix: File copied as-is
- `{{ variable }}`: Directory/file names can use variables

### Jinja Templating

Variables from `copier.yml` are available in templates:

```jinja
{% if include_config_flow %}
# This section only appears if user chose yes
{% endif %}

{{ component_name }}  # Replaced with user's input
{{ vcs_uri_prefix }}{{ git_username }}/{{ repo_name }}  # VCS-agnostic URLs
```

## Testing Template Changes

### Local Testing

**Important: Force local template use**

By default, copier may use the latest git tag instead of your current changes. Always use `--vcs-ref HEAD` to ensure it uses your local working directory:
```bash
# Clear cache to ensure fresh generation
rm -rf ~/.cache/copier

# Generate using current local state (uncommitted, unpushed, untagged changes)
copier copy --trust --vcs-ref HEAD . ../test-component
```

**Non-interactive testing:**
```bash
# Use defaults for all questions
copier copy --trust --defaults --vcs-ref HEAD . ../test-component

# Or provide specific answers
copier copy --trust --defaults --vcs-ref HEAD \
  --data component_name="Test Component" \
  --data integration_type="none" \
  . ../test-component
```

**Using test answers file:**
```bash
copier copy --trust --defaults --vcs-ref HEAD \
  --data-file tests/copier/default-answers.yml \
  . ../test-component
```

**Important flags:**
* `--trust` - Required because template uses tasks for git initialization
* `--vcs-ref HEAD` - Use current local state, not latest tag/remote
* `--defaults` - Non-interactive mode, uses default values



**Test the generated component:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .[dev]
   pytest
   ```

**Check for untemplated variables:**
   ```bash
   grep -r "{{" . && echo "ERROR: Found untemplated variables!" || echo "OK"
   ```

### Running Pre-commit

**Automatically on commit** (if installed):
```bash
git commit -m "feat: add new feature"
# Pre-commit runs automatically
```

**Manually on all files**:
```bash
pre-commit run --all-files
```

**Update hook versions**:
```bash
pre-commit autoupdate
```

**Skip hooks** (not recommended):
```bash
git commit --no-verify
```

## Making Changes

### Adding New Questions

1. **Add to `copier.yml`**:
   ```yaml
   new_option:
     type: str
     qmark: "> "
     help: |

       What is your new option?

       Examples:
       * Example 1
       * Example 2

     default: "default_value"
     placeholder: "example"
   ```

2. **Use in templates**:
   ```jinja
   {{ new_option }}
   ```

### Adding New Template Files

1. Create in `template/` directory
2. Add `.jinja` suffix if it needs templating
3. Add to `_exclude` in `copier.yml` (without `.jinja` suffix) if it's only
   generated conditionally:
   ```yaml
   _exclude:
     - "{% if some_condition %}path/to/file{% endif %}"
   ```

### Updating Documentation

- Update template repo `README.md` (how to use the template)
- Update this `DEVELOPMENT.md` (how to work on the template)
- Update `template/DEVELOPMENT.md.jinja` (for generated component developers)
- Update `template/README.md` (how to use the generated component)

### Modifying Existing Templates

1. Edit files in `template/`
2. Test generation with `copier copy --trust . ../test-output`
3. Verify output in generated project
4. Run pre-commit checks: `pre-commit run --all-files`

## Common Template Patterns

### Multi-line Help with Examples

```yaml
component_name:
  type: str
  qmark: "> "
  help: |

    What is your component name?

    Examples:
    * "Acme Thermostat"
    * "Solar Production"

  placeholder: "Acme Thermostat"
```

### Auto-generated Defaults

```yaml
component_slug:
  default: "{{ component_name.lower().replace(' ', '_').replace('-', '_') }}"
```

### Conditional Template Content

```jinja
{% if include_config_flow %}
async def async_setup_entry(...):
    """Set up from a config entry."""
    ...
{% else %}
async def async_setup(...):
    """Set up from YAML configuration."""
    ...
{% endif %}
```

### VCS-Agnostic URLs

```jinja
{{ vcs_uri_prefix }}{{ git_username }}/{{ repo_name }}
# Becomes: https://github.com/user/repo (if GitHub)
# Becomes: https://gitlab.com/user/repo (if GitLab)
```

## Contributing Guidelines

1. **Run pre-commit**: `pre-commit run --all-files`
2. **Use semantic commits**:
   - `feat: add new template feature`
   - `fix: correct Jinja syntax in manifest`
   - `docs: improve setup instructions`
   - `refactor: reorganize template structure`
3. **Update documentation** if adding features
4. **Submit PR** with clear description of changes

## Release Process

1. **Run full validation**:
   ```bash
   pre-commit run --all-files
   # Fix any issues
   ```

2. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```

3. **Tag release**:
   ```bash
   git tag -a v1.x.x -m "Release v1.x.x"
   ```

4. **Push to repository**:
   ```bash
   git push origin main --tags
   ```

## Resources

### Copier

- [Copier Documentation](https://copier.readthedocs.io/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Copier Examples](https://github.com/copier-org/copier)

### Home Assistant

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Development Checklist](https://developers.home-assistant.io/docs/development_checklist)
- [HACS Documentation](https://hacs.xyz/docs/publish/start)

### Tools

- [uv Documentation](https://docs.astral.sh/uv/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## Getting Help

- Open an issue on the repository
