# EVerest Tutorial Module - Python Implementation

A Python implementation of the EVerest tutorial module, demonstrating how to create EVerest modules using Python instead of C++.

## Overview

This module provides the same functionality as the C++ tutorial module but is implemented in Python using the `everest.framework` package.

## Features

- Implements the `interface_tutorial_module` interface
- Provides the `command_tutorial` command
- Configurable via `config_tutorial_switch` parameter
- Simpler and faster to develop than C++ version

## Installation

This module is built and installed via Yocto/BitBake:

```bash
bitbake everest-tutorial-module-python
```

## Configuration

Add to your EVerest configuration YAML:

```yaml
active_modules:
  tutorial_py:
    module: TutorialModulePy
    config_implementation:
      config_tutorial_switch: true
```

## Testing with MQTT

```bash
# Subscribe to see module activity
mosquitto_sub -h localhost -t 'everest/#' -v &

# Send a command to the module
mosquitto_pub -h localhost \
  -t 'everest/tutorial_py/interface_impl_tutorial_module/cmd/command_tutorial' \
  -m '{"payload": "Hello from Python!"}'
```

## License

Apache-2.0

## Authors

- Andrei Mironenko, Parallel Dynamic Ltd.
