from collections import deque
import os
import pathlib

from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata
from django.db import connection


PATH = pathlib.Path(__file__).parent.resolve()
QUERY = """SELECT
  TABLE_NAME AS table_name,
  REFERENCED_TABLE_NAME AS reference_table_name
FROM
  information_schema.KEY_COLUMN_USAGE"""


class Command(BaseCommand):
    help = 'dependency_load_fixture'

    def handle(self, *args, **options):
        fixture_files = set()
        for _root, _dirs, files in os.walk(PATH.parent.parent / 'fixtures'):
            for file in files:
                if file.endswith('.json'):
                    fixture_files.add(file.removesuffix('.json'))

        dependency_map: dict[str, set[str]] = dict()
        rows = self._get_table_dependency()
        for row in rows:
            s: set[str] = set()
            if dependency_map.get(row['table_name']):
                s = dependency_map.get(row['table_name'])
            if row['reference_table_name'] is not None:
                s.add(row['reference_table_name'])
            dependency_map[row['table_name']] = s

        sorted_list = self._topological_sort(dependency_map)
        print(sorted_list)

        fixture_target = [
            table_name
            for table_name in sorted_list
            if table_name in fixture_files
        ]

        management.call_command(loaddata.Command(), *fixture_target, verbosity=0)

    def _get_table_dependency(self):
        with connection.cursor() as cursor:
            cursor.execute(QUERY)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return rows

    def _topological_sort(self, dependency_map: dict[str, set[str]]) -> list[str]:
        all_tables = set(dependency_map.keys())
        # { テーブル名: 入次数 }
        in_degree: dict[str, int] = dict()
        # 依存先から依存しているテーブルの一覧を作成
        graph = {table: [] for table in dependency_map.keys()}
        # グラフと入次数の計算
        for table, deps in dependency_map.items():
            in_degree[table] = len(deps)
            for dep in deps:
                graph[dep].append(table)

        # 現時点で入次数が 0 の頂点をすべてキューに追加する
        queue = deque([table for table, degree in in_degree.items() if degree == 0])
        # 結果（トポロジカル順序）を格納する配列
        sorted_list: list[str] = []

        while queue:
            # 入次数が 0 の頂点を 1 つ取り出す
            table = queue.popleft()
            # トポロジカル順序に追加する
            sorted_list.append(table)
            # その頂点から出る各辺について
            # その先の頂点の入次数を減らし、新たに 0 になったらキューに追加する
            for dependent in graph[table]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # 閉路が存在する（頂点をすべて処理できていない）場合
        if len(sorted_list) != len(all_tables):
            closed_circuit = ', '.join([
                table
                for table, degree in in_degree.items()
                if degree > 0
            ])
            raise ValueError(f'{closed_circuit} で閉路を検出')

        return sorted_list
