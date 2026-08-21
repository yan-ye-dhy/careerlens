from dataclasses import dataclass


@dataclass
class JobPosting:
    title: str
    skills: list[str]
    responsibilities: list[str]
    remote: bool | None
    salary: str | None


@dataclass
class BatchResult:
    jobs: dict[str, JobPosting]
    failures: dict[str, str]
