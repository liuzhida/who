import ldap

LDAP_HOST = "ldap.corp.wandoujia.com"
LDAP_DN = "ou=People,dc=wandoujia,dc=com"
LDAP_USER = "cn=root,dc=wandoujia,dc=com"


class LdapAuth(object):

    def __init__(self, ldap_host=LDAP_HOST):
        self.ldap_host = ldap_host

    def auth(self, user, passwd):
        self.dn = 'uid=%s,ou=People,dc=wandoujia,dc=com' % user
        self.ldapconn = ldap.initialize('ldap://%s' % self.ldap_host)
        try:
            self.ldapconn.simple_bind_s(self.dn, passwd)
            self.ldapconn.unbind()
            return True
        except Exception as e:
            self.ldapconn.unbind()
            return False


def Auth(user, password):
    demo = LdapAuth()
    return demo.auth(user, password)
