import pendulum

from calendar_service.calendar import Calendar
from currency_exchange_service.currencies import Currency, FiatValue
from currency_exchange_service.exchange_rates_provider import ExchangeRatesProvider


class Exchanger:
    BASE_CURRENCY = Currency.ZLOTY

    def __init__(self, exchange_rates_provider: ExchangeRatesProvider, calendar: Calendar):
        self.exchange_rates_provider = exchange_rates_provider
        self.calendar = calendar

    def exchange(self, date: pendulum.DateTime, fiat_value: FiatValue) -> FiatValue:
        if fiat_value.currency == self.BASE_CURRENCY:
            return fiat_value
        exchange_day = self.get_day_one(date)
        rate = self.exchange_rates_provider.get_rate(fiat_value.currency, exchange_day)

        amount_in_base_currency = round(fiat_value.amount * rate, 2)
        return FiatValue(amount_in_base_currency, self.BASE_CURRENCY)

    def get_day_one(self, day: pendulum.DateTime) -> pendulum.Date:
        day = day.subtract(days=1)

        while not self.calendar.is_workday(day):
            day = day.subtract(days=1)

        if self.calendar.is_out_of_range(day):
            raise ValueError("Date {} is out of range".format(day))

        return day
