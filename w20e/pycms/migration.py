import logging
import os


LOGGER = logging.getLogger("pycms")


def normalize_version(version):

    return version.replace(".", "_").replace("-", "_")


def migrate(current_version, target_version):

    LOGGER.info("Upgrade from %s to %s" % (current_version, target_version))

    current_version = normalize_version(current_version)
    target_version = normalize_version(target_version)    
    
    update_mod = "w20e.pycms.migrations.%s__%s" % \
                 (current_version, target_version)

    mod_path = os.path.join(os.path.dirname(__file__),
                            "migrations",
                            "%s__%s.py" % (current_version, target_version)
                            )

    if os.path.isfile(mod_path):
        
        try:
            __import__(update_mod)
            LOGGER.info("Found upgrade")
        except:
            LOGGER.warn("No upgrade found")
            return False
        
    return True
