"""Main module for the Streamlit app"""

import datetime
import requests
import streamlit as st
import random
import socket
import struct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NAGER_API_BASE = 'https://date.nager.at/api/v2'
NAGER_API_GET_HOLIDAYS = 'https://date.nager.at/Api/v1/Get'
SALUT_API_BASE = 'https://fourtonfish.com/hellosalut'
NUMBER_OF_PREVIOUS_YEARS = 10

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


@st.cache(show_spinner=False)
def get_numbers_of_holidays(country_code, year):
    """
    Get number of holidays based on year and country code
    Args:
        country_code: Country code of a given country
        year: Year for which we should calculate the number of holidays

    Returns:
        Number of holidays given for a specific country code and year, returned by Nager.Date API.
    """
    url = '/'.join([NAGER_API_GET_HOLIDAYS, str(country_code), str(year)])
    try:
        response = requests.get(url)
        response.raise_for_status()
        return len(response.json())
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


@st.cache(show_spinner=False)
def get_holidays(country_code):
    """
    Given a country code, get the number of holidays from Nager.Date API
    Args:
        country_code: Country code of a given country

    Returns:
        The diagram corresponding to number of holidays in the past 10 years.
    """

    current_year = datetime.datetime.now().year

    x_years = np.empty(shape=NUMBER_OF_PREVIOUS_YEARS + 1, dtype=int)
    y_holidays = np.empty(shape=NUMBER_OF_PREVIOUS_YEARS + 1, dtype=int)

    for [index, year] in enumerate(range(current_year - NUMBER_OF_PREVIOUS_YEARS, current_year + 1)):
        response = get_numbers_of_holidays(country_code, year)
        x_years[index] = year
        y_holidays[index] = response

    df = pd.DataFrame({'holidays': y_holidays}, index=x_years)
    return df



def main():

    st.markdown('This is my new salutation')
    ip = gen_random_ipv4()
    st.markdown(get_salutation(ip))

    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown('You selected country code - ' + country_code)

    st.line_chart(get_holidays(country_code))


if __name__ == '__main__':
    main()
