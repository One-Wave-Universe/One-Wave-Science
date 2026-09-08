"""Domain adapters for the problem-builder core.

Adapters are registered explicitly, never discovered automatically. Call
register_default_adapters() to register the adapters that ship with this
package, or register your own directly via parser.adapter.register_adapter()
-- either way, registration is one obvious function call, not import-time
magic.
"""

from ..adapter import register_adapter
from .math_basic_equations import DOMAIN as MATH_BASIC_EQUATIONS_DOMAIN
from .math_basic_equations import MathBasicEquationsAdapter


def register_default_adapters(*, replace: bool = False) -> None:
    register_adapter(MATH_BASIC_EQUATIONS_DOMAIN, MathBasicEquationsAdapter(), replace=replace)


__all__ = [
    "MATH_BASIC_EQUATIONS_DOMAIN",
    "MathBasicEquationsAdapter",
    "register_default_adapters",
]
