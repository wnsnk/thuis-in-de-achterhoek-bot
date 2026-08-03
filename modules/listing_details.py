from bs4 import BeautifulSoup


class listingDetails():
    def __init__(self, listingHTML):
        self.soup = BeautifulSoup(listingHTML, 'html.parser')
        self.listing_info = self.soup.find_all(
            'span', class_='object-label-value')
        self.address_info = self.soup.find('div', class_='object-address')
        self.address = self.address_info.find_all('span')[0].text
        self.city = self.address_info.find_all('span')[2].text.strip()

        self.house_type = self.soup.find('span', class_='woningtype').text
        # if listing is not an appartment self.floor does not exist.
        try:
            self.floor = self.soup.find(
                'span', class_='verdieping').text.replace('•', '').strip()
        except AttributeError:
            self.floor = 'begane grond'
        self.listing_type = self.listing_info[0].text
        self.bedrooms = int(self.listing_info[1].text)
        self.m2 = int(self.listing_info[2].text.replace('m²', ''))
        self.price = float(self.soup.find('span', class_='prijs').text.replace(
            '€', '').replace(',', '.').strip())

    def print_info(self):
        print(self.address)
        print(self.city)
        print(self.house_type)
        print(self.floor)
        print(self.listing_type)
        print('bedrooms: ', self.bedrooms)
        print(self.m2)
        print(self.price)
