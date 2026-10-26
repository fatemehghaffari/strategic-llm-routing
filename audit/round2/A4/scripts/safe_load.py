"""Restricted unpickler for the RouterBench .pkl files.

The published artefacts are Python pickles, which can execute arbitrary code on
load.  We therefore refuse every global except the handful of numpy/pandas
constructors a DataFrame pickle legitimately needs.  If a file needs anything
else, the load fails loudly instead of silently running it.
"""
import io
import pickle

ALLOWED_MODULE_PREFIXES = (
    "numpy",
    "pandas",
    "collections",
    "builtins",
    "copyreg",
    "_codecs",
)
DENIED_NAMES = {
    ("builtins", "eval"),
    ("builtins", "exec"),
    ("builtins", "compile"),
    ("builtins", "open"),
    ("builtins", "__import__"),
    ("builtins", "getattr"),
}


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in DENIED_NAMES:
            raise pickle.UnpicklingError(f"denied global {module}.{name}")
        if not any(module == p or module.startswith(p + ".") for p in ALLOWED_MODULE_PREFIXES):
            raise pickle.UnpicklingError(f"denied module {module} (name {name})")
        return super().find_class(module, name)


def safe_read_pickle(path):
    with open(path, "rb") as fh:
        return RestrictedUnpickler(io.BytesIO(fh.read())).load()
