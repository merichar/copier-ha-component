# Template Development Guide

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
   
   *Note: pip users can substitute `uv pip` with `pip` in all commands.*

3. **Install copier**:
   ```bash
   uv tool install copier
   # or with pipx: pipx install copier
   ```

## Template Structure

```
copier-ha-component/
├── template/                       # Files that get copied/templated
│   ├── custom_components/
│   │   └── {{ component_slug }}/
│   │       ├── config_flow.py.jinja
│   │       ├── __init__.py.jinja
│   │       ├── manifest.json.jinja
│   │       └── strings.json.jinja
│   ├── .devcontainer/
│   │   ├── devcontainer.json.jinja
│   │   └── docker-compose.yml
│   ├── tests/
│   │   └── test_init.py.jinja
│   ├── DEVELOPMENT.md.jinja
│   ├── docker-compose.yml.jinja
│   ├── .editorconfig
│   ├── .gitignore
│   ├── LICENSE.jinja
│   ├── pyproject.toml.jinja
│   └── README.md.jinja
├── copier.yml                      # Template configuration and questions
├── DEVELOPMENT.md                  # This file
├── LICENSE                         # MIT license for template
└── README.md                       # User-facing documentation for template use
```

## Key Files

### copier.yml

Defines:
- Questions asked during generation
- Default values and validation
- Conditional file inclusion
- Post-generation tasks

### template/ Directory

Contains all files that will be copied to generated projects.

**File naming:**
- `.jinja` suffix: File gets templated, suffix removed
- No suffix: File copied as-is
- `{{ variable }}`: Directory/file names can use variables

### Jinja Templating

Variables from `copier.yml` are available in templates:

```jinja
{% if include_config_flow %}
# This section only appears if user chose yes
{% endif %}

{{ component_name }}  # Replaced with user's input
```

## Testing Template Changes

### Local Testing

1. **Generate a test component**:
   ```bash
   copier copy --trust . ../test-component
   ```
   
   Note: The `--trust` flag is needed because the template uses tasks for git initialization and helpful output messages.

2. **Answer prompts** (use varied inputs to test different paths)

3. **Verify generated files**:
   ```bash
   cd ../test-component
   ls -la
   cat custom_components/*/manifest.json
   ```

4. **Test the generated component**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .[dev]
   pytest
   ```

### Test Scenarios

Test with different combinations:
- With/without config flow
- Different IoT classes (including decide_later)
- With/without MIT license
- Various component names (spaces, hyphens, etc.)

### Common Issues to Check

**Jinja syntax errors**:
- Run generation, check for `{{ }}` in output files
- Check for proper `{% endif %}` closing tags

**File paths**:
- Ensure `{{ component_slug }}` directory is created
- Check conditional file exclusion works

**Git initialization**:
- Verify post-generation tasks run
- Check initial commit is created

## Making Changes

### Adding New Questions

1. Add to `copier.yml`:
   ```yaml
   new_option:
     type: str
     help: Description with examples
     default: "default_value"
   ```

2. Use in templates:
   ```jinja
   {{ new_option }}
   ```

### Adding New Files

1. Create in `template/` directory
2. Add `.jinja` suffix if it needs templating
3. Add to `_exclude` in copier.yml if conditional

### Modifying Existing Templates

1. Edit files in `template/`
2. Test generation
3. Verify output in generated project

## Validation Testing

Before committing:

```bash
# Test basic generation
copier copy --trust . ../test-basic

# Test with config flow
copier copy --trust . ../test-config-flow
# Answer yes to config_flow

# Test without config flow
copier copy --trust . ../test-no-config-flow
# Answer no to config_flow

# Test decide_later iot_class
copier copy --trust . ../test-decide-later
# Choose decide_later for iot_class

# Verify each generates correctly
for dir in ../test-*; do
  echo "Testing $dir"
  cd "$dir"
  grep -r "{{" . && echo "ERROR: Untemplated variables found!" || echo "OK"
  uv venv
  source .venv/bin/activate
  uv pip install -e .[dev]
  pytest
  cd -
done
```

## Copier Features Used

### Conditional Files

```yaml
_exclude:
  - "{% if not include_config_flow %}custom_components/{{ component_slug }}/config_flow.py.jinja{% endif %}"
```

### Post-generation Tasks

```yaml
_tasks:
  - "git init"
  - "git add ."
  - 'git commit -m "feat: initial component"'
```

### Validation

```yaml
repo_name:
  validator: "{% if not repo_name.startswith('ha-') %}Repository name must start with 'ha-'{% endif %}"
```

## Common Template Patterns

### Multi-line Help

```yaml
component_name:
  type: str
  help: |
    What is your component name?
    
    Examples:
    - "Acme Thermostat"
    - "Solar Production"
```

### Auto-generated Defaults

```yaml
component_slug:
  default: "{{ component_name.lower().replace(' ', '_') }}"
```

### Conditional Content

```jinja
{% if include_config_flow %}
async def async_setup_entry(...):
    ...
{% else %}
async def async_setup(...):
    ...
{% endif %}
```

## Contributing Guidelines

1. **Update documentation** if adding features
2. **Use semantic commits**:
   - `feat: add new template feature`
   - `fix: correct Jinja syntax in manifest`
   - `docs: improve setup instructions`
3. **Submit PR** with clear description

## Release Process

1. **Test all scenarios** thoroughly
2. **Update version** in documentation if needed
3. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```
4. **Tag release**:
   ```bash
   git tag -a v1.x.x -m "Release v1.x.x"
   ```
5. **Push to GitHub**:
   ```bash
   git push origin main --tags
   ```

## Resources

- [Copier Documentation](https://copier.readthedocs.io/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)

## Getting Help

- Open an issue on GitHub
- Check existing issues for similar problems
- Review Copier documentation for advanced features
