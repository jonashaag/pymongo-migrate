import importlib.util
from pathlib import Path
from typing import Generator

from pymongo_migrate.migrations import MigrationModuleWrapper


def load_module_migrations(
    path: Path, namespace=f"{__name__}._migrations"
) -> Generator[MigrationModuleWrapper, None, None]:

    for module_file in path.iterdir():
        migration_name = module_file.stem
        spec = importlib.util.spec_from_file_location(
            f"{namespace}.{migration_name}", str(module_file)
        )
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)  # type: ignore
        yield MigrationModuleWrapper(  # type: ignore
            name=migration_name, module=migration_module
        )