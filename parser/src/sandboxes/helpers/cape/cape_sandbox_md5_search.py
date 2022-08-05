from datetime import datetime
from typing import List

"""

    Search Object Decoded from CAPE V2 returned data

"""

class Datum:
    id: int
    target: str
    category: str
    cape: str
    timeout: int
    priority: int
    custom: str
    machine: str
    package: str
    route: bool
    tags_tasks: None
    options: str
    platform: str
    memory: bool
    enforce_timeout: bool
    clock: datetime
    added_on: datetime
    started_on: datetime
    completed_on: None
    status: str
    dropped_files: None
    running_processes: None
    api_calls: None
    domains: None
    signatures_total: None
    signatures_alert: None
    files_written: None
    registry_keys_modified: None
    crash_issues: None
    anti_issues: None
    analysis_started_on: None
    analysis_finished_on: None
    processing_started_on: None
    processing_finished_on: None
    signatures_started_on: None
    signatures_finished_on: None
    reporting_started_on: None
    reporting_finished_on: None
    timedout: bool
    sample_id: int
    machine_id: int
    shrike_url: None
    shrike_refer: None
    shrike_msg: None
    shrike_sid: None
    parent_id: None
    tlp: None
    user_id: int
    username: bool
    tags: List[str]

    def __init__(self, id: int, target: str, category: str, cape: str, timeout: int, priority: int, custom: str, machine: str, package: str, route: bool, tags_tasks: None, options: str, platform: str, memory: bool, enforce_timeout: bool, clock: datetime, added_on: datetime, started_on: datetime, completed_on: None, status: str, dropped_files: None, running_processes: None, api_calls: None, domains: None, signatures_total: None, signatures_alert: None, files_written: None, registry_keys_modified: None, crash_issues: None, anti_issues: None, analysis_started_on: None, analysis_finished_on: None, processing_started_on: None, processing_finished_on: None, signatures_started_on: None, signatures_finished_on: None, reporting_started_on: None, reporting_finished_on: None, timedout: bool, sample_id: int, machine_id: int, shrike_url: None, shrike_refer: None, shrike_msg: None, shrike_sid: None, parent_id: None, tlp: None, user_id: int, username: bool, tags: List[str]) -> None:
        self.id = id
        self.target = target
        self.category = category
        self.cape = cape
        self.timeout = timeout
        self.priority = priority
        self.custom = custom
        self.machine = machine
        self.package = package
        self.route = route
        self.tags_tasks = tags_tasks
        self.options = options
        self.platform = platform
        self.memory = memory
        self.enforce_timeout = enforce_timeout
        self.clock = clock
        self.added_on = added_on
        self.started_on = started_on
        self.completed_on = completed_on
        self.status = status
        self.dropped_files = dropped_files
        self.running_processes = running_processes
        self.api_calls = api_calls
        self.domains = domains
        self.signatures_total = signatures_total
        self.signatures_alert = signatures_alert
        self.files_written = files_written
        self.registry_keys_modified = registry_keys_modified
        self.crash_issues = crash_issues
        self.anti_issues = anti_issues
        self.analysis_started_on = analysis_started_on
        self.analysis_finished_on = analysis_finished_on
        self.processing_started_on = processing_started_on
        self.processing_finished_on = processing_finished_on
        self.signatures_started_on = signatures_started_on
        self.signatures_finished_on = signatures_finished_on
        self.reporting_started_on = reporting_started_on
        self.reporting_finished_on = reporting_finished_on
        self.timedout = timedout
        self.sample_id = sample_id
        self.machine_id = machine_id
        self.shrike_url = shrike_url
        self.shrike_refer = shrike_refer
        self.shrike_msg = shrike_msg
        self.shrike_sid = shrike_sid
        self.parent_id = parent_id
        self.tlp = tlp
        self.user_id = user_id
        self.username = username
        self.tags = tags


class CapeSandboxMD5Search:
    error: bool
    data: List[Datum]

    def __init__(self, error: bool, data: List[Datum]) -> None:
        self.error = error
        self.data = data
