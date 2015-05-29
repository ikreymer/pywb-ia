pywb IA Tools
=============

This project contains the setup for running pywb web archive replay system with the Internet Archive web archives.

It is still in experimental/alpha phase and should only be used for testing replay only.

## Installation

`pip install -r requirements.txt` which includes installing latest pywb and uwsgi.

Run with `uwsgi uwsgi.ini`

## Available Tools

## Alternate Wayback Machine Replay `/web/`

* `/web/` -> replays from `https://web.archive.org/web/`

For example, `http://localhost:8080/web/20111231161728//example.com/` will replay equivalent content from `http://web.archive.org/web/20111231161728/http://www.iana.org/domains/example/`
using pywb replay system.

## Archive-It Service Replay `/ait/` 

* `/ait/` -> replays from `http://wayback.archive-it.org/<COLLID>`
* `/ait/all/` -> replays from `http://wayback.archive-it.org/all/`

`<COLLID>` corresponds to a collection from the http://archive-it.org/ service.

## Single Item Replay `/item/`

* `/item/<ITEMNAME>` -> replays from WARC files stored under `http://archive.org/details/<ITEMNAME>`

For any public ITEMNAME that has a cdx files, replay content from that item only.
This will download the item `.idx` file locally on first use, and access the `.cdx.gz` and WARC remotely.
The item's `.idx`, `.cdx.gz` and WARC files must be accessible for this to work.





