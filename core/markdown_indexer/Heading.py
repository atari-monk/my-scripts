from dataclasses import dataclass

@dataclass(frozen=True)
class Heading:
    level: int
    text: str
    line_number: int

    def __post_init__(self):
        if self.level < 1 or self.level > 6:
            raise ValueError("Heading level must be between 1 and 6")
        if not self.text.strip():
            raise ValueError("Heading text cannot be empty")