# Internet login
USERNAME = ''
PASSWORD = ''

LOGIN_URL = 'http://10.10.0.1/24online/webpages/clientlogin.jsp'

USERNAME_XPATH = '//*[@id="jsena"]/table/tbody/tr/td/table/tbody/tr[3]\
    /td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/\
    table/tbody/tr[2]/td[2]/div/span/input'

PASSWORD_XPATH = '//*[@id="jsena"]/table/tbody/tr/td/table/tbody/\
    tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/table/tbody/\
    tr[1]/td/table/tbody/tr[4]/td[2]/div/span/input'

# Router Admin login
ROUTER_ADMIN_USERNAME = ''
ROUTER_ADMIN_PASSWORD = ''

CLIENT_LIST_XPATH = "//*[@id='dhcp_client_list']/table"
SESSION_XPATH = "//*[@id='generateHtml']/div[2]/table"

DHCP_CLIENT_LIST_URL = "http://192.168.0.1/Basic/Network.asp"
ACTIVE_SESSION_URL = "http://192.168.0.1/Status/Internet_Sessions.asp"
