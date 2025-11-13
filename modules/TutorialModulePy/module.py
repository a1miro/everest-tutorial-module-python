#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Pionix GmbH and Contributors to EVerest

"""
EVerest Tutorial Module - Python Implementation

This module demonstrates how to create an EVerest module in Python.
It implements the interface_tutorial_module interface.
"""

from everest.framework import Module, RuntimeSession


class TutorialModulePy(Module):
    """
    Python implementation of the EVerest Tutorial Module.
    """

    def __init__(self, session: RuntimeSession):
        super().__init__(session)
        self.config_tutorial_switch = None

    def _setup(self, runtime_session: RuntimeSession):
        """
        Setup method called during module initialization.
        Here you can access configuration and prepare resources.
        """
        # Access configuration parameters
        self.config_tutorial_switch = self.config.config_tutorial_switch
        self.logger.info(f"Tutorial module initialized with config_tutorial_switch={self.config_tutorial_switch}")

    def _ready(self):
        """
        Ready method called when all modules are initialized and ready to interact.
        This is where you can start background tasks or subscribe to events.
        """
        self.logger.info("Tutorial module is ready!")

    def command_tutorial(self, payload: str) -> str:
        """
        Implementation of the command_tutorial command.
        
        Args:
            payload: An arbitrary string that can be sent to the module
            
        Returns:
            The response string (default: "everest")
        """
        self.logger.info(f"Received command_tutorial with payload: {payload}")
        
        # You can add your custom logic here
        if self.config_tutorial_switch:
            return f"everest (config enabled): {payload}"
        else:
            return "everest"


if __name__ == "__main__":
    # RuntimeSession is provided by the EVerest manager
    import sys
    from everest.framework import RuntimeSession
    
    session = RuntimeSession.from_main()
    module = TutorialModulePy(session)
    module.run()
