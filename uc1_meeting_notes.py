"""
OrangeTree Global — AI Meeting Notes Tracker (UC1)
Powered by Claude API (Anthropic)
Run: streamlit run uc1_meeting_notes.py
"""

import streamlit as st
import anthropic
import json
from datetime import datetime

# -- Embedded logo (base64) so no separate SVG file needed on Streamlit Cloud --
LOGO_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjUgOSAxNTg2IDI2OCIgd2lkdGg9IjE1ODYiIGhlaWdodD0iMjY4Ij48dGl0bGU+T3JhbmdlVHJlZS57YWl9PC90aXRsZT48cGF0aCBmaWxsPSIjMUE3QTMwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xODIuNSAxM0wxODMuNSAxM0wxODMuNSAxOEwxODIuNSAxOUwxODIuNSAyMkwxODEuNSAyM0wxODAuNSAyOEwxNzguNSAzMUwxNzguNSAzM0wxNzMuNSA0M0wxNzEuNSA0NUwxNjcuNSA1MkwxNjMuNSA1NkwxNjMuNSA1N0wxNTMgNjcuNUwxNTIgNjcuNUwxNDUgNzMuNUwxNDIgNzQuNUwxNDAgNzYuNUwxMzYgNzguNUwxMzQgNzguNUwxMzAgODAuNUwxMjcgODAuNUwxMjYgODEuNUwxMTYgODEuNUwxMTUgODAuNUwxMTIgODAuNUwxMDUgNzYuNUwxMDAuNSA3MkwxMDAuNSA3MUwxMDYgNjguNUwxMDggNjYuNUwxMTUgNjIuNUwxMTggNTkuNUwxMTkgNTkuNUwxMjQgNTQuNUwxMjUgNTQuNUwxMzEuNSA0OEwxMzEuNSA0N0wxMzAgNDYuNUwxMTUgNTQuNUwxMTMgNTQuNUwxMDkgNTYuNUwxMDYgNTYuNUwxMDUgNTcuNUw5NiA1Ny41TDk1IDU2LjVMOTMgNTYuNUw4OC41IDUxTDg4LjUgNDRMOTIuNSAzNUw5NS41IDMyTDk1LjUgMzFMMTAzIDI0LjVMMTEyIDIwLjVMMTE5IDIwLjVMMTIwIDE5LjVMMTQ4IDE5LjVMMTQ5IDE4LjVMMTU5IDE4LjVMMTYwIDE3LjVMMTY2IDE3LjVMMTY3IDE2LjVMMTcxIDE2LjVMMTcyIDE1LjVMMTc1IDE1LjVMMTc2IDE0LjVMMTgyIDEzLjVaTTI5LjUgMTdMMzAgMTYuNUwzNCAyMC41TDM1IDIwLjVMNDAgMjQuNUw1MiAzMC41TDU0IDMwLjVMNjMgMzUuNUw2NSAzNS41TDY3IDM3LjVMNzIgMzkuNUw3NSA0Mi41TDc2IDQyLjVMODIuNSA1MEw4Mi41IDUyTDg0LjUgNTZMODQuNSA2MEw4MyA2MS41TDc3IDYyLjVMNzYgNjMuNUw2OCA2My41TDY3IDY0LjVMNjYgNjMuNUw1OSA2My41TDU4IDYyLjVMNTUgNjIuNUw0NiA1Ny41TDM4LjUgNDlMMzQuNSA0MUwzMy41IDM1TDMyLjUgMzRMMzIuNSAzMUwzMS41IDMwTDMxLjUgMjRMMzAuNSAyM0wzMCAxNy41Wk0xMzEuNSA0NkwxMzIgNDUuNUwxMzIgNDYuNVoiPjwvcGF0aD48cGF0aCBmaWxsPSIjRjM2NjIxIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik05My41IDg3TDExOSA4Ni41TDEyMCA4Ny41TDEyNCA4Ny41TDEyNSA4OC41TDEzMyA5MC41TDE0MyA5NS41TDE0NSA5Ny41TDE1MiAxMDEuNUwxNTYgMTA1LjVMMTU3IDEwNS41TDE2Ni41IDExNUwxNjYuNSAxMTZMMTcwLjUgMTIwTDE3MC41IDEyMUwxNzMuNSAxMjRMMTc0LjUgMTI3TDE3Ni41IDEyOUwxODEuNSAxMzlMMTgxLjUgMTQxTDE4Mi41IDE0MkwxODIuNSAxNDRMMTg1LjUgMTUxTDE4NS41IDE1NEwxODYuNSAxNTVMMTg2LjUgMTYwTDE4Ny41IDE2MUwxODcuNSAxODFMMTg2LjUgMTgyTDE4Ni41IDE4OEwxODUuNSAxODlMMTg1LjUgMTkzTDE4My41IDE5N0wxODIuNSAyMDNMMTc5LjUgMjA4TDE3OS41IDIxMEwxNzcuNSAyMTRMMTc1LjUgMjE2TDE3NC41IDIxOUwxNjcuNSAyMjhMMTY3LjUgMjI5TDE1NSAyNDEuNUwxNTQgMjQxLjVMMTUxIDI0NC41TDE1MCAyNDQuNUwxNDUgMjQ4LjVMMTQyIDI0OS41TDE0MCAyNTEuNUwxMzYgMjUzLjVMMTM0IDI1My41TDEyOSAyNTYuNUwxMjMgMjU3LjVMMTE5IDI1OS41TDExNSAyNTkuNUwxMTQgMjYwLjVMMTA4IDI2MC41TDEwNyAyNjEuNUw4OSAyNjEuNUw4OCAyNjAuNUw4MiAyNjAuNUw4MSAyNTkuNUw3MyAyNTguNUw3MiAyNTcuNUw2NyAyNTYuNUw2NCAyNTQuNUw2MiAyNTQuNUw1MiAyNDkuNUw0MyAyNDIuNUw0MiAyNDIuNUwyNi41IDIyN0wyNi41IDIyNkwyMC41IDIxOEwxMi41IDIwMUwxMS41IDE5NUwxMC41IDE5NEwxMC41IDE5MUw5LjUgMTkwTDkuNSAxODVMOC41IDE4NEw4LjUgMTYyTDkuNSAxNjFMMTAuNSAxNTNMMTEuNSAxNTJMMTMuNSAxNDRMMTYuNSAxMzhMMTguNSAxMzZMMjEuNSAxMzBMMzEgMTE5LjVMMzEuNSAxMjBMMjQuNSAxMzNMMjQuNSAxMzVMMjEuNSAxNDJMMjEuNSAxNTVMMjQuNSAxNjFMMzAgMTY1LjVMMzYgMTY4LjVMNDQgMTY5LjVMNDUgMTcwLjVMNzEgMTcwLjVMNzIgMTY5LjVMNzYgMTY5LjVMNzcgMTY4LjVMODAgMTY4LjVMODEgMTY3LjVMODkgMTY1LjVMMTA1IDE1Ny41TDEwNyAxNTUuNUwxMTQgMTUxLjVMMTMxLjUgMTM1TDEzMS41IDEzNEwxMzYuNSAxMjhMMTQwLjUgMTE5TDE0MC41IDEwOUwxMzguNSAxMDVMMTMyIDk4LjVMMTI0IDk0LjVMMTIwIDk0LjVMMTE5IDkzLjVMMTA0IDkzLjVMMTAzIDk0LjVMOTUgOTUuNUw5NCA5Ni41TDg5IDk3LjVMODQgMTAwLjVMODIgMTAwLjVMODAgMTAyLjVMNzcgMTAzLjVMNzEgMTA4LjVMNzAgMTA4LjVMNjAuNSAxMThMNjAuNSAxMTlMNTcuNSAxMjJMNTYuNSAxMjVMNTQuNSAxMjdMNTQuNSAxMjlMNTIuNSAxMzNMNTIuNSAxNDFMNTQuNSAxNDVMNTcgMTQ3LjVMNjMgMTUwLjVMNzQgMTUwLjVMNzUgMTQ5LjVMNzkgMTQ4LjVMODQuNSAxNDNMODUuNSAxNDFMODUuNSAxMzNMODQuNSAxMzJMODMuNSAxMjdMNzcuNSAxMTlMODUgMTE0LjVMODcgMTE0LjVMOTMgMTExLjVMOTYgMTExLjVMOTcgMTEwLjVMMTExIDExMC41TDExNy41IDExNkwxMTcuNSAxMThMMTE4LjUgMTE5TDExOC41IDEyNEwxMTcuNSAxMjVMMTE3LjUgMTI4TDExMi41IDEzN0wxMDMgMTQ2LjVMOTAgMTU0LjVMODggMTU0LjVMODUgMTU2LjVMODMgMTU2LjVMNzkgMTU4LjVMNzYgMTU4LjVMNzUgMTU5LjVMNzAgMTU5LjVMNjkgMTYwLjVMNTMgMTYwLjVMNTIgMTU5LjVMNDggMTU5LjVMNDcgMTU4LjVMNDIgMTU3LjVMMzUgMTUzLjVMMzAuNSAxNDhMMzAuNSAxNDZMMjguNSAxNDJMMjguNSAxMzZMMjkuNSAxMzVMMjkuNSAxMzFMMzQuNSAxMjFMMzcuNSAxMThMMzcuNSAxMTdMNDcgMTA3LjVMNDggMTA3LjVMNTIgMTAzLjVMNTMgMTAzLjVMNTggOTkuNUw3MiA5Mi41TDc0IDkyLjVMNzUgOTEuNUw3NyA5MS41TDg0IDg4LjVMODcgODguNUw4OCA4Ny41TDkzIDg3LjVaIj48L3BhdGg+PHBhdGggZmlsbD0iIzAwMDAwMCIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMjcwLjUgNzFMMjc3IDcwLjVMMjc4IDcxLjVMMjg3IDcxLjVMMjg4IDcyLjVMMjkyIDcyLjVMMjk2IDc0LjVMMjk5IDc0LjVMMzAyIDc2LjVMMzA0IDc2LjVMMzEwIDc5LjVMMzE5IDg2LjVMMzIwIDg2LjVMMzI4LjUgOTVMMzI4LjUgOTZMMzMzLjUgMTAyTDMzNC41IDEwNUwzMzYuNSAxMDdMMzM5LjUgMTEzTDMzOS41IDExNUwzNDEuNSAxMThMMzQyLjUgMTI0TDM0NC41IDEyOEwzNDUuNSAxMzhMMzQ2LjUgMTM5TDM0Ni41IDE2OEwzNDUuNSAxNjlMMzQ0LjUgMTc5TDM0My41IDE4MEwzNDMuNSAxODNMMzQyLjUgMTg0TDM0MC41IDE5MkwzMzguNSAxOTVMMzM4LjUgMTk3TDMzNi41IDIwMUwzMzQuNSAyMDNMMzMzLjUgMjA2TDMyOC41IDIxMkwzMjguNSAyMTNMMzE1IDIyNS41TDMxNCAyMjUuNUwzMDkgMjI5LjVMMzAzIDIzMi41TDMwMSAyMzIuNUwyOTggMjM0LjVMMjkyIDIzNS41TDI5MSAyMzYuNUwyODggMjM2LjVMMjg3IDIzNy41TDI4MSAyMzcuNUwyODAgMjM4LjVMMjYzIDIzOC41TDI2MiAyMzcuNUwyNTcgMjM3LjVMMjU2IDIzNi41TDI0OSAyMzUuNUwyNDEgMjMxLjVMMjM5IDIzMS41TDIzNyAyMjkuNUwyMzQgMjI4LjVMMjMyIDIyNi41TDIyOCAyMjQuNUwyMTMuNSAyMDlMMjEwLjUgMjAzTDIwOC41IDIwMUwyMDcuNSAxOTdMMjA0LjUgMTkyTDIwNC41IDE5MEwyMDIuNSAxODZMMjAyLjUgMTgzTDIwMS41IDE4MkwyMDEuNSAxNzlMMjAwLjUgMTc4TDIwMC41IDE3M0wxOTkuNSAxNzJMMTk4LjUgMTUwTDE5OS41IDE0OUwxOTkuNSAxNDBMMjAwLjUgMTM5TDIwMC41IDEzNEwyMDEuNSAxMzNMMjAyLjUgMTI2TDIwMy41IDEyNUwyMDQuNSAxMjBMMjA2LjUgMTE3TDIwNi41IDExNUwyMTAuNSAxMDdMMjEyLjUgMTA1TDIxNi41IDk4TDIyOSA4NS41TDIzMCA4NS41TDIzOCA3OS41TDI0MiA3Ny41TDI0NCA3Ny41TDI0NyA3NS41TDI1MiA3NC41TDI1MyA3My41TDI2MSA3Mi41TDI2MiA3MS41TDI3MCA3MS41Wk0xMjgyLjUgNzFMMTI5MC41IDcxTDEyOTAuNSA4NEwxMjgwIDg0LjVMMTI3OSA4NS41TDEyNzcgODUuNUwxMjcwLjUgOTFMMTI2OC41IDk1TDEyNjguNSA5N0wxMjY3LjUgOThMMTI2Ny41IDExNEwxMjY4LjUgMTE1TDEyNjguNSAxMjFMMTI2OS41IDEyMkwxMjY5LjUgMTI4TDEyNzAuNSAxMjlMMTI3MC41IDE0OUwxMjY5LjUgMTUwTDEyNjguNSAxNTVMMTI2Ni41IDE1N0wxMjY2LjUgMTU4TDEyNjEgMTYzLjVMMTI1NyAxNjUuNUwxMjU1IDE2NS41TDEyNTQuNSAxNjdMMTI2MSAxNjkuNUwxMjY2LjUgMTc1TDEyNjkuNSAxODFMMTI2OS41IDE4NEwxMjcwLjUgMTg1TDEyNzAuNSAyMDVMMTI2OS41IDIwNkwxMjY4LjUgMjE5TDEyNjcuNSAyMjBMMTI2Ny41IDIzNUwxMjY4LjUgMjM2TDEyNjguNSAyMzlMMTI3MC41IDI0M0wxMjc0IDI0Ni41TDEyODEgMjQ5LjVMMTI5MC41IDI1MEwxMjkwLjUgMjYyTDEyNzYgMjYyLjVMMTI3NSAyNjEuNUwxMjY5IDI2MC41TDEyNjMgMjU3LjVMMTI1NS41IDI1MEwxMjUyLjUgMjQ0TDEyNTIuNSAyNDJMMTI1MS41IDI0MUwxMjUxLjUgMjM2TDEyNTAuNSAyMzVMMTI1MS41IDIxNUwxMjUyLjUgMjE0TDEyNTIuNSAyMDhMMTI1My41IDIwN0wxMjUzLjUgMjAxTDEyNTQuNSAyMDBMMTI1NC41IDE4NUwxMjUzLjUgMTg0TDEyNTIuNSAxODBMMTI0OCAxNzUuNUwxMjQ0IDE3NC41TDEyNDMgMTczLjVMMTIzOSAxNzMuNUwxMjM1LjUgMTcyTDEyMzUuNSAxNjFMMTI0NCAxNTkuNUwxMjUwIDE1Ni41TDEyNTEuNSAxNTVMMTI1NC41IDE0OEwxMjU0LjUgMTMzTDEyNTMuNSAxMzJMMTI1My41IDEyNUwxMjUyLjUgMTI0TDEyNTEuNSAxMTBMMTI1MC41IDEwOUwxMjUwLjUgOThMMTI1MS41IDk3TDEyNTIuNSA4OUwxMjU2LjUgODJMMTI2NCA3NS41TDEyNzEgNzIuNUwxMjc0IDcyLjVMMTI3NSA3MS41TDEyODIgNzEuNVpNMTQyMC41IDcxTDE0MjggNzAuNUwxNDI5IDcxLjVMMTQzNiA3MS41TDE0MzcgNzIuNUwxNDQzIDczLjVMMTQ1MCA3Ny41TDE0NTUuNSA4M0wxNDU4LjUgODlMMTQ1OS41IDk1TDE0NjAuNSA5NkwxNDYwLjUgMTEyTDE0NTkuNSAxMTNMMTQ1OS41IDEyMEwxNDU4LjUgMTIxTDE0NTcuNSAxMzZMMTQ1Ni41IDEzN0wxNDU2LjUgMTQ2TDE0NTcuNSAxNDdMMTQ1Ny41IDE1MUwxNDYzIDE1Ny41TDE0NjcgMTU5LjVMMTQ3Ni41IDE2MUwxNDc2LjUgMTcyTDE0NzMgMTcyLjVMMTQ3MiAxNzMuNUwxNDY4IDE3My41TDE0NjIgMTc2LjVMMTQ1OC41IDE4MUwxNDU3LjUgMTgzTDE0NTcuNSAxODZMMTQ1Ni41IDE4N0wxNDU3LjUgMjA1TDE0NTguNSAyMDZMMTQ1OS41IDIyMEwxNDYwLjUgMjIxTDE0NjAuNSAyMzdMMTQ1OS41IDIzOEwxNDU5LjUgMjQyTDE0NTYuNSAyNDlMMTQ1MSAyNTUuNUwxNDUwIDI1NS41TDE0NDUgMjU5LjVMMTQ0MyAyNTkuNUwxNDM5IDI2MS41TDE0MzYgMjYxLjVMMTQzNSAyNjIuNUwxNDIwLjUgMjYyTDE0MjAuNSAyNTBMMTQzMCAyNDkuNUwxNDMxIDI0OC41TDE0MzMgMjQ4LjVMMTQzNyAyNDYuNUwxNDQwLjUgMjQzTDE0NDIuNSAyMzlMMTQ0Mi41IDIzN0wxNDQzLjUgMjM2TDE0NDMuNSAyMThMMTQ0Mi41IDIxN0wxNDQyLjUgMjEwTDE0NDEuNSAyMDlMMTQ0MS41IDIwNEwxNDQwLjUgMjAzTDE0NDAuNSAxODZMMTQ0MS41IDE4NUwxNDQyLjUgMTc5TDE0NDUuNSAxNzRMMTQ1MiAxNjguNUwxNDU2LjUgMTY3TDE0NTYgMTY1LjVMMTQ1MiAxNjQuNUwxNDQ1LjUgMTU5TDE0NDIuNSAxNTRMMTQ0Mi41IDE1MkwxNDQwLjUgMTQ4TDE0NDAuNSAxMzFMMTQ0MS41IDEzMEwxNDQxLjUgMTI0TDE0NDIuNSAxMjNMMTQ0Mi41IDExN0wxNDQzLjUgMTE2TDE0NDMuNSA5N0wxNDQyLjUgOTZMMTQ0Mi41IDk0TDE0NDEuNSA5MkwxNDM2IDg2LjVMMTQzNCA4NS41TDE0MzIgODUuNUwxNDMxIDg0LjVMMTQyMSA4NC41TDE0MjAuNSA3MlpNMTU4NC41IDczTDE1ODcuNSA3M0wxNTg3IDkxLjVMMTU4Ni41IDgzTDE1ODUuNSA4MkwxNTg1LjUgNzZMMTU4NC41IDc0Wk04MjkuNSA3NEw5NDkuNSA3NEw5NDkgOTEuNUw5MDAuNSA5Mkw5MDAgMjM1LjVMODc5LjUgMjM1TDg3OS41IDkyTDgzMCA5MS41TDgyOS41IDc1Wk0xNDAwLjUgNzRMMTQwOCA3My41TDE0MDkgNzQuNUwxNDExIDc0LjVMMTQxNi41IDgwTDE0MTYuNSA4MkwxNDE3LjUgODNMMTQxNy41IDkxTDE0MTYuNSA5M0wxNDExIDk4LjVMMTQwOSA5OC41TDE0MDggOTkuNUwxNDAxIDk5LjVMMTQwMCA5OC41TDEzOTggOTguNUwxMzkyLjUgOTNMMTM5Mi41IDkxTDEzOTEuNSA5MEwxMzkxLjUgODNMMTM5Mi41IDgyTDEzOTIuNSA4MEwxMzk4IDc0LjVMMTQwMCA3NC41Wk0yNjMuNSA4OUwyODIgODguNUwyODMgODkuNUwyODYgODkuNUwyODcgOTAuNUwyODkgOTAuNUwyOTYgOTMuNUwzMDIgOTguNUwzMDMgOTguNUwzMDguNSAxMDRMMzA4LjUgMTA1TDMxNS41IDExNEwzMTguNSAxMjBMMzE4LjUgMTIyTDMxOS41IDEyM0wzMTkuNSAxMjVMMzIyLjUgMTMyTDMyMy41IDE0MkwzMjQuNSAxNDNMMzI0LjUgMTY2TDMyMy41IDE2N0wzMjMuNSAxNzJMMzIyLjUgMTczTDMyMi41IDE3N0wzMjEuNSAxNzhMMzIwLjUgMTg0TDMxOC41IDE4N0wzMTguNSAxODlMMzE0LjUgMTk3TDMxMi41IDE5OUwzMTAuNSAyMDNMMzAxIDIxMi41TDI5MyAyMTcuNUwyOTEgMjE3LjVMMjg4IDIxOS41TDI4NSAyMTkuNUwyODQgMjIwLjVMMjgwIDIyMC41TDI3OSAyMjEuNUwyNjcgMjIxLjVMMjY2IDIyMC41TDI2MiAyMjAuNUwyNjEgMjE5LjVMMjU4IDIxOS41TDI1NSAyMTcuNUwyNTMgMjE3LjVMMjQ1IDIxMi41TDIzNS41IDIwM0wyMjYuNSAxODdMMjI2LjUgMTg1TDIyNC41IDE4MUwyMjQuNSAxNzhMMjIzLjUgMTc3TDIyMy41IDE3NEwyMjIuNSAxNzNMMjIyLjUgMTY4TDIyMS41IDE2N0wyMjEuNSAxNDRMMjIyLjUgMTQzTDIyMi41IDEzN0wyMjMuNSAxMzZMMjIzLjUgMTMzTDIyNC41IDEzMkwyMjQuNSAxMjlMMjI1LjUgMTI4TDIyNy41IDEyMEwyMzMuNSAxMDlMMjQ0IDk3LjVMMjU0IDkxLjVMMjU2IDkxLjVMMjYwIDg5LjVMMjYzIDg5LjVaTTQwMi41IDExN0w0MTAgMTE2LjVMNDEyLjUgMTE4TDQxMi41IDEzN0w0MTEgMTM3LjVMNDEwIDEzNi41TDQwMiAxMzYuNUw0MDEgMTM3LjVMMzk4IDEzNy41TDM5MSAxNDAuNUwzODEuNSAxNTFMMzc5LjUgMTU1TDM3OC41IDE2MEwzNzcuNSAxNjFMMzc3LjUgMTY0TDM3Ni41IDE2NUwzNzYuNSAyMzVMMzU1LjUgMjM1TDM1NS41IDEzNUwzNTQuNSAxMzRMMzU0LjUgMTIwTDM3Mi41IDEyMEwzNzIuNSAxMjVMMzczLjUgMTI2TDM3NCAxNDIuNUwzODAuNSAxMzBMMzg4IDEyMi41TDM5NSAxMTguNUwzOTcgMTE4LjVMMzk4IDExNy41TDQwMiAxMTcuNVpNNDQ2LjUgMTE3TDQ2MCAxMTYuNUw0NjEgMTE3LjVMNDY2IDExNy41TDQ2NyAxMTguNUw0NzMgMTE5LjVMNDc5IDEyMi41TDQ4OC41IDEzMUw0OTQuNSAxNDJMNDk1LjUgMTQ4TDQ5Ni41IDE0OUw0OTYuNSAxNTRMNDk3LjUgMTU1TDQ5Ny41IDIyM0w0OTguNSAyMjRMNDk4LjUgMjMzTDQ5OS41IDIzNUw0ODEgMjM1LjVMNDc5LjUgMjM0TDQ3OS41IDIyNkw0NzguNSAyMjVMNDc4IDIyMS41TDQ2OSAyMzAuNUw0NjAgMjM1LjVMNDU4IDIzNS41TDQ1NCAyMzcuNUw0NTAgMjM3LjVMNDQ5IDIzOC41TDQzNiAyMzguNUw0MzUgMjM3LjVMNDMxIDIzNy41TDQzMCAyMzYuNUw0MjggMjM2LjVMNDE5IDIzMS41TDQxMy41IDIyNkw0MDguNSAyMTdMNDA3LjUgMjExTDQwNi41IDIxMEw0MDYuNSAyMDBMNDA3LjUgMTk5TDQwNy41IDE5NUw0MDguNSAxOTRMNDEwLjUgMTg3TDQxMi41IDE4NUw0MTQuNSAxODFMNDE5IDE3Ni41TDQyMCAxNzYuNUw0MjYgMTcxLjVMNDMyIDE2OC41TDQzNCAxNjguNUw0MzcgMTY2LjVMNDQwIDE2Ni41TDQ0NCAxNjQuNUw0NTQgMTYzLjVMNDU1IDE2Mi41TDQ2NCAxNjIuNUw0NjUgMTYxLjVMNDc2LjUgMTYxTDQ3Ni41IDE1Mkw0NzUuNSAxNTFMNDc1LjUgMTQ4TDQ3Mi41IDE0Mkw0NjcgMTM2LjVMNDYxIDEzMy41TDQ1OCAxMzMuNUw0NTcgMTMyLjVMNDQyIDEzMi41TDQ0MSAxMzMuNUw0MzcgMTMzLjVMNDM2IDEzNC41TDQyOCAxMzYuNUw0MjEgMTQwLjVMNDE5LjUgMTQwTDQxNy41IDEzM0w0MTYuNSAxMzJMNDE2LjUgMTMwTDQxNS41IDEyOUw0MTUuNSAxMjdMNDE3IDEyNS41TDQzMSAxMTkuNUw0MzQgMTE5LjVMNDM1IDExOC41TDQzOCAxMTguNUw0MzkgMTE3LjVMNDQ2IDExNy41Wk01NjUuNSAxMTdMNTc2IDExNi41TDU3NyAxMTcuNUw1ODIgMTE3LjVMNTg4IDEyMC41TDU5MCAxMjAuNUw1OTIgMTIyLjVMNTk1IDEyMy41TDYwMy41IDEzMkw2MDkuNSAxNDNMNjA5LjUgMTQ2TDYxMS41IDE1MEw2MTEuNSAxNTVMNjEyLjUgMTU2TDYxMi41IDIzNUw1OTEuNSAyMzVMNTkxLjUgMTYyTDU5MC41IDE2MUw1OTAuNSAxNTZMNTg5LjUgMTU1TDU4OS41IDE1Mkw1ODUuNSAxNDRMNTc3IDEzNi41TDU3NSAxMzYuNUw1NzEgMTM0LjVMNTU5IDEzNC41TDU1OCAxMzUuNUw1NTUgMTM1LjVMNTQ5IDEzOC41TDUzOS41IDE0OEw1MzYuNSAxNTRMNTM2LjUgMTU2TDUzNS41IDE1N0w1MzUuNSAxNjJMNTM0LjUgMTYzTDUzNC41IDIzNUw1MTMuNSAyMzVMNTEzLjUgMTI1TDUxMi41IDEyNEw1MTIuNSAxMjBMNTMxIDExOS41TDUzMyAxMzguNUw1MzUuNSAxMzRMNTQ1IDEyNC41TDU0NiAxMjQuNUw1NDggMTIyLjVMNTU3IDExOC41TDU2NSAxMTcuNVpNNjY3LjUgMTE3TDY3OCAxMTYuNUw2NzkgMTE3LjVMNjg0IDExNy41TDY4NSAxMTguNUw2ODggMTE4LjVMNjk4IDEyMy41TDcwNi41IDEzMkw3MDkgMTM2LjVMNzA5LjUgMTMwTDcxMC41IDEyOUw3MTEgMTE5LjVMNzI5LjUgMTIwTDcyOS41IDEyM0w3MjguNSAxMjRMNzI4LjUgMjI4TDcyNy41IDIyOUw3MjcuNSAyMzlMNzI2LjUgMjQwTDcyNS41IDI0OUw3MjQuNSAyNTBMNzIzLjUgMjU1TDcxNy41IDI2Nkw3MDggMjc1LjVMNzA2IDI3Ni41TDYzMC41IDI3Nkw2MzEuNSAyNzVMNjMxLjUgMjczTDYzMi41IDI3Mkw2MzIuNSAyNzBMNjMzLjUgMjY5TDYzMy41IDI2N0w2MzQuNSAyNjZMNjM2IDI2MC41TDY0MyAyNjQuNUw2NDUgMjY0LjVMNjUyIDI2Ny41TDY1NSAyNjcuNUw2NTYgMjY4LjVMNjYxIDI2OC41TDY2MiAyNjkuNUw2NzcgMjY5LjVMNjc4IDI2OC41TDY4MiAyNjguNUw2ODMgMjY3LjVMNjg4IDI2Ni41TDY5OC41IDI1OUw3MDQuNSAyNDlMNzA1LjUgMjQzTDcwNi41IDI0Mkw3MDYuNSAyMzhMNzA3LjUgMjM3TDcwNyAyMTYuNUw3MDUuNSAyMTlMNjk3IDIyNy41TDY4OCAyMzIuNUw2ODIgMjMzLjVMNjgxIDIzNC41TDY3NyAyMzQuNUw2NzYgMjM1LjVMNjY1IDIzNS41TDY2NCAyMzQuNUw2NTkgMjM0LjVMNjQ1IDIyOC41TDY0MyAyMjYuNUw2NDIgMjI2LjVMNjMyLjUgMjE3TDYzMi41IDIxNkw2MjkuNSAyMTNMNjI0LjUgMjAzTDYyNC41IDIwMUw2MjIuNSAxOTdMNjIyLjUgMTk0TDYyMS41IDE5M0w2MjEuNSAxODhMNjIwLjUgMTg3TDYyMC41IDE2OUw2MjEuNSAxNjhMNjIxLjUgMTYzTDYyMi41IDE2Mkw2MjMuNSAxNTVMNjI5LjUgMTQyTDYzMS41IDE0MEw2MzMuNSAxMzZMNjQzIDEyNi41TDY0NCAxMjYuNUw2NDkgMTIyLjVMNjUzIDEyMC41TDY2MSAxMTguNUw2NjIgMTE3LjVMNjY3IDExNy41Wk03ODUuNSAxMTdMNzk3IDExNi41TDc5OCAxMTcuNUw4MDMgMTE3LjVMODA0IDExOC41TDgxMCAxMTkuNUw4MTkgMTI0LjVMODI4LjUgMTM0TDgzMy41IDE0Mkw4MzMuNSAxNDRMODM1LjUgMTQ3TDgzNS41IDE0OUw4MzcuNSAxNTNMODM4LjUgMTYzTDgzOS41IDE2NEw4MzkuNSAxNzhMODM4IDE4MS41TDc1OCAxODEuNUw3NTcuNSAxOTBMNzU4LjUgMTkxTDc1OC41IDE5NUw3NTkuNSAxOTZMNzU5LjUgMTk4TDc2NS41IDIwOUw3NzAgMjEzLjVMNzcxIDIxMy41TDc3NiAyMTcuNUw3ODMgMjE5LjVMNzg0IDIyMC41TDc4NyAyMjAuNUw3ODggMjIxLjVMODEwIDIyMS41TDgxMSAyMjAuNUw4MTYgMjIwLjVMODE3IDIxOS41TDgyMCAyMTkuNUw4MjEgMjE4LjVMODI2IDIxNy41TDgyOSAyMTUuNUw4MjkuNSAyMTlMODMwLjUgMjIwTDgzMC41IDIyM0w4MzEuNSAyMjRMODMxLjUgMjI3TDgzMi41IDIyOEw4MzIuNSAyMzFMODMwIDIzMi41TDgyMiAyMzQuNUw4MjEgMjM1LjVMODE3IDIzNS41TDgxNiAyMzYuNUw4MTIgMjM2LjVMODExIDIzNy41TDgwMiAyMzcuNUw4MDEgMjM4LjVMNzg4IDIzOC41TDc4NyAyMzcuNUw3ODEgMjM3LjVMNzgwIDIzNi41TDc3NyAyMzYuNUw3NzYgMjM1LjVMNzcwIDIzNC41TDc1OSAyMjguNUw3NTAuNSAyMjFMNzUwLjUgMjIwTDc0Ni41IDIxNkw3NDUuNSAyMTNMNzQyLjUgMjA5TDc0Mi41IDIwN0w3NDAuNSAyMDRMNzQwLjUgMjAyTDczOC41IDE5OEw3MzguNSAxOTRMNzM3LjUgMTkzTDczNy41IDE4Nkw3MzYuNSAxODVMNzM2LjUgMTc0TDczNy41IDE3M0w3MzcuNSAxNjZMNzM4LjUgMTY1TDczOC41IDE2MUw3MzkuNSAxNjBMNzM5LjUgMTU3TDc0MC41IDE1Nkw3NDEuNSAxNTFMNzQ4LjUgMTM4TDc1My41IDEzM0w3NTMuNSAxMzJMNzYxIDEyNS41TDc3MCAxMjAuNUw3NzIgMTIwLjVMNzc5IDExNy41TDc4NSAxMTcuNVpNOTk1LjUgMTE3TDEwMDQgMTE2LjVMMTAwNi41IDExOEwxMDA2LjUgMTM3TDEwMDUgMTM3LjVMMTAwNCAxMzYuNUw5OTYgMTM2LjVMOTk1IDEzNy41TDk5MSAxMzcuNUw5ODUgMTQwLjVMOTc5LjUgMTQ1TDk3OS41IDE0Nkw5NzYuNSAxNDlMOTczLjUgMTU0TDk3My41IDE1Nkw5NzEuNSAxNjBMOTcxLjUgMTYzTDk3MC41IDE2NEw5NzAuNSAxNzBMOTY5LjUgMTcxTDk2OS41IDIzNUw5NDguNSAyMzVMOTQ4LjUgMTIwTDk2Ni41IDEyMEw5NjYuNSAxMzNMOTY3LjUgMTM0TDk2OCAxNDIuNUw5NjguNSAxNDBMOTczLjUgMTMxTDk4MiAxMjIuNUw5ODkgMTE4LjVMOTk1IDExNy41Wk0xMDQ5LjUgMTE3TDEwNjIgMTE2LjVMMTA2MyAxMTcuNUwxMDY4IDExNy41TDEwNjkgMTE4LjVMMTA3NCAxMTkuNUwxMDgyIDEyMy41TDEwODUgMTI2LjVMMTA4NiAxMjYuNUwxMDkzLjUgMTM1TDEwOTkuNSAxNDZMMTA5OS41IDE0OEwxMTAxLjUgMTUyTDExMDEuNSAxNTVMMTEwMi41IDE1NkwxMTAyLjUgMTYwTDExMDMuNSAxNjFMMTEwNCAxNjkuNUwxMTA2LjUgMTU2TDExMTEuNSAxNDRMMTExMy41IDE0MkwxMTE0LjUgMTM5TDExMTcuNSAxMzZMMTExNy41IDEzNUwxMTI5IDEyNC41TDExMzkgMTE5LjVMMTE0NSAxMTguNUwxMTQ2IDExNy41TDExNTEgMTE3LjVMMTE1MiAxMTYuNUwxMTY0IDExNi41TDExNjUgMTE3LjVMMTE3MCAxMTcuNUwxMTcxIDExOC41TDExNzQgMTE4LjVMMTE3NyAxMjAuNUwxMTgxIDEyMS41TDExODMgMTIzLjVMMTE4NyAxMjUuNUwxMTk0LjUgMTMzTDExOTQuNSAxMzRMMTE5OC41IDEzOUwxMjAxLjUgMTQ1TDEyMDEuNSAxNDdMMTIwNC41IDE1NEwxMjA0LjUgMTU4TDEyMDUuNSAxNTlMMTIwNS41IDE2N0wxMjA2LjUgMTY4TDEyMDYuNSAxNzVMMTIwNS41IDE3NkwxMjA1IDE4MS41TDExMjQgMTgxLjVMMTEyMy41IDE4NkwxMTI0LjUgMTg3TDExMjQuNSAxOTJMMTEyNS41IDE5M0wxMTI1LjUgMTk2TDExMjkuNSAyMDVMMTEzMS41IDIwN0wxMTMxLjUgMjA4TDExNDEgMjE2LjVMMTE0NyAyMTkuNUwxMTQ5IDIxOS41TDExNTAgMjIwLjVMMTE1NCAyMjAuNUwxMTU1IDIyMS41TDExNzcgMjIxLjVMMTE3OCAyMjAuNUwxMTgyIDIyMC41TDExODMgMjE5LjVMMTE5MCAyMTguNUwxMTkzIDIxNi41TDExOTYgMjE2LjVMMTE5OS41IDIzMUwxMTkxIDIzNC41TDExODggMjM0LjVMMTE4NyAyMzUuNUwxMTg0IDIzNS41TDExODMgMjM2LjVMMTE3OSAyMzYuNUwxMTc4IDIzNy41TDExNjkgMjM3LjVMMTE2OCAyMzguNUwxMTU1IDIzOC41TDExNTQgMjM3LjVMMTE0MyAyMzYuNUwxMTQyIDIzNS41TDExMzcgMjM0LjVMMTEyNyAyMjkuNUwxMTE1LjUgMjE5TDExMTUuNSAyMThMMTExMS41IDIxM0wxMTA1LjUgMTk5TDExMDUuNSAxOTVMMTEwNC41IDE5NEwxMTA0LjUgMTg5TDExMDMuNSAxODhMMTEwMyAxODEuNUwxMDIxLjUgMTgyTDEwMjEuNSAxODlMMTAyMi41IDE5MEwxMDIyLjUgMTk0TDEwMjMuNSAxOTVMMTAyNC41IDIwMEwxMDI4LjUgMjA3TDEwMzcgMjE1LjVMMTA0NSAyMTkuNUwxMDUxIDIyMC41TDEwNTIgMjIxLjVMMTA3NCAyMjEuNUwxMDc1IDIyMC41TDEwODAgMjIwLjVMMTA4MSAyMTkuNUwxMDg0IDIxOS41TDEwODUgMjE4LjVMMTA5MyAyMTYuNUwxMDk0LjUgMjE5TDEwOTQuNSAyMjJMMTA5NS41IDIyM0wxMDk1LjUgMjI2TDEwOTYuNSAyMjdMMTA5NiAyMzEuNUwxMDg5IDIzNC41TDEwODYgMjM0LjVMMTA4NSAyMzUuNUwxMDgyIDIzNS41TDEwODEgMjM2LjVMMTA3NiAyMzYuNUwxMDc1IDIzNy41TDEwNjcgMjM3LjVMMTA2NiAyMzguNUwxMDUzIDIzOC41TDEwNTIgMjM3LjVMMTA0NSAyMzcuNUwxMDQ0IDIzNi41TDEwNDEgMjM2LjVMMTA0MCAyMzUuNUwxMDMyIDIzMy41TDEwMjIgMjI3LjVMMTAxMi41IDIxOEwxMDEyLjUgMjE3TDEwMDguNSAyMTJMMTAwMy41IDIwMEwxMDAyLjUgMTkyTDEwMDEuNSAxOTFMMTAwMS41IDE2N0wxMDAyLjUgMTY2TDEwMDIuNSAxNjJMMTAwMy41IDE2MUwxMDAzLjUgMTU4TDEwMDQuNSAxNTdMMTAwNS41IDE1MkwxMDExLjUgMTQwTDEwMjQgMTI2LjVMMTAzNCAxMjAuNUwxMDM2IDEyMC41TDEwNDAgMTE4LjVMMTA0MyAxMTguNUwxMDQ0IDExNy41TDEwNDkgMTE3LjVaTTEzMjYuNSAxMTdMMTM0MCAxMTYuNUwxMzQxIDExNy41TDEzNDYgMTE3LjVMMTM0NyAxMTguNUwxMzUwIDExOC41TDEzNTEgMTE5LjVMMTM1NiAxMjAuNUwxMzY2LjUgMTI4TDEzNjYuNSAxMjlMMTM3MC41IDEzM0wxMzc0LjUgMTQxTDEzNzUuNSAxNDdMMTM3Ni41IDE0OEwxMzc2LjUgMTUyTDEzNzcuNSAxNTNMMTM3Ny41IDIxNEwxMzc4LjUgMjE1TDEzNzguNSAyMzBMMTM3OS41IDIzMUwxMzc5LjUgMjM1TDEzNjEgMjM1LjVMMTM2MC41IDIzMUwxMzU5LjUgMjMwTDEzNTkuNSAyMjJMMTM1OCAyMjEuNUwxMzU2LjUgMjI0TDEzNDggMjMxLjVMMTM0MCAyMzUuNUwxMzM4IDIzNS41TDEzMzQgMjM3LjVMMTMzMCAyMzcuNUwxMzI5IDIzOC41TDEzMTYgMjM4LjVMMTMxNSAyMzcuNUwxMzEyIDIzNy41TDEzMTEgMjM2LjVMMTMwNiAyMzUuNUwxMzAxIDIzMi41TDEyOTUuNSAyMjhMMTI5NS41IDIyN0wxMjkyLjUgMjI0TDEyODkuNSAyMTlMMTI4OS41IDIxN0wxMjg3LjUgMjEzTDEyODcuNSAxOTdMMTI4OC41IDE5NkwxMjg4LjUgMTkzTDEyOTMuNSAxODNMMTMwMiAxNzQuNUwxMzE1IDE2Ny41TDEzMTcgMTY3LjVMMTMyMSAxNjUuNUwxMzI0IDE2NS41TDEzMjUgMTY0LjVMMTMyOCAxNjQuNUwxMzI5IDE2My41TDEzNTYuNSAxNjFMMTM1Ni41IDE1MUwxMzU1LjUgMTUwTDEzNTUuNSAxNDdMMTM1MC41IDEzOUwxMzQ0IDEzNC41TDEzNDIgMTM0LjVMMTMzOCAxMzIuNUwxMzIyIDEzMi41TDEzMjEgMTMzLjVMMTMxNyAxMzMuNUwxMzE2IDEzNC41TDEzMDggMTM2LjVMMTMwNCAxMzguNUwxMzAyIDE0MC41TDEyOTkuNSAxNDBMMTI5OS41IDEzOEwxMjk4LjUgMTM3TDEyOTguNSAxMzVMMTI5NS41IDEyOEwxMjk2IDEyNi41TDEzMDMgMTIyLjVMMTMwNSAxMjIuNUwxMzExIDExOS41TDEzMTkgMTE4LjVMMTMyMCAxMTcuNUwxMzI2IDExNy41Wk0xMzkzLjUgMTIwTDE0MTUuNSAxMjBMMTQxNSAyMzUuNUwxMzkzLjUgMjM1TDEzOTMuNSAxMjFaTTc4Ni41IDEzMkw3OTMgMTMxLjVMNzk0IDEzMi41TDc5OCAxMzIuNUw4MDggMTM3LjVMODExLjUgMTQxTDgxNi41IDE1MEw4MTYuNSAxNTJMODE4LjUgMTU2TDgxOC41IDE2NEw4MTkuNSAxNjVMODE4IDE2Ni41TDc1OCAxNjYuNUw3NTcuNSAxNjNMNzU4LjUgMTYyTDc1OC41IDE1OUw3NTkuNSAxNThMNzYwLjUgMTUzTDc2NS41IDE0NEw3NzMgMTM2LjVMNzgyIDEzMi41TDc4NiAxMzIuNVpNMTA1MC41IDEzMkwxMDU3IDEzMS41TDEwNTggMTMyLjVMMTA2MiAxMzIuNUwxMDYzIDEzMy41TDEwNjUgMTMzLjVMMTA3MSAxMzYuNUwxMDc2LjUgMTQyTDEwODAuNSAxNDlMMTA4MC41IDE1MUwxMDgyLjUgMTU1TDEwODMuNSAxNjZMMTAyMiAxNjYuNUwxMDIxLjUgMTY0TDEwMjIuNSAxNjNMMTAyMi41IDE1OUwxMDIzLjUgMTU4TDEwMjMuNSAxNTZMMTAyNS41IDE1M0wxMDI2LjUgMTQ5TDEwMjguNSAxNDdMMTAzMC41IDE0M0wxMDM5IDEzNS41TDEwNDYgMTMyLjVMMTA1MCAxMzIuNVpNMTE1My41IDEzMkwxMTU5IDEzMS41TDExNjAgMTMyLjVMMTE2NSAxMzIuNUwxMTY2IDEzMy41TDExNjggMTMzLjVMMTE3MiAxMzUuNUwxMTc5LjUgMTQzTDExODIuNSAxNDhMMTE4Mi41IDE1MEwxMTg0LjUgMTU0TDExODQuNSAxNTdMMTE4NS41IDE1OEwxMTg1LjUgMTY2TDExMjQuNSAxNjZMMTEyNC41IDE2MUwxMTI1LjUgMTYwTDExMjYuNSAxNTRMMTEyOS41IDE0OEwxMTM1LjUgMTQxTDExMzUuNSAxNDBMMTE0NSAxMzMuNUwxMTQ3IDEzMy41TDExNDggMTMyLjVMMTE1MyAxMzIuNVpNNjY5LjUgMTM0TDY4MyAxMzMuNUw2ODQgMTM0LjVMNjkxIDEzNi41TDcwMS41IDE0Nkw3MDUuNSAxNTNMNzA1LjUgMTU1TDcwNi41IDE1Nkw3MDYuNSAxNjBMNzA3LjUgMTYxTDcwNy41IDE5MEw3MDYuNSAxOTFMNzA2LjUgMTk2TDcwNS41IDE5N0w3MDUuNSAxOTlMNjk4LjUgMjEwTDY5MyAyMTQuNUw2ODQgMjE4LjVMNjgwIDIxOC41TDY3OSAyMTkuNUw2NjcgMjE4LjVMNjU3IDIxMy41TDY0OS41IDIwNkw2NDQuNSAxOTZMNjQ0LjUgMTk0TDY0My41IDE5M0w2NDMuNSAxODlMNjQyLjUgMTg4TDY0Mi41IDE4MEw2NDEuNSAxNzlMNjQxLjUgMTc1TDY0Mi41IDE3NEw2NDIuNSAxNjZMNjQzLjUgMTY1TDY0My41IDE2MUw2NDQuNSAxNjBMNjQ1LjUgMTU1TDY1MS41IDE0NUw2NTcgMTM5LjVMNjY0IDEzNS41TDY2OSAxMzQuNVpNNDYxLjUgMTc3TDQ3Ny41IDE3N0w0NzcuNSAxOThMNDc2LjUgMTk5TDQ3NS41IDIwNUw0NzEuNSAyMTJMNDY3IDIxNi41TDQ1OCAyMjEuNUw0NTYgMjIxLjVMNDU1IDIyMi41TDQ0MiAyMjIuNUw0MzQgMjE4LjVMNDI4LjUgMjEwTDQyNy41IDIwMEw0MjguNSAxOTlMNDI4LjUgMTk1TDQzMC41IDE5MUw0MzggMTgzLjVMNDQ0IDE4MC41TDQ0NiAxODAuNUw0NTAgMTc4LjVMNDU0IDE3OC41TDQ1NSAxNzcuNUw0NjEgMTc3LjVaTTEzNDEuNSAxNzdMMTM1Ny41IDE3N0wxMzU3LjUgMjAwTDEzNTYuNSAyMDFMMTM1Ni41IDIwNEwxMzUyLjUgMjExTDEzNDMgMjE5LjVMMTMzNiAyMjEuNUwxMzM1IDIyMi41TDEzMjIgMjIyLjVMMTMyMSAyMjEuNUwxMzE5IDIyMS41TDEzMTcgMjE5LjVMMTMxNiAyMTkuNUwxMzA5LjUgMjEyTDEzMDkuNSAyMTBMMTMwOC41IDIwOUwxMzA4LjUgMTk3TDEzMTEuNSAxOTBMMTMxNyAxODQuNUwxMzIyIDE4MS41TDEzMjQgMTgxLjVMMTMyNyAxNzkuNUwxMzM0IDE3OC41TDEzMzUgMTc3LjVMMTM0MSAxNzcuNVpNMTIxOC41IDIwOUwxMjI4IDIwOC41TDEyMzIgMjEwLjVMMTIzNS41IDIxNEwxMjM3LjUgMjE4TDEyMzcuNSAyMjhMMTIzNC41IDIzNEwxMjMwIDIzNy41TDEyMjggMjM3LjVMMTIyNyAyMzguNUwxMjIwIDIzOC41TDEyMTkgMjM3LjVMMTIxNyAyMzcuNUwxMjEyLjUgMjM0TDEyMDkuNSAyMjhMMTIwOS41IDIxOEwxMjExLjUgMjE0TDEyMTUgMjEwLjVMMTIxOCAyMDkuNVpNMTU4Ni41IDIxNkwxNTg3LjUgMjE2TDE1ODcuNSAyMjJMMTU4Ni41IDIyMkwxNTg2LjUgMjE3WiI+PC9wYXRoPjwvc3ZnPg=="
LOGO_HTML = '<img src="data:image/svg+xml;base64,' + LOGO_B64 + '" style="width:100%;max-width:220px;display:block;margin-bottom:4px;">'

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Meeting Notes Tracker | OrangeTree Global",
    page_icon="🌳",
    layout="wide",
)

# ── Branding ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .action-card {
        background: #f8f9fa;
        border-left: 4px solid #F36621;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        margin: 0.4rem 0;
    }
    .metric-box {
        background: #fff3ee;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .tag {
        display: inline-block;
        background: #F36621;
        color: white;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin-right: 4px;
    }
    .tag-low { background: #28a745; }
    .tag-med { background: #ffc107; color: #333; }
    .tag-high { background: #dc3545; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    f'<img src="data:image/svg+xml;base64,{LOGO_B64}" style="width:280px;max-width:100%;display:block;margin-bottom:12px;">',
    unsafe_allow_html=True
)
st.markdown("## AI Meeting Notes Tracker")
st.markdown("Paste your meeting transcript → get structured notes, decisions & action items instantly")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO_HTML, unsafe_allow_html=True)
    st.markdown("---")
    api_key = st.text_input("Anthropic API Key", type="password", help="Get from console.anthropic.com")
    model = st.selectbox("Model", ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"], index=1)
    st.markdown("---")
    st.markdown("**Meeting context (optional)**")
    meeting_type = st.selectbox("Meeting type", ["Client call", "Internal team", "Sales demo", "Strategy session", "Project review", "Other"])
    language = st.selectbox("Language", ["English", "Hindi", "Bengali", "Mixed (Hinglish)"])
    st.markdown("---")
    st.markdown("**About this tool**")
    st.info("UC1 of OrangeTree's AI SME Suite. Powered by Claude API.", icon="ℹ️")

# ── Main content ──────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📋 Paste Transcript", "📁 Upload File"])

with tab1:
    transcript_text = st.text_area(
        "Paste your meeting transcript here",
        height=250,
        placeholder="Paste raw transcript, meeting notes, or even rough bullet points...\n\nExample:\nSubhra: We need to close the QSR pilot by end of month.\nRahul: I'll set up the demo environment by Wednesday.\nClient: Can you share a proposal with pricing?\n..."
    )

with tab2:
    uploaded_file = st.file_uploader("Upload transcript (.txt or .md)", type=["txt", "md"])
    if uploaded_file:
        transcript_text = uploaded_file.read().decode("utf-8")
        st.success(f"Loaded: {uploaded_file.name} ({len(transcript_text)} characters)")
        st.text_area("Preview", transcript_text[:500] + "...", height=150, disabled=True)

# ── Process button ────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    process_btn = st.button("⚡ Analyse Meeting", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    st.rerun()

if process_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
        st.stop()
    if not transcript_text or len(transcript_text.strip()) < 20:
        st.warning("Please paste or upload a transcript first.")
        st.stop()

    with st.spinner("Claude is reading your meeting..."):
        try:
            client = anthropic.Anthropic(api_key=api_key)

            SYSTEM_PROMPT = """You are an expert meeting analyst for OrangeTree Global, a Data Science and AI consulting company.
Analyse the meeting transcript and return a JSON object with this exact structure:
{
  "meeting_title": "Inferred title (max 8 words)",
  "meeting_date": "Inferred or 'Unknown'",
  "duration_estimate": "Estimated duration",
  "participants": ["name1", "name2"],
  "executive_summary": "3-4 sentence summary of what was discussed and decided",
  "key_decisions": [
    {"decision": "What was decided", "owner": "Who decided/responsible", "impact": "Why it matters"}
  ],
  "action_items": [
    {"task": "Clear action description", "owner": "Person responsible", "deadline": "By when or 'Not specified'", "priority": "High/Medium/Low", "notes": "Any extra context"}
  ],
  "open_questions": ["Unresolved question 1", "Unresolved question 2"],
  "risks_flags": ["Any risk or concern raised"],
  "next_meeting": "Mentioned or 'Not scheduled'"
}
Return ONLY valid JSON. No markdown, no explanation."""

            USER_PROMPT = f"""Meeting type: {meeting_type}
Language context: {language}

TRANSCRIPT:
{transcript_text}"""

            response = client.messages.create(
                model=model,
                max_tokens=2000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": USER_PROMPT}]
            )

            raw = response.content[0].text.strip()
            # Strip markdown code blocks if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw)
            st.session_state["meeting_data"] = data

        except json.JSONDecodeError as e:
            st.error(f"Could not parse Claude's response. Try a longer transcript. Error: {e}")
            st.code(raw, language="text")
        except Exception as e:
            st.error(f"API error: {e}")

# ── Display results ───────────────────────────────────────────────────────────
if "meeting_data" in st.session_state:
    d = st.session_state["meeting_data"]

    st.markdown("---")
    st.markdown(f"## 📝 {d.get('meeting_title', 'Meeting Notes')}")

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Participants", len(d.get("participants", [])))
    with c2:
        st.metric("Action Items", len(d.get("action_items", [])))
    with c3:
        st.metric("Decisions", len(d.get("key_decisions", [])))
    with c4:
        st.metric("Open Questions", len(d.get("open_questions", [])))

    # Executive Summary
    st.markdown("### 📋 Executive Summary")
    st.info(d.get("executive_summary", ""))

    # Two columns: decisions + action items
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### ✅ Key Decisions")
        decisions = d.get("key_decisions", [])
        if decisions:
            for dec in decisions:
                st.markdown(f"""
<div class="action-card">
<b>{dec.get('decision', '')}</b><br>
👤 <i>{dec.get('owner', 'TBD')}</i> &nbsp;|&nbsp; 💡 {dec.get('impact', '')}
</div>
""", unsafe_allow_html=True)
        else:
            st.write("No explicit decisions recorded.")

    with col_right:
        st.markdown("### 🎯 Action Items")
        actions = d.get("action_items", [])
        if actions:
            # Sort by priority
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            actions_sorted = sorted(actions, key=lambda x: priority_order.get(x.get("priority", "Low"), 2))
            for item in actions_sorted:
                priority = item.get("priority", "Medium")
                tag_class = {"High": "tag-high", "Medium": "tag-med", "Low": "tag-low"}.get(priority, "tag-med")
                st.markdown(f"""
<div class="action-card">
<span class="tag {tag_class}">{priority}</span>
<b>{item.get('task', '')}</b><br>
👤 {item.get('owner', 'TBD')} &nbsp;|&nbsp; 📅 {item.get('deadline', 'TBD')}<br>
<small>{item.get('notes', '')}</small>
</div>
""", unsafe_allow_html=True)
        else:
            st.write("No action items extracted.")

    # Open questions & risks
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### ❓ Open Questions")
        for q in d.get("open_questions", []):
            st.markdown(f"- {q}")

    with col4:
        st.markdown("### ⚠️ Risks & Flags")
        risks = d.get("risks_flags", [])
        if risks:
            for r in risks:
                st.warning(r, icon="⚠️")
        else:
            st.success("No risks flagged.", icon="✅")

    # Participants & next meeting
    st.markdown("### 👥 Participants")
    participants = d.get("participants", [])
    if participants:
        st.write(", ".join(participants))

    next_mtg = d.get("next_meeting", "Not scheduled")
    if next_mtg and next_mtg != "Not scheduled":
        st.info(f"**Next meeting:** {next_mtg}", icon="📅")

    # Export section
    st.markdown("---")
    st.markdown("### 📤 Export")

    # Generate plain text export
    def generate_text_export(d):
        lines = []
        lines.append(f"MEETING NOTES — {d.get('meeting_title', '')}")
        lines.append(f"Date: {d.get('meeting_date', 'Unknown')} | Duration: {d.get('duration_estimate', 'Unknown')}")
        lines.append(f"Participants: {', '.join(d.get('participants', []))}")
        lines.append("\n─── EXECUTIVE SUMMARY ───")
        lines.append(d.get("executive_summary", ""))
        lines.append("\n─── KEY DECISIONS ───")
        for i, dec in enumerate(d.get("key_decisions", []), 1):
            lines.append(f"{i}. {dec.get('decision', '')} (Owner: {dec.get('owner', 'TBD')})")
        lines.append("\n─── ACTION ITEMS ───")
        for i, item in enumerate(d.get("action_items", []), 1):
            lines.append(f"{i}. [{item.get('priority', 'Medium')}] {item.get('task', '')} — {item.get('owner', 'TBD')} by {item.get('deadline', 'TBD')}")
        lines.append("\n─── OPEN QUESTIONS ───")
        for q in d.get("open_questions", []):
            lines.append(f"• {q}")
        lines.append(f"\nGenerated by OrangeTree Global AI Suite | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        return "\n".join(lines)

    text_export = generate_text_export(d)
    json_export = json.dumps(d, indent=2)

    ecol1, ecol2 = st.columns(2)
    with ecol1:
        st.download_button(
            "⬇️ Download as Text",
            data=text_export,
            file_name=f"meeting_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with ecol2:
        st.download_button(
            "⬇️ Download as JSON",
            data=json_export,
            file_name=f"meeting_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.caption("OrangeTree Global | AI SME Suite — UC1: Meeting Notes Tracker")
