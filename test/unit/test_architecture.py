import ast
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[2] / 'src'


def imported_modules(layer: str) -> set[str]:
    modules: set[str] = set()
    for path in (SRC_DIR / layer).rglob('*.py'):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


@pytest.mark.parametrize(
    ('layer', 'forbidden_prefixes'),
    [
        (
            'domain',
            {
                'fastapi',
                'jose',
                'passlib',
                'pydantic',
                'redis',
                'sqlalchemy',
                'src.application',
                'src.infrastructure',
                'src.presentation',
            },
        ),
        (
            'application',
            {
                'fastapi',
                'jose',
                'passlib',
                'pydantic',
                'redis',
                'sqlalchemy',
                'src.infrastructure',
                'src.presentation',
            },
        ),
    ],
)
def test_layer_dependencies(layer: str, forbidden_prefixes: set[str]):
    violations = {
        module
        for module in imported_modules(layer)
        if any(module == prefix or module.startswith(f'{prefix}.') for prefix in forbidden_prefixes)
    }

    assert not violations, f'{layer} imports forbidden modules: {sorted(violations)}'
