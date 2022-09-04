class ip2infres:
    def __init__(self, domain, ip, loc, mail, name, tel, services, others):
        self.domain = domain
        self.ip = ip
        self.loc = loc
        self.mail = mail
        self.name = name
        self.tel = tel
        self.services = services
        self.others = others

    def to_string(self):
        res = ''
        res += str(self.ip) + '\n'
        res += str(self.loc) + '\n'
        res += 'dom' + self.list_to_string(self.domain)
        res += 'mail' + self.list_to_string(self.mail)
        res += 'nam' + self.list_to_string(self.name)
        res += 'tel' + self.list_to_string(self.tel)
        res += str(self.services) + '\n'
        res += str(self.others)
        return res

    def list_to_string(self, l):
        t = ''
        if isinstance(l, list):
            for it in l:
                t += '--' + it + '\n'
            return t
        else:
            return str(t) + '\n'
