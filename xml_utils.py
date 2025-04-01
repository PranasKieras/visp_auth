import xml.etree.ElementTree as ET


def extract_ticket(content):
    root = ET.fromstring(content)

    namespaces = {'authentication': 'http://www.epaslaugos.lt/services/authentication'}

    ticket_element = root.find('.//authentication:ticket', namespaces)

    ticket_value = ticket_element.text if ticket_element is not None else None
    return ticket_value

def extract_login_info(content):
    root = ET.fromstring(content)

    # Define namespaces
    namespaces = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'authentication': 'http://www.epaslaugos.lt/services/authentication'
    }

    # Find values using XPath
    vk_user_name = root.find('.//authentication:parameter[@name="VK_USER_NAME"]', namespaces).text
    vk_country = root.find('.//authentication:parameter[@name="VK_COUNTRY"]', namespaces).text
    vk_user_id = root.find('.//authentication:parameter[@name="VK_USER_ID"]', namespaces).text

    return vk_user_name, vk_user_id, vk_country

