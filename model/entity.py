# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# User


import sirope


class Entity:
    def save(self, srp: sirope.Sirope):
        oid = srp.save(self)
        if not hasattr(self, "safe_id"):
            self.safe_id = srp.safe_from_oid(oid)
            srp.save(self)

    @staticmethod
    def load_from_safe_oid(srp: sirope.Sirope, safe_oid: str) -> Self:
        return srp.load(srp.oid_from_safe(safe_oid))
