# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# AppInfo


class AppInfo:
    @staticmethod
    def name():
        return "Petete"
    
    @staticmethod
    def author():
        return "Baltasar"
    
    @staticmethod
    def version():
        return "v0.1 20260421" 
    
    @staticmethod
    def title():
        return f"{AppInfo.name()} {AppInfo.version()}"

    @staticmethod
    def complete_title():
        return f"{AppInfo.name()} ({AppInfo.author()}) {AppInfo.version()}"
