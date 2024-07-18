from pathlib import Path
from typing import override

from tap import Tap


class Args(Tap):
    core: Path  # pyright: ignore[reportUninitializedInstanceVariable]
    host: str = "127.0.0.1"
    port: int = 8000

    @override
    def configure(self) -> None:
        self.add_argument("core", metavar="<DIRECTORY>",
                          help="path to Elect.Gen Core")  # pyright: ignore[reportUnknownMemberType]
        self.add_argument("--host", metavar="<IPv4>",
                          help="bind socket to this host")  # pyright: ignore[reportUnknownMemberType]
        self.add_argument(  # pyright: ignore[reportUnknownMemberType]
            "--port",
            metavar="<USHORT>",
            help="bind socket to this port (if 0, an available port will be picked)",
        )
