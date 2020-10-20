
class Aggregate(Enum):
    """
    Enum to describe aggregation method to use.
    Note that this aggregation functions should
    be supported at the backend level.
    """
    COUNT
    COUNT_ERRORS
    COUNT_NAN
    MIN
    MAX
    AVG
    STD_DEV


class AbstractReader(object):
    """
    Subclass this class to create a PyTangoArchiving Reader for your specific DB

    e.g. TimeDBReader(AbstractReader)
    """

    def __init__(self, config='',...):
        '''
        Config can be an string like user:passwd@host
        or a json-like dictionary "{'user':'...','passwd':'...'}"
        '''
        self.db = YourDb(config)
        return

    def get_attributes(self, active=False, regexp=''):
        """
        Queries the database for the current list of archived attributes.
        arguments:
            active: True: only attributes currently archived
                    False: all attributes, even the one not archiving anymore
            regexp: '' :filter for attributes to retrieve
        """
        return list()

    def is_attribute_archived(self, attribute, active=False):
        """
        Returns if an attribute has values in DB.

        arguments:
            attribute: fqdn for the attribute.
            active: if true, only check for active attributes,
                    otherwise check all.
        """
        return True

    def get_last_attribute_value(self, attribute):
        """
        Returns last value inserted in DB for an attribute

        arguments:
            attribute: fqdn for the attribute.
        returns:
            (epoch, r_value, w_value, quality, error_desc)
        """

        return get_last_attributes_values((attribute))[attribute]

    def get_last_attributes_values(self, attributes):
        """
        Returns last values inserted in DB for a list of attributes

        arguments:
            attribute: fqdn for the attribute.
        returns:
            {'att1':(epoch, r_value, w_value, quality, error_desc),
             'att2':(epoch, r_value, w_value, quality, error_desc),
             ...
            }
        """

        return {attributes[0]: (time.time(), 0., 0., 0, "")}

    def get_attribute_values(self, attribute,
            start_date, stop_date=None,
            decimate=None):
        """
        Returns attribute values between start and stop dates.

        arguments:
            attribute: fqdn for the attribute.
            start_date: datetime, beginning of the period to query.
            stop_date: datetime, end of the period to query.
                       if None, now() is used.
            decimate: aggregation function to use in the form:
                      {'timedelta0':(MIN, MAX, …)
                      , 'timedelta1':(AVG, COUNT, …)
                      , …}
                      if None, returns raw data.
        returns:
            [(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ]
        """
        attributes[attribute] = {'start': start_date
                , 'stop': stop_date
                , 'decimation': decimate}
        return get_attributes_values(attributes)[attribute]

    def get_attributes_values(self, attributes):
        """
        Returns attributes values between start and stop dates
        , using decimation or not.

        arguments:
            attributes: a dict from the fqdn for the attributes
                        to the data to extract.
                        See get_attribute_values for the format to be used.

        returns:
            {'attr0':[(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ],
            'attr1':[(…),(…)]}
        """
        return {'attr0': [(time.time(), 0., 0., 0, '')]
                , 'attr1': [(time.time(), 0., 0., 0, '')]}
