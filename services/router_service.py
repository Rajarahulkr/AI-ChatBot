class RouterService:

    PDF_KEYWORDS = [
        "pdf",
        "document",
        "resume",
        "report",
        "invoice",
        "uploaded",
        "file",
        "chapter",
        "page"
    ]

    WEB_KEYWORDS = [
        "latest",
        "today",
        "news",
        "current",
        "2026",
        "live",
        "price",
        "weather",
        "stock",
        "score",
        "recent"
    ]

    @staticmethod
    def use_pdf(question):

        question = question.lower()

        return any(
            keyword in question
            for keyword in RouterService.PDF_KEYWORDS
        )

    @staticmethod
    def use_web(question):

        question = question.lower()

        return any(
            keyword in question
            for keyword in RouterService.WEB_KEYWORDS
        )