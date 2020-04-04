# Automated FOREX trading with Python

You can watch how do I built this code on [Youtube](https://www.youtube.com/channel/UCnpiZEi_ZpjhF7g5KAdvUnw/)

## Youtube content

### How to gather the data from the broker

[How to gather the data from the broker](https://www.youtube.com/watch?v=6Ca4Gz1Upzo)

### Convert the JSON candle data to CSV

- Make a simple converter
- Enhance the converter and add calculated fields
- Analyse the CSV in Google Spreadsheet

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
