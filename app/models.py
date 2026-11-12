
from dataclasses import dataclass, asdict


@dataclass
class Record:
    cheat_sheet: str
    vulnerability: str
    recommended_control: str
    exact_parameter: str
    owasp_top10_category: str
    source_url: str

    def to_dict(self):
        return asdict(self)
