from session import Session
import time
import os


class Poskmark(Session):
    HOME_PAGE = "https://poshmark.com/create-listing"

    def __init__(self, browser, sale_product, category):
        super(Poskmark, self).__init__(browser)
        self.sale_product = sale_product
        self.category = category

    def __upload_image(self, files: list):
        """上传图片"""
        path_split_by_newline = '\n'.join(files)

        self.browser.send_keys(
            '//*[@id="img-file-input"]', path_split_by_newline)

        modal_xpath = '//*[@id="imagePlaceholder"]//div[@class="modal__body"]'
        time.sleep(3)
        button_xpath = '//button[@data-et-on-name="edit_covershot"]'
        self.browser.click(button_xpath)

    def __set_title(self, title):
        """设置标题"""
        self.browser.send_keys('//input[@data-vv-name="title"]', title)

    def __set_description(self, description):
        """设置简介"""
        self.browser.send_keys(
            '//textarea[@data-vv-name="description"]', description)

    def __set_category(self, parent, selection, sub=None):
        """设置产品类别"""

        self.browser.click('//span[@data-et-name="category"]')

        self.browser.click(f'//a[@data-et-name="{parent.lower()}"]')

        options = self.browser.find_elements_by_xpath(
            '//li[@data-et-on-name="category_selection"]')

        selection_category = self.category[parent].get(selection)
        selection_index = selection_category.get("index")
        options[selection_index].click()

        if sub:
            children = selection_category.get("children").get(sub)
            children_index = children.get("index")
            subcategories = self.browser.find_elements_by_xpath(
                '//a[@data-et-name="subcategory"]')

            subcategories[children_index].click()

    def _set_size(self, category, value):
        self.browser.click('//div[@data-et-name="size"]')

        category_xpath = '//a[@data-test="horizontal-nav-tab"]'
        categories = self.browser.find_elements_by_xpath(category_xpath)
        for element in categories:
            if element.text == category:
                time.sleep(3)
                element.click()
                time.sleep(1)
                self.browser.click(f'//button[@id="size-{value}"]')
                return True

        return False

    def __click_next(self):
        """点击下一步"""
        xpath = '//button[@data-et-name="next"]'
        self.browser.click(xpath)

    def __set_sell_price(self, price):
        """设置销售价格"""
        self.browser.send_keys(
            '//input[@data-vv-name="listingPrice"]', int(price))

    def __set_original_price(self, price):
        """设置原始价格"""
        self.browser.send_keys(
            '//input[@data-vv-name="originalPrice"]', int(price))

    def __submit(self):
        print("点击提交")
        submit_button = '//button[@data-testid="ListButton"]'
        i = 0
        while i < 3 and self.browser.is_display(submit_button):
            self.browser.click(submit_button, time_sleep=1)
            i = i + 1
            time.sleep(30)

    def is_block(self):
        flag_xpath = '//*[@id="app"]/main/div[1]/div/div[2]/div[3]/div/button'
        try:
            button = self.browser.find_element_by_xpath(flag_xpath)
            button.click()
            return True
        except Exception as e:
            return False

    def execute(self):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        self.browser.get(self.HOME_PAGE)
        time.sleep(10)
        sale_product = self.sale_product
        is_block = self.is_block()
        if is_block:
            print("账号已经被锁")

        self.__upload_image(sale_product.blob_list)
        self.__set_title(sale_product.title)
        self.__set_description(sale_product.description)
        self.__set_category(*sale_product.category)
        self._set_size(*sale_product.size)
        self.__set_original_price(sale_product.original_price)
        self.__set_sell_price(sale_product.listing_price)
        self.__click_next()
