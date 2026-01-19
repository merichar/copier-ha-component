#!/usr/bin/env python3
"""Scaffold platforms and features for your Home Assistant integration.

Usage:
    python scripts/scaffold.py sensor
    python scripts/scaffold.py api
    python scripts/scaffold.py --list
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, TemplateNotFound
except ImportError:
    print("Error: jinja2 is required. Install with: uv pip install jinja2")
    sys.exit(1)


AVAILABLE_COMPONENTS = [
    # Base classes
    "entity",
    # Communication layer
    "api",
    "application_credentials",
    # Optional features
    "services",
    # Read-only entity platforms
    "sensor",
    "binary_sensor",
    # Control entity platforms
    "switch",
    "button",
    "light",
    "cover",
    # Device automation
    "device_trigger",
    "device_action",
    "device_condition",
]


def load_config():
    """Load component configuration from manifest.json."""
    manifest_path = Path("custom_components")

    # Find the first directory in custom_components
    try:
        component_slug = next(manifest_path.iterdir()).name
    except StopIteration:
        print("Error: No component found in custom_components/")
        sys.exit(1)

    manifest_file = manifest_path / component_slug / "manifest.json"

    if not manifest_file.exists():
        print(f"Error: manifest.json not found at {manifest_file}")
        sys.exit(1)

    with open(manifest_file) as f:
        manifest = json.load(f)

    return {
        "component_slug": component_slug,
        "component_name": manifest.get("name", component_slug.replace("_", " ").title()),
        "domain": manifest.get("domain", component_slug),
    }


def generate_component(component: str, config: dict, force: bool = False):
    """Generate a component file from template."""
    component_slug = config["component_slug"]

    # Check if entity.py base class exists
    entity_file = Path("custom_components") / component_slug / "entity.py"
    config["has_entity_base"] = entity_file.exists()

    # Set up Jinja environment
    template_dir = Path("scripts/scaffolds")
    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}")
        print("   Make sure you're running this from the project root.")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(str(template_dir)))

    # Try to find template with .py or .yaml extension
    template_file = None
    file_extension = None
    for ext in [".py", ".yaml"]:
        try:
            template_file = env.get_template(f"{component}{ext}.jinja")
            file_extension = ext
            break
        except TemplateNotFound:
            continue

    if not template_file:
        print(f"Error: Template not found for component: {component}")
        print(f"   Expected: {template_dir / f'{component}.py.jinja'} or {template_dir / f'{component}.yaml.jinja'}")
        return False

    # Set output path based on extension
    output_path = Path("custom_components") / component_slug / f"{component}{file_extension}"

    if output_path.exists() and not force:
        print(f"Error: {component}{file_extension} already exists. Use --force to overwrite.")
        return False

    # Render template
    rendered = template_file.render(**config)

    # Write file
    output_path.write_text(rendered)
    print(f"Created {output_path}")

    # Create corresponding test file
    test_path = Path("tests") / f"test_{component}.py"
    try:
        test_template = env.get_template(f"test_{component}.py.jinja")
        test_path.write_text(test_template.render(**config))
        print(f"Created {test_path}")
    except TemplateNotFound:
        print(f"No test template found for {component} (skipping)")

    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scaffold platforms and features for your Home Assistant integration"
    )
    parser.add_argument(
        "component",
        choices=AVAILABLE_COMPONENTS,
        help="Component to add",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing component file",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available components",
    )

    args = parser.parse_args()

    if args.list:
        print("Available components:")
        for component in AVAILABLE_COMPONENTS:
            print(f"  * {component}")
        return

    # Load configuration
    config = load_config()

    print(f"Adding {args.component} to {config['component_name']}...")

    # Generate component
    if generate_component(args.component, config, args.force):
        component_slug = config['component_slug']

        # Determine file extension
        file_ext = ".yaml" if args.component == "services" else ".py"

        print(f"\n{args.component} added successfully!")
        print(f"\nNext steps:")
        print(f"  1. Edit custom_components/{component_slug}/{args.component}{file_ext}")

        # Component-specific guidance
        if args.component == "entity":
            print(f"     * Customize device_info, unique_id patterns")
            print(f"     * Update device ID extraction from coordinator.data")
            print(f"  2. Regenerate existing platforms to use this base class:")
            print(f"     python scripts/scaffold.py sensor --force")
        elif args.component == "api":
            print(f"     * Update API endpoints and authentication")
            print(f"     * Implement data fetching methods")
            print(f"  2. Use this API client in your coordinator or entities")
        elif args.component == "application_credentials":
            print(f"     * Update OAuth authorize and token URLs")
            print(f"  2. Add 'application_credentials' to manifest.json dependencies")
            print(f"  3. Implement OAuth flow in config_flow.py")
        elif args.component == "services":
            print(f"     * Customize service definitions")
            print(f"  2. Register services in __init__.py:")
            print(f"     hass.services.async_register(DOMAIN, 'service_name', handler)")
        elif args.component in ["device_trigger", "device_action", "device_condition"]:
            print(f"     * Define your device automation triggers/actions/conditions")
            print(f"  2. These will appear in the automation UI automatically")
        else:  # Entity platforms
            print(f"     * Implement entity properties and methods")
            print(f"  2. Entities will be auto-discovered by Home Assistant")

        print(f"  3. Run tests: pytest tests/test_{args.component}.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
