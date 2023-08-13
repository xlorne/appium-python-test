import json
import unittest
from appium import webdriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput


capabilities_json = """
{
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "ruby",
    "appPackage": "com.android.settings",
    "appActivity": ".Settings"
}
"""

capabilities = json.loads(capabilities_json)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)
        # 获取屏幕尺寸
        size = self.driver.get_window_size()
        self.width = size['width']
        self.height = size['height']

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:
        # List all the available contexts
        el = self.driver.find_element(by=AppiumBy.ID, value='com.android.settings:id/scroll_headers')
        elements = el.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
        for element in elements:
            print(element.text)

        # 查找并点击电池选项
        el = self.driver.find_element(by=AppiumBy.ID, value='android:id/input')
        el.click()

        search = self.driver.find_element(by=AppiumBy.ID, value='android:id/input')
        search.send_keys('设置')

        self.driver.back()

        # 计算滑动的起始和结束点
        start_x = self.width // 2
        start_y = self.height // 2
        end_x = start_x
        end_y = start_y - self.height // 2

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        # 查找并点击电池选项
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="更多设置"]')
        el.click()

        # 返回上一级
        self.driver.back()


if __name__ == '__main__':
    unittest.main()
