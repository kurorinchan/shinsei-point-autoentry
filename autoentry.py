import argparse
import logging
from selenium import webdriver
import time
import sys

_POINT_ENTRY_URL = 'https://www.shinseibank.com/service/point/'


def _FillTPointNumber(driver, t_number):
    # T point has 16 digit version and 9 digit version. Switch based on length.
    driver.find_element_by_xpath(
        "//input[@id='r-point_t']/following-sibling::label").click()
    if len(t_number) == 16:
        driver.find_element_by_xpath(
            "//input[@id='point_t_16']/following-sibling::label").click()
        driver.find_element_by_id('fi_point_t16').send_keys(t_number)
    elif len(t_number) == 9:
        driver.find_element_by_xpath(
            "//input[@id='fi_point_t_9']/following-sibling::label").click()
        driver.find_element_by_id('fi_point_t9').send_keys(t_number)
    else:
        logging.error(
            f'{t_number} is not a valid T point number must be 16 or 9 chars!!'
        )
        sys.exit(1)


def _FillDPointNumber(driver, d_number):
    driver.find_element_by_xpath(
        "//input[@id='r-point_d']/following-sibling::label").click()
    if len(d_number) != 12:
        logging.error(
            f'{d_number} is not a valid D point number must be 12 chars!!')
        sys.exit(1)

    driver.find_element_by_id('fi_point_d').send_keys(d_number)
    # One of those forms with "re-enter" fields.
    driver.find_element_by_id('fi_point_d_r').send_keys(d_number)


def _FillNanacoNumber(driver, nanaco_number):
    driver.find_element_by_xpath(
        "//input[@id='r-point_n']/following-sibling::label").click()
    if len(nanaco_number) != 16:
        logging.error(
            f'{nanaco_number} is not a valid nanaco number must be 16 chars!!')
        sys.exit(1)

    driver.find_element_by_id('fi_point_n').send_keys(nanaco_number)


def _ChoosePointProgram(driver, t_number, d_number, nanaco_number):
    if t_number:
        return _FillTPointNumber(driver, t_number)
    if d_number:
        return _FillDPointNumber(driver, d_number)
    if nanaco_number:
        return _FillNanacoNumber(driver, nanaco_number)

    logging.error('No point number specified!')
    sys.exit(2)

def _FillForm(driver, account_num, dob_year, dob_month, dob_day,
              t_point_number, d_point_number, nanaco_number, email):
    print('driver currently at')
    print(driver.current_url)
    account_num_input = driver.find_element_by_id('fi_account_num')
    account_num_input.send_keys(account_num)

    driver.find_element_by_id('fi_birth_year').send_keys(dob_year)
    driver.find_element_by_id('fi_birth_month').send_keys(dob_month)
    driver.find_element_by_id('fi_birth_day').send_keys(dob_day)

    _ChoosePointProgram(driver, t_point_number, d_point_number, nanaco_number)

    driver.find_element_by_id('fi_mail').send_keys(email)

    # Press on "agree" radio button.
    driver.find_element_by_xpath(
        "//input[@id='fi_policy']/following-sibling::label").click()

    # Press submit button.
    submit_area = driver.find_element_by_class_name('submit_btn_area')
    submit_area.find_element_by_tag_name('input').click()

    # Let the next page load.
    time.sleep(10)

    button_area = driver.find_element_by_class_name('submit_btn_area')
    button_area.find_element_by_xpath("//input[@type='submit']").click()

    time.sleep(5)


def AutoSubmit(driver_path, account_num, dob_year, dob_month, dob_day,
               t_point_number, d_point_number, nanaco_number, email):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')

    logging.info('Launching chrome.')
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.get(_POINT_ENTRY_URL)

    banner_with_div = driver.find_element_by_class_name(
        'entry_button_yellowback')
    first_div = banner_with_div.find_element_by_tag_name('div')
    link_image = first_div.find_element_by_tag_name('img')
    link_image.click()

    # Wait till it opens to the form.
    time.sleep(10)

    # It should open a new tab. Switch to that page.
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])

    _FillForm(driver, account_num, dob_year, dob_month, dob_day,
              t_point_number, d_point_number, nanaco_number, email)
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Program to auto fill the Shinsei point entry program.',
        epilog=('If more than one point numbers are specified, then the '
                'program picks one to enter the form.'))
    parser.add_argument('--driver', required=True)
    parser.add_argument('--account_num', type=str, required=True)
    parser.add_argument('--date_of_birth', help='in YYYY-MM-DD', required=True)
    parser.add_argument('--tpoint_num', type=str, help='Use T-point number.')
    parser.add_argument('--dpoint_num', type=str, help='Use D point number.')
    parser.add_argument('--nanaco_num', type=str, help='Use nanaco number.')
    parser.add_argument('--email', required=True)

    parser.add_argument(
        '-d',
        '--debug',
        help="Print debugging logs.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help="Print verbose logs.",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    year, month, day = args.date_of_birth.split('-')

    AutoSubmit(args.driver, args.account_num, year, month, day,
               args.tpoint_num, args.dpoint_num, args.nanaco_num, args.email)
