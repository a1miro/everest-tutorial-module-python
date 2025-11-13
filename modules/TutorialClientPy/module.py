#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Pionix GmbH and Contributors to EVerest

"""
EVerest Tutorial Client Module - Python Implementation

This module demonstrates how to use another module's interface in Python.
It requires the interface_tutorial_module interface and periodically calls
the command_tutorial command on the connected module.
"""

import time
import threading
from everest.framework import Module, RuntimeSession


class TutorialClientPy(Module):
    """
    Python implementation of a client for the EVerest Tutorial Module.
    This module connects to a TutorialModulePy instance and uses its interface.
    """

    def __init__(self, session: RuntimeSession):
        super().__init__(session)
        self.client_name = None
        self.poll_interval = 10
        self.running = False
        self.poll_thread = None
        self.tutorial_interface_fulfillment = None

    def _setup(self, runtime_session: RuntimeSession):
        """
        Setup method called during module initialization.
        """
        self.logger.info(f"Tutorial client module '{self.client_name}' initializing...")

    def _ready(self):
        """
        Ready method called when all modules are initialized and ready to interact.
        This is where we start our polling thread.
        """
        self.logger.info(f"Tutorial client '{self.client_name}' is ready! Starting periodic polling...")
        self.running = True
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()

    def _poll_loop(self):
        """
        Background thread that periodically calls the tutorial module's command.
        """
        counter = 0
        while self.running:
            try:
                counter += 1
                payload = f"{self.client_name} message #{counter}"
                
                print(f"[CLIENT] Calling command_tutorial with payload: {payload}")
                
                # Call the command on the required interface
                result = self.call_command(
                    self.tutorial_interface_fulfillment,  # The fulfillment object
                    "command_tutorial",                   # The command name
                    {"payload": payload}                  # The command arguments
                )
                
                print(f"[CLIENT] Received response: {result}")
                
            except Exception as e:
                print(f"[CLIENT] Error calling command_tutorial: {e}")
            
            # Wait for the next poll interval
            time.sleep(self.poll_interval)

    def shutdown(self):
        """
        Clean shutdown of the module.
        """
        print(f"[CLIENT] Tutorial client '{self.client_name}' shutting down...")
        self.running = False
        if self.poll_thread:
            self.poll_thread.join(timeout=2)


if __name__ == "__main__":
    # The EVerest manager creates and injects the RuntimeSession
    import sys
    
    # Create session from command line arguments provided by manager
    if sys.argv.__len__() != 3:
        session = RuntimeSession()
    else:
        session = RuntimeSession(sys.argv[1], sys.argv[2])
    
    module = TutorialClientPy(session)

    # Initialize and connect to the framework
    setup = module.say_hello()

    # Access configuration
    module.client_name = setup.configs.module.get("client_name", "DefaultClient")
    module.poll_interval = setup.configs.module.get("poll_interval_seconds", 10)
    
    # Get the fulfillment for the required interface (connections returns a list, we need the first one)
    tutorial_connections = setup.connections.get("tutorial_interface")
    module.tutorial_interface_fulfillment = tutorial_connections[0] if tutorial_connections else None

    # No commands to implement for this module - it only calls commands on other modules
    
    # Signal that we're ready
    module.init_done()
    
    # Start the polling thread
    print(f"Tutorial client '{module.client_name}' is ready! Starting periodic polling...")
    module.running = True
    module.poll_thread = threading.Thread(target=module._poll_loop, daemon=True)
    module.poll_thread.start()
    
    # Keep the main thread alive while the background thread runs
    try:
        while module.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Received keyboard interrupt, shutting down...")
        module.shutdown()
