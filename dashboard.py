"""Main module for the Streamlit app"""

import requests
import streamlit as st
import random
import socket
import struct

NAGER_API_BASE = 'https://date.nager.at/api/v2'
SALUT_API_BASE = 'https://fourtonfish.com/hellosalut'

def gen_random_ipv4():
    """
    Generates random IP

    Returns:
        A random generated IP
    """
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


@st.cache
def get_salutation(ip):
    """

    Retrieve a salution for a specific IP address from the given API

    Args:
        ip: Random generated IP address

    Returns:
        The specific salutation for the given IP

    """
    # Join the base upi with ip URL parameter
    url = '/'.join([SALUT_API_BASE, '?ip=' + ip])

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    salutation_response = response.json()
    salutation = salutation_response['hello']

    return salutation


@st.cache
def load_country_codes():
    """Loads country codes available from the Nager.Date API

    Returns:
        A list of country codes. Each country code is
        a two character string.

    Raises:
        requests.exceptions.RequestException: If the
            request to the Nager.Date API fails.
    """


    url = '/'.join([NAGER_API_BASE, 'AvailableCountries'])
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    country_codes = [country['key'] for country in response.json()]

    return country_codes


def main():

    st.markdown('This is my new salutation')
    ip = gen_random_ipv4()
    st.markdown(get_salutation(ip))

    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown('You selected country code -', country_code)


if __name__ == '__main__':
    main()
