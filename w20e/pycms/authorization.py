from zope.interface import implements

from pyramid.interfaces import IAuthorizationPolicy

from pyramid.location import lineage
from pyramid.security import ACLAllowed
from pyramid.security import ACLDenied
from pyramid.security import Allow
from pyramid.security import Deny
from pyramid.security import Everyone


class ACLAuthorizationPolicy(object):

    implements(IAuthorizationPolicy)

    def permits(self, context, principals, permission):
        """ Return an instance of
        :class:`pyramid.security.ACLAllowed` instance if the policy
        permits access, return an instance of
        :class:`pyramid.security.ACLDenied` if not."""

        acl = '<No ACL found on any object in resource lineage>'

        reg = get_current_registry()
        
        for location in lineage(context):
            try:
                security = reg.getAdapter(location, ISecure)
                acl = security.__acl__
            except AttributeError:
                continue

            for ace in acl:
                ace_action, ace_principal, ace_permissions = ace
                if ace_principal in principals:
                    if not hasattr(ace_permissions, '__iter__'):
                        ace_permissions = [ace_permissions]
                    if permission in ace_permissions:
                        if ace_action == Allow:
                            return ACLAllowed(ace, acl, permission,
                                              principals, location)
                        else:
                            return ACLDenied(ace, acl, permission,
                                             principals, location)

        # default deny (if no ACL in lineage at all, or if none of the
        # principals were mentioned in any ACE we found)
        return ACLDenied(
            '<default deny>',
            acl,
            permission,
            principals,
            context)

    def principals_allowed_by_permission(self, context, permission):
        """ Return the set of principals explicitly granted the
        permission named ``permission`` according to the ACL directly
        attached to the ``context`` as well as inherited ACLs based on
        the :term:`lineage`."""
        allowed = set()

        reg = get_current_registry()        

        for location in reversed(list(lineage(context))):
        
            try:
                security = reg.getAdapter(location, ISecure)
                acl = security.__acl__            
            except AttributeError:
                continue

            allowed_here = set()
            denied_here = set()
            
            for ace_action, ace_principal, ace_permissions in acl:
                if not hasattr(ace_permissions, '__iter__'):
                    ace_permissions = [ace_permissions]
                if (ace_action == Allow) and (permission in ace_permissions):
                    if not ace_principal in denied_here:
                        allowed_here.add(ace_principal)
                if (ace_action == Deny) and (permission in ace_permissions):
                        denied_here.add(ace_principal)
                        if ace_principal == Everyone:
                            # clear the entire allowed set, as we've hit a
                            # deny of Everyone ala (Deny, Everyone, ALL)
                            allowed = set()
                            break
                        elif ace_principal in allowed:
                            allowed.remove(ace_principal)

            allowed.update(allowed_here)

        return allowed
