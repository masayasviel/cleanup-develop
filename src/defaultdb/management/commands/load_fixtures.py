from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata
from django.db import connection


QUERY = """SELECT
  TABLE_NAME AS table_name,
  REFERENCED_TABLE_NAME AS reference_table_name
FROM
  information_schema.KEY_COLUMN_USAGE"""


class Command(BaseCommand):
    help = 'dependency_load_fixture'

    def handle(self, *args, **options):
        dependency_map: dict[str, set[str]] = dict()
        rows = self._get_table_dependency()
        for row in rows:
            s = set()
            if dependency_map.get(row['table_name']):
                s = dependency_map.get(row['table_name'])
            if row['reference_table_name'] is not None:
                s.add(row['reference_table_name'])
            dependency_map[row['table_name']] = s

        sorted = self._topological_sort(dependency_map)

        print(sorted)

    def _get_table_dependency(self):
        with connection.cursor() as cursor:
            cursor.execute(QUERY)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return rows

    def _topological_sort(self, dependency_map: dict[str, set[str]]) -> list[str]:
        sorted_list: list[str] = []
        visited = set()
        temp_marked = set()

        def visit(table_name: str) -> None:
            if table_name in temp_marked:
                raise ValueError(f'{table_name} で閉路を検出')
            if table_name not in visited:
                temp_marked.add(table_name)
                dependencies = dependency_map.get(table_name) or set()
                for dep in dependencies:
                    visit(dep)
                temp_marked.remove(table_name)
                visited.add(table_name)
                sorted_list.append(table_name)

        for table_name in dependency_map.keys():
            if table_name not in visited:
                visit(table_name)

        return sorted_list
