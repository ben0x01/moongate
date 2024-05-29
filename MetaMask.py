import asyncio
from playwright.async_api import async_playwright, expect

class MetaMask:
    def __init__(self, MM_PASSWORD):
        self.mm_page = ""
        self.MM_PASSWORD = MM_PASSWORD

    def get_mm_page(self):
        return self.mm_page

    async def open_metamask(self, context):
        if len(context.background_pages) == 0:
            background_page = await context.wait_for_event('backgroundpage')
        else:
            background_page = await context.background_pages[0]

        titles = []

        while "MetaMask" not in titles:
            titles = [await p.title() for p in context.pages]

        mm_page = context.pages[1]

        await mm_page.wait_for_load_state()

        self.mm_page = mm_page

    async def login_to_metamask(self, seed_phrase):
        await asyncio.sleep(1)
        checkbox = self.mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await self.mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        import_wallet = self.mm_page.get_by_test_id(test_id="onboarding-import-wallet")
        await expect(import_wallet).to_be_enabled()
        await import_wallet.click()

        i_dont_agree = self.mm_page.get_by_test_id(test_id="metametrics-no-thanks")
        await expect(i_dont_agree).to_be_enabled()
        await i_dont_agree.click()

        for i in range(12):
            await self.mm_page.get_by_test_id(test_id=f'import-srp__srp-word-{i}').fill(seed_phrase[i])

        confirm_seed = self.mm_page.get_by_test_id(test_id="import-srp-confirm")
        await expect(confirm_seed).to_be_enabled()
        await confirm_seed.click()

        await self.mm_page.get_by_test_id(test_id='create-password-new').fill(self.MM_PASSWORD)
        await self.mm_page.get_by_test_id(test_id='create-password-confirm').fill(self.MM_PASSWORD)
        terms_button = self.mm_page.get_by_test_id(test_id="create-password-terms")
        await expect(terms_button).to_be_enabled()
        await terms_button.click()

        terms_button_2 = self.mm_page.get_by_test_id(test_id="create-password-import")
        await expect(terms_button_2).to_be_enabled()
        await terms_button_2.click()

        terms_button_3 = self.mm_page.get_by_test_id(test_id="onboarding-complete-done")
        await expect(terms_button_3).to_be_enabled()
        await terms_button_3.click()

        terms_button_4 = self.mm_page.get_by_test_id(test_id="onboarding-complete-done")
        await expect(terms_button_4).to_be_enabled()
        await terms_button_4.click()

        terms_button_5 = self.mm_page.get_by_test_id(test_id="pin-extension-next")
        await expect(terms_button_5).to_be_enabled()
        await terms_button_5.click()

        terms_button_6 = self.mm_page.get_by_test_id(test_id="pin-extension-done")
        await expect(terms_button_6).to_be_enabled()
        await terms_button_6.click()
