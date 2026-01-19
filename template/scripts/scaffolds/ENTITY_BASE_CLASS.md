# Base Entity Class (`entity.py`)

## What is `entity.py`?

`entity.py` provides a base entity class that all your platforms can inherit from. This centralizes common functionality like device_info, unique_id patterns, and availability logic.

## When to Use It

**Use `entity.py` if:**
- You have multiple platforms (sensor, switch, binary_sensor, etc.)
- All entities belong to the same device(s)
- You want consistent device_info across all entities
- You have custom unique_id formatting

**Skip `entity.py` if:**
- You only have one platform (just sensor)
- Each entity represents a different device
- Simple integrations with no shared logic

## How It Works

### 1. Generate `entity.py` First

```bash
python scripts/scaffold.py entity
```

This creates `custom_components/my_integration/entity.py` with:
- Base class `MyIntegrationEntity`
- Centralized `device_info` property
- Consistent `unique_id` pattern
- Common `available` property

### 2. Generate Platforms

After `entity.py` exists, platforms automatically inherit from it:

```bash
python scripts/scaffold.py sensor
python scripts/scaffold.py switch
```

**Without `entity.py`**, platforms inherit from `CoordinatorEntity`:
```python
class MyIntegrationSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_sensor"
        # ... device_info handled per-entity
```

**With `entity.py`**, platforms inherit from your base class:
```python
from .entity import MyIntegrationEntity

class MyIntegrationSensor(MyIntegrationEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, "sensor")
        # unique_id and device_info handled by base class
```

### 3. Auto-Detection

The scaffold script automatically detects if `entity.py` exists:
- `entity.py` found: Platforms import and use `MyIntegrationEntity`
- `entity.py` missing: Platforms use `CoordinatorEntity` directly

### 4. Regenerate After Adding `entity.py`

If you add `entity.py` after creating platforms:

```bash
# Create entity base class
python scripts/scaffold.py entity

# Regenerate existing platforms to use it
python scripts/scaffold.py sensor --force
python scripts/scaffold.py switch --force
```

## What `entity.py` Provides

### Base Class Structure

```python
class MyIntegrationEntity(CoordinatorEntity):
    """Base entity for My Integration."""

    def __init__(self, coordinator, entity_type):
        super().__init__(coordinator)
        self._entity_type = entity_type
        # Extract device info from coordinator.data

    @property
    def device_info(self):
        """Common device info for all entities."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Acme Corp",
            model=self._model,
        )

    @property
    def unique_id(self):
        """Consistent unique ID pattern."""
        return f"{self._device_id}_{self._entity_type}"

    @property
    def available(self):
        """Common availability logic."""
        return self.coordinator.last_update_success
```

### Platform Usage

```python
class MyIntegrationSensor(MyIntegrationEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        # Pass entity_type to base class
        super().__init__(coordinator, "sensor")

        # device_info and unique_id automatically handled
        # Just set sensor-specific attributes
        self._attr_name = f"{entry.title} Temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
```

## Benefits

1. **DRY** - device_info defined once, not per-platform
2. **Consistency** - All entities use same unique_id pattern
3. **Maintainability** - Change device info in one place
4. **Device Grouping** - All entities show under one device in HA UI

## Example Workflow

```bash
# Start integration
copier copy gh:user/copier-ha-component my-integration

# Add base entity class
python scripts/scaffold.py entity

# Add platforms (automatically use entity base class)
python scripts/scaffold.py sensor
python scripts/scaffold.py binary_sensor
python scripts/scaffold.py switch

# Customize entity.py
# Edit device_info, unique_id patterns, etc.

# All platforms inherit your customizations!
```

## Customization

Edit `entity.py` to customize:

```python
def __init__(self, coordinator, entity_type):
    super().__init__(coordinator)
    self._entity_type = entity_type

    # TODO: Extract from coordinator.data
    device_data = coordinator.data.get("device_info", {})
    self._device_id = device_data.get("id", "unknown")
    self._device_name = device_data.get("name", "My Device")
    self._model = device_data.get("model", "Unknown")

@property
def device_info(self):
    return DeviceInfo(
        identifiers={(DOMAIN, self._device_id)},
        name=self._device_name,
        manufacturer="Your Brand",
        model=self._model,
        sw_version=self.coordinator.data.get("firmware", "1.0"),
        configuration_url=f"http://{self.coordinator.data.get('ip')}",
    )

@property
def unique_id(self):
    # Custom pattern: domain_deviceid_type
    return f"{DOMAIN}_{self._device_id}_{self._entity_type}"
```

## Notes

- `entity.py` is **optional** - platforms work fine without it
- The scaffold script **automatically detects** its presence
- You can add it **at any time** and regenerate platforms
- Class name derives from slug: `my_thermostat` -> `MyThermostatEntity`
- Best for **multi-platform** integrations with shared devices
