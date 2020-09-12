# Tablemap Builder

Used to build a tablemap to be used for [ajecc/poker-table-controller](https://github.com/ajecc/poker-table-controller). Provides a nice GUI to make the job easier. 

---

The tablemap is a json used to represent different areas of the poker table. These are will later be scraped and processed by [ajecc/poker-table-controller](https://github.com/ajecc/poker-table-controller) to take an action on the poker table.

The tablemap must be renamed to `tablemap.json` in order to be used by [ajecc/poker-table-controller](https://github.com/ajecc/poker-table-controller).

It must also have all the fields included in `template.json`. Notice the `is_bool_symbol` for each `label` and set it accordingly.

Also, notice that the hero is `p2`. Also, the players must be labeled in clockwise order.

After building the tablemap, the `tablemap.json` should look like a tablemap found in [examples](https://github.com/ajecc/tablemap-builder).

---

## Dependencies

Requieres x64 Python for Windows.

Install [Visual C++ Redistributable 2015-2019](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads).

Run `py -3 -m pip install -r requierments.txt` to install the dependencies.

---

## Runnig

Run with `py -3 main.py`.

---

![tablemap-builer example GUI](https://github.com/ajecc/tablemap-builder/tree/master/examples/example_image.png)
