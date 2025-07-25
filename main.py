import asyncio, json, re
from playwright.async_api import async_playwright

GROUP_URL = "https://www.facebook.com/messages/t/9531602573607816/"

async def run_bot():
    print("🤖 Bot is live. Listening for commands...\n")

    with open("fbstate.json", "r") as f:
        cookies = json.load(f)

    with open("commands.json", "r") as f:
        commands = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="fbstate.json")
        page = await context.new_page()

        await page.goto(GROUP_URL)
        await page.wait_for_selector('div[role="row"] div[dir="auto"]', timeout=15000)
        print("✅ Loaded group chat.")

        seen = set()

        while True:
            messages = await page.query_selector_all('div[role="row"] div[dir="auto"]')
            for msg in messages[-10:]:
                text = await msg.inner_text()
                if text not in seen:
                    seen.add(text)
                    print("📨", text)

                    for cmd in commands:
                        if text.lower().startswith(cmd["command"].lower()):
                            reply = cmd["reply"]
                            await page.type('div[aria-label="Message"]', reply)
                            await page.keyboard.press("Enter")
                            print(f"⚙️ Replied to command: {cmd['command']}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_bot())
