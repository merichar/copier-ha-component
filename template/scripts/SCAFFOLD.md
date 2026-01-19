# Component Scaffolding Script

This directory contains a helper script for scaffolding Home Assistant platforms and features.

## Adding Components

Use `scaffold.py` to generate new platform and feature files from templates:

```bash
# Add a sensor platform
python scripts/scaffold.py sensor

# Add a switch platform
python scripts/scaffold.py switch

# Add device triggers
python scripts/scaffold.py device_trigger
```

### Available Components

**Base Classes:**
- `entity` - Base entity class for shared device_info (optional, for multi-platform integrations)

**Communication Layer:**
- `api` - API client for external communication
- `application_credentials` - OAuth2 authorization flow (see [scaffolds/APPLICATION_CREDENTIALS_GUIDE.md](scaffolds/APPLICATION_CREDENTIALS_GUIDE.md))

**Optional Features:**
- `services` - Custom service definitions

**Entity Platforms:**
- `sensor` - Read-only data (temperature, battery, status)
- `binary_sensor` - On/off states (motion, door open/closed)
- `switch` - Controllable on/off devices
- `button` - Trigger actions (restart, calibrate)
- `light` - Lights with brightness/color control
- `cover` - Garage doors, blinds, shutters

**Device Automation:**
- `device_trigger` - Automation triggers (button pressed, motion detected)
- `device_action` - Automation actions
- `device_condition` - Automation conditions

*Some scaffolds have detailed guides in the `scaffolds/` directory for additional information.*

### Options

```bash
# List all available components
python scripts/scaffold.py --list

# Overwrite existing component file
python scripts/scaffold.py sensor --force
```

### Base Entity Class (Optional)

For integrations with multiple platforms sharing the same device, generate `entity.py` first:

```bash
python scripts/scaffold.py entity
```

After `entity.py` exists, all platforms automatically inherit from it:
- Centralized device_info
- Consistent unique_id patterns
- Shared availability logic

Platforms auto-detect `entity.py` and adjust imports/inheritance accordingly. See [scaffolds/ENTITY_BASE_CLASS.md](scaffolds/ENTITY_BASE_CLASS.md) for details.

## Component Templates

Templates are stored in `scripts/scaffolds/` and use Jinja2 syntax.

Available variables in templates:
- `component_slug` - The integration domain (e.g., `my_integration`)
- `component_name` - Human-readable name (e.g., `My Integration`)
- `domain` - Same as component_slug

### Creating Custom Templates

Add new `.jinja` files to `scaffolds/`:

```
scripts/scaffolds/
├── sensor.py.jinja
├── switch.py.jinja
├── button.py.jinja
└── your_component.py.jinja
```

The script will automatically use any new templates you add.
