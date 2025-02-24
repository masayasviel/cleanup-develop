from collections import deque

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
            s: set[str] = set()
            if dependency_map.get(row['table_name']):
                s = dependency_map.get(row['table_name'])
            if row['reference_table_name'] is not None:
                s.add(row['reference_table_name'])
            dependency_map[row['table_name']] = s

        sorted_list = self._topological_sort(dependency_map)

        print(sorted_list)

    def _get_table_dependency(self):
        with connection.cursor() as cursor:
            cursor.execute(QUERY)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return rows

    def _topological_sort(self, dependency_map: dict[str, set[str]]) -> list[str]:
        all_tables = set(dependency_map.keys())
        for deps in dependency_map.values():
            all_tables |= deps

        # 各テーブルの依存数（入次数）を初期化する
        in_degree = {table: 0 for table in all_tables}
        # 逆方向のグラフ: 依存先から依存しているテーブルの一覧を作成
        graph = {table: [] for table in all_tables}
        # グラフと入次数の構築
        for table, deps in dependency_map.items():
            in_degree[table] = len(deps)
            for dep in deps:
                graph[dep].append(table)

        # 入次数が0のテーブルをキューに追加（幅優先探索の開始点）
        queue = deque([table for table, degree in in_degree.items() if degree == 0])
        sorted_list = []

        while queue:
            table = queue.popleft()
            sorted_list.append(table)
            for dependent in graph[table]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # 全テーブルが処理されなかった場合は閉路が存在する
        if len(sorted_list) != len(all_tables):
            for table, degree in in_degree.items():
                if degree > 0:
                    raise ValueError(f'{table} で閉路を検出')

        return sorted_list
