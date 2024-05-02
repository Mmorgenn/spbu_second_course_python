import requests
from bs4 import BeautifulSoup


class BashQuotes:
    URL_BEST = "https://xn--80abh7bk0c.xn--p1ai/best/2024"
    URL_RANDOM = "https://xn--80abh7bk0c.xn--p1ai/random"
    URL_NEW = "https://xn--80abh7bk0c.xn--p1ai"

    @staticmethod
    def req_quotes(url: str, count: int = 10, new: bool = False) -> str:
        start = 0
        if new:
            count += 1
            start = 1
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            quote_list = soup.findAll("div", class_="quote__body")
            quote_list = quote_list[start:count]
            quote_list = list(map(lambda x: x.get_text().strip(), quote_list))
            return "#  " + "\n#  ".join(quote_list)
        return "Error"

    async def get_quote(self, type_quote: str) -> str:
        match type_quote:
            case "new":
                return self.req_quotes(self.URL_NEW, new=True)
            case "best":
                return self.req_quotes(self.URL_BEST)
            case "random":
                return self.req_quotes(self.URL_RANDOM)
            case default:
                return "Error"
