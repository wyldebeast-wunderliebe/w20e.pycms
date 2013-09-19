import logging


LOGGER = logging.getLogger("pycms")


def normalize_version(version):

    return version.replace(".", "_").replace("-", "_")


def migrate(app, current_version, target_version):

    LOGGER.info("Upgrade from %s to %s" % (current_version, target_version))

    current_version = normalize_version(current_version)
    target_version = normalize_version(target_version)    
    
    update_mod = "w20e.pycms.migrations.%s__%s" % \
                 (current_version, target_version)

    updated = False

    try:
        mod = __import__(update_mod, globals(), locals(), ['migrate'], -1)
        LOGGER.info("Found upgrade")
        updated = mod.migrate(app)
    except:
        pass

    if not updated:

        # Maybe no from version?
        #
        update_mod = "w20e.pycms.migrations.any__%s" % target_version

        try:
            mod = __import__(update_mod, globals(), locals(), ['migrate'], -1)
            LOGGER.info("Found upgrade")
            updated = mod.migrate(app)
        except:
            LOGGER.exception("Couldn't upgrade")

    return updated
