from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login_functionality(app):
    """
    Test performs login and verifies 'Signed in successfully' message is present
    """
    LoginPage(app.page) \
        .open_login_page(app.test_data.base_url + app.test_data.login_url) \
        .fill_email(app.test_data.user_credentials.username) \
        .fill_password(app.test_data.user_credentials.password) \
        .press_sign_in()
    HomePage(app.page).signed_in_alert_has_text('Signed in successfully')
