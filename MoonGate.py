import asyncio
from playwright.async_api import async_playwright, expect

class MoonGate:
    def __init__(self):
        self.mm_page = ""

    async def open_moongate_page(self, context, mm_page):
        await mm_page.goto("https://app.moongate.id/discover")
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await asyncio.sleep(10)

        print(mm_page)
        mm_page = context.pages[1]
        print(mm_page)

        await mm_page.wait_for_load_state()

        self.mm_page = mm_page

    async def switch_to_last_page(self, pages):
        last_page = pages[-1]
        await last_page.bring_to_front()

    async def login_to_moongate(self, context, seed_phrase):
        await self.mm_page.locator("button:has-text('Login / Sign Up')").first.click()

        await self.mm_page.locator("p:has-text('Wallet')").click()

        await asyncio.sleep(5)

        await self.mm_page.get_by_text('MetaMask').click()
        await asyncio.sleep(10)

        pages = context.pages
        print(pages)
        self.mm_page = context.pages[-1]
        await self.switch_to_last_page(pages)
        await asyncio.sleep(5)

        terms_button_7 = self.mm_page.get_by_test_id(test_id="page-container-footer-next")
        await expect(terms_button_7).to_be_enabled()
        await terms_button_7.click()

        await asyncio.sleep(5)

        terms_button_8 = self.mm_page.get_by_test_id(test_id="page-container-footer-next")
        await expect(terms_button_8).to_be_enabled()
        await terms_button_8.click()
        await asyncio.sleep(3)

        self.mm_page = context.pages[1]
        await self.mm_page.wait_for_load_state()

        await self.mm_page.locator("button:has-text('Confirm')").first.click()

        await asyncio.sleep(5)

        pages = context.pages
        self.mm_page = context.pages[-1]
        await self.switch_to_last_page(pages)

        terms_button_9 = self.mm_page.get_by_test_id(test_id="page-container-footer-next")
        await expect(terms_button_9).to_be_enabled()
        await terms_button_9.click()

        self.mm_page = context.pages[1]
        await self.mm_page.wait_for_load_state()
        await asyncio.sleep(5)
        await self.mm_page.wait_for_load_state(state='domcontentloaded')
        await asyncio.sleep(10)

    async def open_events(self):
        first_element_index = 15
        last_el_index = 0

        # blue - event_index = 2
        # gray - event_index = 1
        for event_index in (2, 1):
            for el in range(first_element_index, last_el_index, -1):
                await self.mm_page.click(
                    f'//*[@id="__next"]/div[1]/main/div/div/div[2]/main/div[2]/div/div/div[{event_index}]/div[{el}]')
                await asyncio.sleep(1)  # 2

            first_element_index = 6
            last_el_index = 1

        await self.mm_page.wait_for_load_state(state='domcontentloaded')
        await asyncio.sleep(10)

    async def get_tasks(self):
        return await self.mm_page.query_selector_all("section")

    async def open_tasks(self):
        tasks = await self.get_tasks()

        print("START CLICK TASKS")

        for task in tasks:
            print(await task.text_content())
            await task.click()
            await asyncio.sleep(2)  # 6

            await self.complete_task()

            await asyncio.sleep(1)  # 3

    async def complete_task(self):
        try:
            await self.mm_page.locator("p:has-text('follow event')").click()
            await self.mm_page.locator("p:has-text('share event')").click()
            await asyncio.sleep(7)
            await self.mm_page.locator(
                'path[d="M0.500122 19.5L19.5001 19.5L19.5001 0.500002L0.500124 0.5L0.500122 19.5Z"]').click()

        except Exception as ex:
            print(ex)
            await self.mm_page.locator(
                'path[d="M0.500122 19.5L19.5001 19.5L19.5001 0.500002L0.500124 0.5L0.500122 19.5Z"]').click()

    async def get_mm_page(self):
        return self.mm_page