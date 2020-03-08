# Trading robot on FOREX

This code is designed for demo only.

## Development

Install python 3.7 and the requirements from `requirements.txt`

## How to use

You have to set the following environment variables:
- `API_URL` Base url for your broker
- `ACCESS_TOKEN` Access token for your broker

Positional Arguments:
- Instrument (e.g. EUR_USD)
- Granularity (e.g. M15)
- Data folder - collected data will be written there

```shell
python collect_candles.py 
```

This details are needed for my broker, but if you find
an other broker, with a slight change of code I'm sure you can make it as well.

If you need any help for a different broker setup, reach me out,
I'm happy to give some pointers.

## Tools that I've mentioned in my video

- [envchain](https://github.com/sorah/envchain)
- [anaconda](https://anaconda.org)
- [Visual Studio Code](https://code.visualstudio.com)
