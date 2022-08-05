from typing import Optional

"""

    Helper Objects for MD5 Search Object from CAPE V2 returned data

"""

class Machines:
    total: int
    available: int

    def __init__(self, total: int, available: int) -> None:
        self.total = total
        self.available = available


class RAM:
    free: int
    total: int
    used: int
    used_by: Optional[str]

    def __init__(self, free: int, total: int, used: int, used_by: Optional[str]) -> None:
        self.free = free
        self.total = total
        self.used = used
        self.used_by = used_by


class Server:
    storage: RAM
    ram: RAM

    def __init__(self, storage: RAM, ram: RAM) -> None:
        self.storage = storage
        self.ram = ram


class Tasks:
    total: int
    pending: int
    running: int
    completed: int
    reported: int

    def __init__(self, total: int, pending: int, running: int, completed: int, reported: int) -> None:
        self.total = total
        self.pending = pending
        self.running = running
        self.completed = completed
        self.reported = reported


class Data:
    version: str
    hostname: str
    machines: Machines
    tasks: Tasks
    server: Server

    def __init__(self, version: str, hostname: str, machines: Machines, tasks: Tasks, server: Server) -> None:
        self.version = version
        self.hostname = hostname
        self.machines = machines
        self.tasks = tasks
        self.server = server


class CapeSandboxStatus:
    error: bool
    data: Data

    def __init__(self, error: bool, data: Data) -> None:
        self.error = error
        self.data = data
