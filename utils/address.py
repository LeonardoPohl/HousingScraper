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
