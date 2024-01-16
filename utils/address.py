from dataclasses import dataclass

@dataclass
class Address:
  street: str = ""
  city: str = ""
  postal_code: str = ""
  district: str = ""
  addr_type: str = ""

  @classmethod
  def from_pararius_dict(cls, addr_dict: dict):
    instance = cls(
      addr_type=addr_dict["@type"],
      street=addr_dict['streetAddress'],
      city=addr_dict['addressLocality'],
      postal_code=addr_dict['postalCode'],
      district=addr_dict['addressRegion']
    )

    return instance

  def __repr__(self):
    return repr(f'''\
      Street: {self.street}
      District: {self.district}
      Postal Code: {self.postal_code}
      City: {self.city}
      Address Type: {self.addr_type}
      ''')

  def __str__(self):
    return f'''\
      Street: {self.street}
      District: {self.district}
      Postal Code: {self.postal_code}
      City: {self.city}
      Address Type: {self.addr_type}
      '''

  def to_string(addr_dict):
    return f'''\
      Street: {addr_dict['street']}
      District: {addr_dict['district']}
      Postal Code: {addr_dict['postal_code']}
      City: {addr_dict['city']}
      Address Type: {addr_dict['addr_type']}
      '''
