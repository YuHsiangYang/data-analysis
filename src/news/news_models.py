class NewsArticle:
    def __init__(
            self,
            title: str,
            summary: str,
            date: str,
            href: str,
            additional_info: dict = None,
            keywords: list = None
    ):
        self.title = title
        self.summary = summary
        self.date = date
        self.href = href
        self.additional_info = additional_info
        self.keywords = keywords

    def __str__(self):
        return f"{self.title} - {self.date}"

    @classmethod
    def from_dict(cls, dict_: dict):
        return cls(
            dict_["title"],
            dict_["summary"],
            dict_["publication_date"],
            dict_["href"],
            dict_.get("additional_info"),
            dict_.get("keywords")
        )

    def to_dict(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "publication_date": self.date,
            "href": self.href,
            "additional_info": self.additional_info,
            "keywords": self.keywords
        }


class Theme:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def __str__(self):
        return f"{self.title} - {self.description}"

    @classmethod
    def from_dict(cls, dict_: dict):
        return cls(
            title=dict_["title"],
            description=dict_["description"]
        )

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description
        }
