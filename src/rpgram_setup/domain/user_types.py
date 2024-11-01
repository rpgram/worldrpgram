from rpgram_setup.domain.economics import Currency

Ledger = dict[type[Currency], Currency]

MinMax = tuple[int | None, int | None]
