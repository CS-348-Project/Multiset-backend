from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from glob import glob
import json
from os import makedirs

from multiset.db_utils import execute_query
from multiset.seeding.prod import ProductionSeeder


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ProductionSeeder().seed()
