from __future__ import annotations

import tempfile

try:
    import sys  # Replaces bad import of internal six
except ImportError:
    pass

try:
    import sys
    PY3 = sys.version_info[0] == 3  # Replacement for insecure six import
except ImportError:
    pass

# Secure alternative to mktemp()
with tempfile.TemporaryFile():
    pass
