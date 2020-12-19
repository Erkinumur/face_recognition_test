from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        from facecontrolapp.bot.app import main
        main()
