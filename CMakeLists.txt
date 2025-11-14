cmake_minimum_required(VERSION 3.14.7)
project(everest-tutorial-python VERSION 0.1
    DESCRIPTION "EVerest tutorial module - Python implementation"
    LANGUAGES NONE)

include(GNUInstallDirs)

# Install config-module-tutorial-python.yaml to /etc/everest
install(
    FILES config-module-tutorial-python.yaml config-with-client.yaml
    DESTINATION ${CMAKE_INSTALL_SYSCONFDIR}/everest
)


# Install interface definition
install(
    #FILES interfaces/interface_tutorial_module.yaml interfaces/empty.yaml
    FILES interfaces/interface_tutorial_module.yaml
    DESTINATION ${CMAKE_INSTALL_DATADIR}/everest/interfaces
)

# Install Python modules
install(
    DIRECTORY modules/TutorialModulePy modules/TutorialClientPy
    DESTINATION ${CMAKE_INSTALL_LIBEXECDIR}/everest/modules
    FILES_MATCHING 
    PATTERN "*.py"
    PATTERN "*.yaml"
)

# Make the Python modules executable
install(
    FILES modules/TutorialModulePy/module.py
    DESTINATION ${CMAKE_INSTALL_LIBEXECDIR}/everest/modules/TutorialModulePy
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
)

install(
    FILES modules/TutorialClientPy/module.py
    DESTINATION ${CMAKE_INSTALL_LIBEXECDIR}/everest/modules/TutorialClientPy
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
)
