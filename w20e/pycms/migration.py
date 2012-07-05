import logging


LOGGER = logging.getLogger("pycms")


def normalize_version(version):

    return version.replace(".", "_").replace("-", "_")


def migrate(current_version, target_version):

    LOGGER.info("Upgrade from %s to %s" % (current_version, target_version))

    current_version = normalize_version(current_version)
    target_version = normalize_version(target_version)    
    
    update_mod = "w20e.pycms.migrations.%s__%s" % \
                 (current_version, target_version)

    try:
        module = __import__(update_mod)
        LOGGER.info("Found upgrade")

        return True

    except:
        LOGGER.warn("No upgrade found")
        
        return False
