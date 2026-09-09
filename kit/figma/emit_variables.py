"""Import shim: exposes emit-variables-script.py's collect() under an importable name."""
import importlib.util
import os

_spec = importlib.util.spec_from_file_location("emit_variables_script", os.path.join(os.path.dirname(os.path.abspath(__file__)), "emit-variables-script.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
collect = _mod.collect
