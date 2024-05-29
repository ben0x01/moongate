import asyncio
import aiofiles
from playwright.async_api import async_playwright, expect
import MetaMask
import MoonGate

class Main:
    def __init__(self, seed):
        self.EXTENSIONS_PATH = r"C:\Users\glazy\AppData\Local\Google\Chrome\User Data\Default\Extensions\nkbihfbeogaeaoehlefnkodbefgpgknn\11.16.0_0"
        self.MM_PASSWORD = "B7601As5T78"
        self.SEED_PHRASE = ["food", "report", "vanish", "faint", "gown", "expose", "please", "mandate", "birth", "elegant", "find", "cotton"]
        self.mm_page = ""
        self.seed_phrase = seed

    async def main(self):
        async with async_playwright() as p:
            context = await self.get_context(p)

            await self.perform_actions_with_metamask(context)

            await self.perform_actions_with_moongate(context)

            await self.write_results()

    async def perform_actions_with_metamask(self, context):
        metamask = MetaMask.MetaMask(self.MM_PASSWORD)

        await metamask.open_metamask(context)

        self.mm_page = metamask.get_mm_page()

        await metamask.login_to_metamask(self.seed_phrase)

    async def perform_actions_with_moongate(self, context):
        moongate = MoonGate.MoonGate()

        await moongate.open_moongate_page(context, self.mm_page)

        await moongate.login_to_moongate(context, self.seed_phrase)

        self.mm_page = await moongate.get_mm_page()

        await moongate.open_events()

        await moongate.open_tasks()

    async def write_file(self, filename, seed, text):
        async with aiofiles.open(filename, mode='a') as f:
            await f.write(seed + " - " + text + '\n')

    async def get_context(self, p):
        return await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                f"--disable-extensions-except={self.EXTENSIONS_PATH}",
                f"--load-extension={self.EXTENSIONS_PATH}"],
        # proxy={
        #     'server': f"{ip}:{port}",
        #     'username': f'{username}',
        #     'password': f'{password}',
        #
        # },
    )

    async def write_results(self):
        points = self.get_points()
        seed_to_string = " ".join(self.seed_phrase)
        await self.write_file("results.txt", seed_to_string, await points)

    async def get_points(self):
        pts_element = await self.mm_page.query_selector("span.font-semibold.uppercase.text-primary-300")
        pts_text = await pts_element.text_content()
        return pts_text.split(" / ")[0]

if __name__ == "__main__":
    with open('seed.txt', 'r') as file:
        data = [line.strip() for line in file.readlines()]


    for line in data:
        seed = line.split()

        main = Main(seed)
        asyncio.run(main.main())







        