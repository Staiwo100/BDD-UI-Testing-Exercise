# ─────────────────────────────────────────────────────────────────
# FILE: features/steps/task_steps.py
#
# This file connects your Gherkin steps to real browser actions.
# Every @given / @when / @then below must match a step in your
# task_tracker.feature file EXACTLY (spelling, spaces, quotes).
# ─────────────────────────────────────────────────────────────────

# Import the Behave decorators that mark each function as a step
from behave import given, when, then

# Import Playwright's synchronous API (sync = step-by-step, not async)
from playwright.sync_api import sync_playwright

# ── STEP 1: Navigate to the app ──────────────────────────────────
# This @given matches: Given the user navigates to "http://localhost:5000"
# The {url} in curly braces captures the quoted URL from the feature file
# and passes it into this function as the `url` parameter.
@given('the user navigates to "{url}"')
def step_navigate(context, url):
    # Start the Playwright engine — must be done before opening a browser
    context.playwright = sync_playwright().start()
    # Launch a Chromium browser; headless=True means it runs invisibly
    # Change to headless=False to WATCH the browser during debugging
    context.browser = context.playwright.chromium.launch(headless=True)
    # Open a new browser tab (called a "page" in Playwright)
    context.page = context.browser.new_page()
    # Navigate to the URL from the feature file (e.g. http://localhost:5000)
    context.page.goto(url)

# ── STEP 2: Confirm we are on the task list page ─────────────────
# This @given matches: Given the user is on the task list page
# wait_for_selector pauses until the element with that ID appears on screen.
@given("the user is on the task list page")
def step_on_page(context):
    # Replace ___ with the ID selector for the task list  →  "#task-list"
    context.page.wait_for_selector("#task-list")

# ── STEP 3: Add a task ───────────────────────────────────────────
# This @when matches: When the user adds a task "Buy milk"
# The {task_title} captures "Buy milk" from the feature file.
@when('the user adds a task "{task_title}"')
def step_add_task(context, task_title):
    # fill() types text into a field; replace ___ with "#task-input"
    context.page.fill("#task-input", task_title)
    # click() clicks a button; replace ___ with "#add-btn"
    context.page.click("#add-btn")

# ── STEP 4: Submit the form with no text typed ───────────────────
# This @when matches: When the user submits an empty task
# We fill the input with "" (an empty string) to clear it, then click Add.
@when("the user submits an empty task")
def step_empty_task(context):
    # Clear the task input field by filling it with nothing ("")
    context.page.fill("#task-input", "")
    # Click Add — this should trigger the app's validation error
    context.page.click("#add-btn")

# ── STEP 5: Verify the task appears in the list ──────────────────
# This @then matches: Then the task list should contain "Buy milk"
# We read all the text from the task list and assert our task is in it.
@then('the task list should contain "{task_title}"')
def step_check_list(context, task_title):
    # Wait until the task list element is visible on the page
    context.page.wait_for_selector("#task-list")
    # text_content() reads all visible text inside the element
    # Replace ___ with the ID selector for the task list  →  "#task-list"
    list_text = context.page.text_content("#task-list")
    # assert checks that task_title appears somewhere in the list text
    # If it does NOT, the test fails and shows this error message
    assert task_title in list_text, \
        f"Expected '{task_title}' in list but got: {list_text}"

# ── STEP 6: Verify an error message is shown ─────────────────────
# This @then matches: Then an error message "Task cannot be empty" should be displayed
# Same pattern: wait for element → read its text → assert the message is there.
@then('an error message "{message}" should be displayed')
def step_check_error(context, message):
    # Wait until the error paragraph appears; replace ___ with "#error-msg"
    context.page.wait_for_selector("#error-msg")
    # Read the text of the error element; replace ___ with "#error-msg"
    error_text = context.page.text_content("#error-msg")
    # Assert the expected error message text is somewhere in that element
    assert message in error_text, \
        f"Expected error '{message}' but got: {error_text}"
