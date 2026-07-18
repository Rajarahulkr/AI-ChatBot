from tavily import TavilyClient
from config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


class WebService:

    @staticmethod
    def search(query):

        try:

            result = client.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )

            context = ""

            for item in result["results"]:

                context += f"""
Title: {item['title']}

Content:
{item['content']}

Source:
{item['url']}

------------------------------------

"""

            return context.strip()

        except Exception:

            return ""